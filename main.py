from fastapi import FastAPI
from api.router.user_router import router as user_router
from api.router.todo_router import router as todo_router

app = FastAPI()

app.include_router(user_router)
app.include_router(todo_router)

@app.get("/")
def read_root():
    return {"message": "API is running"}
