# Todo Management API

A FastAPI application for managing user accounts and todo items with authentication and database persistence.

## Features
- User authentication system
- Todo item CRUD operations
- User-todo relationship management
- SQLite database support
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
│   └── services/         # Business logic
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
touch db/database.db
```

### Configuration
Create a `.env` file with:
```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

### Running the Application
```bash
uvicorn main:app --reload
```

## API Endpoints

### Users
- `POST /users/` - Create a new user
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

## Authentication
- Use `/docs` endpoint to test authentication
- Authentication tokens are required for todo operations
- Token expiration is handled automatically

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.