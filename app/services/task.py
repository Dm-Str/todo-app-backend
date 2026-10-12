from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema


class TaskNotFoundError(Exception):
    """Исключение, возникающее при попытке получить задачу по несуществующему id"""
    pass


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        """Получить список всех задач"""
        tasks = self.repository.get_all()

        return [TaskSchema.model_validate(task) for task in tasks]

    def create_task(self, payload: TaskCreateSchema) -> TaskSchema:
        """Создать новую задачу"""
        task = self.repository.create(title=payload.title)

        self.db.commit()

        return TaskSchema.model_validate(task)

    def update_task(self, task_id: str, payload: TaskUpdateSchema) -> TaskSchema:
        """"Обновить задачу"""
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        task.title = payload.title if payload.title is not None else task.title
        task.completed = payload.completed if payload.completed is not None else task.completed

        self.db.commit()

        return TaskSchema.model_validate(task)

    def delete_task(self, task_id: str) -> None:
        """Удалить задачу"""
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        self.repository.delete(task)
        self.db.commit()
