from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int

class TodoBase(BaseModel):
    text: str

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int
    text: str

class MiniTodoBase(BaseModel):
    text: str
    completed: bool = False

class MiniTodoCreate(MiniTodoBase):
    pass

class MiniTodoRead(MiniTodoBase):
    id: int

class ProjectWithTodos(ProjectRead):
    todos: List[TodoRead] = []

class UserProjectsAndTodos(UserRead):
    projects: List[ProjectWithTodos] = []

class AIResponse(BaseModel):
    text: str
