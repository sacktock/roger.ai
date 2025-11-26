from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    projects: Mapped[List["Project"]] = relationship(
        "Project",
        back_populates="user",
        foreign_keys="Project.user_id",
    )

class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), index=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="projects",
        foreign_keys=[user_id],
    )

    todos: Mapped[List["Todo"]] = relationship(
        "Todo",
        back_populates="project",
        foreign_keys="Todo.project_id",
    )

class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), index=True
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="todos",
        foreign_keys=[project_id],
    )

    mini_todos: Mapped[List["MiniTodo"]] = relationship(
        "MiniTodo",
        back_populates="todo",
        foreign_keys="MiniTodo.todo_id",
    )

class MiniTodo(Base):
    __tablename__ = "mini_todo"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    todo_id: Mapped[int] = mapped_column(
        ForeignKey("todo.id", ondelete="CASCADE"), index=True
    )

    todo: Mapped["Todo"] = relationship(
        "Todo",
        back_populates="mini_todos",
        foreign_keys=[todo_id]
    )