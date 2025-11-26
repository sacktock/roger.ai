# roger.ai Server (FastAPI + SQLAlchemy Backend)

This is the backend for the TODO Agent.

## Features

- FastAPI
- SQLAlchemy ORM
- SQLite (file-based DB)
- Basic CRUD for:
  - Projects
  - TODO items tied to projects

## Layout

server/
   ├─ README.md
   ├─ Dockerfile
   ├─ requirements.txt
   └─ app/
      ├─ __init__.py
      ├─ __main__.py      # FastAPI app + endpoints here
      ├─ db.py
      ├─ models.py
      ├─ schemas.py
      └─ crud.py

## Run locally (without Docker)

```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.__main__:app --reload
