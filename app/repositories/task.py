from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import TaskORM


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[TaskORM]:
        """Получить все записи tasks"""
        return self.db.scalars(select(TaskORM)).all()

    def get_by_id(self, task_id: str) -> TaskORM | None:
        """Получить запись tasks по id"""
        return self.db.get(TaskORM, task_id)

    def create(self, title: str) -> TaskORM:
        """Создать новую запись tasks"""
        task = TaskORM(title=title, completed=False)
        self.db.add(task)

        return task

    def delete(self, task: TaskORM) -> None:
        """Удалить запись tasks"""
        self.db.delete(task)
