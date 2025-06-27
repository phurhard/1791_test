# Todo Management API

A FastAPI application for managing user accounts and todo items with authentication and database persistence.

## Features
- User authentication system (JWT-based)
- Todo item CRUD operations
- User-todo relationship management
- **AI-powered NLP suggestions for todos**
- **Productivity analysis endpoint**
- SQLite database support (default) or PostgreSQL
- API documentation via Swagger UI

## Project Structure
```
todo-api/
├── alembic/              # Database migration files
├── api/                  # Main application code
│   ├── core/             # Application settings
│   ├── database/         # Database configuration
│   ├── models/           # SQLAlchemy models
│   ├── router/           # API endpoints
│   ├── schemas/          # Pydantic models
│   ├── services/         # Business logic
│   └── utils/            # Dependencies
├── db/                   # Database files
├── main.py               # Application entry point
└── requirements.txt      # Python dependencies
```

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL or SQLite (default)

### Installation
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Create database file (if using SQLite):
    ```bash
    mkdir -p db
    touch db/database.db
    ```

### Configuration

Create a `.env` file in the project root with the following variables:
```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
DATABASE_URL=sqlite:///./db/database.db  # Or your PostgreSQL URL
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
- `SECRET_KEY`: Used for JWT token signing.
- `ALGORITHM`: JWT signing algorithm.
- `DATABASE_URL`: SQLAlchemy database URL.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time.

### Database Migrations

This project uses Alembic for database migrations.

- To create a new migration after modifying models:
    ```bash
    alembic revision --autogenerate -m "Your migration message"
    ```
- To apply migrations:
    ```bash
    alembic upgrade head
    ```

### Running the Application
```bash
uvicorn main:app --reload
```

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `POST /users/login` - Obtain JWT access token
- `GET /users/{user_id}` - Get user details
- `GET /users/` - List all users
- `PUT /users/{user_id}` - Update user information
- `DELETE /users/{user_id}` - Delete a user

### Todos
- `POST /todos/` - Create a new todo (requires auth)
- `GET /todos/{todo_id}` - Get todo details
- `GET /todos/` - List all todos
- `PUT /todos/{todo_id}` - Update a todo (requires auth)
- `DELETE /todos/{todo_id}` - Delete a todo (requires auth)

### Advanced Endpoints

- `POST /todos/nlp/` - **Generate AI-powered suggestions for a todo description**  
    **Request:**  
    ```json
    {
      "description": "Finish the quarterly report"
    }
    ```
    **Response:**  
    ```json
    {
      "suggestions": ["Break the report into sections", "Set a deadline for each section"]
    }
    ```

- `GET /todos/analyze/` - **Analyze productivity based on todos**  
    **Response:**  
    ```json
    {
      "completed": 5,
      "pending": 3,
      "productivity_score": 0.62
    }
    ```

## Authentication
- Use `/docs` endpoint to test authentication and try endpoints interactively.
- Authentication tokens (JWT) are required for protected endpoints.
- Token expiration is handled automatically.

## Testing

*No automated tests are present yet.*  
To add tests, consider using [pytest](https://docs.pytest.org/) and [httpx](https://www.python-httpx.org/) for API testing.

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## API Testing with Postman

A ready-to-use Postman collection is provided in `postman_collection.json`. This collection includes:

- All user and todo endpoints, including advanced features (NLP suggestions, productivity analysis)
- Example requests and responses for every route (success and error cases)
- Variables for `base_url`, `access_token`, `user_id`, and `todo_id` to streamline testing

### How to Use

1. Open Postman and click "Import".
2. Select the `postman_collection.json` file from this repository.
3. Set the `base_url` variable (e.g., `http://localhost:8000` if running locally).
4. Register a user and log in to obtain an access token, then set the `access_token` variable.
5. Use the provided examples to understand the expected request and response formats before sending your own requests.

This makes it easy for anyone to test and explore the API interactively.
