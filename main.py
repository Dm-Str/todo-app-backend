from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class Task(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreate(BaseModel):
    title: str


class Book(BaseModel):
    book: str


tasks: list[Task] = []
book = ""


@app.get("/tasks", response_model=list[Task])
async def get_tasks() -> list[Task]:
    """Получить спсиок задач"""
    return tasks


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task_create: TaskCreate) -> Task:
    """Создать задачу"""
    task = Task(
        id=str(uuid4()),
        **task_create.model_dump(),
        completed=False
    )

    tasks.append(task)

    return task


@app.get("/book")
async def get_book() -> str:
    """Получить любимую книгу"""
    return f"Любимая книга: {book}"


@app.post("/book", status_code=status.HTTP_201_CREATED)
async def set_book(book_data: Book) -> str:
    """Добавить любимую книгу"""
    global book
    book = book_data.book

    return f"Любимая книга добавленна: {book}"
