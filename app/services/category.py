from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)


class CategoryNotFoundError(Exception):
    """Исключение, возникающее при попытке получить категорию по несуществующему id"""

    pass


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository(db)

    def list_categories(self) -> list[CategorySchema]:
        categories = self.repository.get_all()

        return [CategorySchema.model_validate(category) for category in categories]

    def create_category(self, payload: CategoryCreateSchema) -> CategorySchema:
        category = self.repository.create(name=payload.name)
        self.db.commit()

        return CategorySchema.model_validate(category)

    def update_category(
        self, category_id: str, payload: CategoryUpdateSchema
    ) -> CategorySchema:
        category = self.repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError(f"Category with id {category_id} not found")

        if payload.name is not None:
            category.name = payload.name

        self.db.commit()

        return CategorySchema.model_validate(category)

    def delete(self, category_id: str) -> None:
        category = self.repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError(f"Category with id {category_id} not found")

        self.repository.delete(category)
        self.db.commit()
