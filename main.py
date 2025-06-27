from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from api.router.user_router import router as user_router
from api.router.todo_router import router as todo_router
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

app = FastAPI(openapi_url="/openapi.json", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom OpenAPI schema to include bearer token
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="1791_test",
        version="1.0.0",
        description="Do cool AI Stuffs",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "security" in method:
                method["security"].append({"Bearer": []})
            else:
                method["security"] = [{"Bearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Enhanced error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": "HTTPException"},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": exc.errors(), "type": "ValidationError"},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "type": "Exception"},
    )

app.include_router(user_router)
app.include_router(todo_router)

@app.get("/")
def read_root():
    return {"message": "API is running"}
