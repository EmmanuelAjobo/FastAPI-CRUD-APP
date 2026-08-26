# Product CRUD API

A REST API for managing products, built with FastAPI, SQLModel, and PostgreSQL, using fully async database access.

## Features

- Full CRUD for products (create, read, update, delete)
- Async database layer end-to-end (async engine, async sessions)
- Separate schemas for create/update to prevent clients from setting server-controlled fields (`id`, `createdAt`)
- Auto-generated interactive API docs via FastAPI (`/docs`)

## Tech Stack

- **FastAPI** — web framework
- **SQLModel** — ORM / schema validation (built on SQLAlchemy + Pydantic)
- **PostgreSQL** — database
- **psycopg (v3, async)** — database driver
- **uv** — dependency management

## Project Structure
app/
├── main.py # routes
├── engine.py # database engine setup
├── models.py # SQLModel schemas
└── init.py
pyproject.toml
uv.lock


## Setup

1. Clone the repo:
```bash
   git clone <your-repo-url>
   cd <repo-name>
```

2. Install dependencies:
```bash
   uv sync
```

3. Create a `.env` file in the project root:
```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
```

4. Run the server:
```bash
   uv run fastapi dev app/main.py
```

5. Open `http://localhost:8000/docs` for interactive API documentation.

## API Endpoints

| Method | Endpoint       | Description          |
|--------|----------------|----------------------|
| GET    | `/posts`       | List all products    |
| GET    | `/posts/{id}`  | Get a single product  |
| POST   | `/posts`       | Create a product      |
| PUT    | `/posts/{id}`  | Update a product      |
| DELETE | `/posts/{id}`  | Delete a product      |

## Example Request

**Create a product**
```bash
curl -X POST http://localhost:8000/posts \
  -H "Content-Type: application/json" \
  -d '{"name": "Sample Product", "price": 2500, "issale": false, "inventory": 10}'
```

## License

MIT (or whatever you choose)
