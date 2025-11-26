from contextlib import asynccontextmanager

from typing import List, Generator

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import SessionLocal, Base, engine, get_db
from . import schemas, models
from sqlalchemy import insert, select, update

from .internal.ai import ResponseModel, get_ai

from pydantic import BaseModel

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    # Insert seed data
    with SessionLocal() as db:
        db.execute(insert(models.User).values(id=1, name="sacktock"))
        db.execute(insert(models.Project).values(
            id=1, name="MASA-Safe-RL", user_id=1,
            description="A comprehensive library for Multi Agent and Single Agent (MASA) Safe Reinforcement Learning"
        ))
        db.execute(insert(models.Todo).values(
            id=1, text="Add PPO/A2C Implementations", project_id=1,
        ))
        db.commit()
    yield

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello from roger.ai server!"}

@app.get("/users/{user_id}")
def get_user(
    user_id: int, db: Session = Depends(get_db)
) -> schemas.UserRead:
    user = db.scalar(select(models.User).where(models.User.id == user_id))
    return {
        "id": user_id,
        "name": user.name,
    }

@app.get("/projects/{project_id}/todos")
def get_project_todos(
    project_id: int, db: Session = Depends(get_db)
) -> List[schemas.TodoRead]:
    project = db.scalar(select(models.Project).where(models.Project.id == project_id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.scalars(
        select(models.Todo)
        .where(models.Project.id == project_id)
    ).all()

@app.get("/users/{user_id}/projects/todos")
def get_user_projects_and_todos(
    user_id: int, db: Session = Depends(get_db)
) -> schemas.UserProjectsAndTodos:
    user = db.scalar(select(models.User).where(models.User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    projects = db.scalars(
        select(models.Project)
        .where(models.Project.user_id == user_id)
        .order_by(models.Project.id)
    ).all()
    response = {
        "id": user_id,
        "name": user.name,
        "projects": [],
    }
    for project in projects:
        todos = db.scalars(
            select(models.Todo)
            .where(models.Todo.project_id == project.id)
            .order_by(models.Todo.id)
        ).all()
        response["projects"].append(
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "todos": [{"id": todo.id, "text": todo.text} for todo in todos],
            }
        )
    return response

@app.get("/roger/request")
async def make_roger_request(
    text: str, ai: ResponseModel = Depends(get_ai)
) -> schemas.AIResponse:
    response = ai.response(text)
    if not response or getattr(response, "status", None) != "completed":
        raise HTTPException(status_code=500, detail="Internal AI error")
    return {"text": response.output_text}

@app.post("/users/update/{user_id}")
def update_user(
    user_id: int, name: str, db: Session = Depends(get_db)
) -> schemas.UserUpdate:
    user = db.scalar(select(models.User).where(models.User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.execute(
        update(models.User)
        .where(models.User.id == user_id)
        .values(
            name=name
        )
    )
    return {"name": name}





