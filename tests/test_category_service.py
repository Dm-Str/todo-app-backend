from unittest.mock import Mock

import pytest

from app.models.category import CategoryORM
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryNotFoundError, CategoryService


def test_list_categories_returns_pydantic_models(
    service_category: CategoryService, repository_mock_category: Mock
) -> None:
    repository_mock_category.get_all.return_value = [
        CategoryORM(id="category-1", name="Category_1"),
        CategoryORM(id="category-2", name="Category_222"),
    ]

    result = service_category.list_categories()

    assert result == [
        CategorySchema(id="category-1", name="Category_1"),
        CategorySchema(id="category-2", name="Category_222"),
    ]


def test_create_category_commits_created_category(
    service_category: CategoryService, db_mock: Mock, repository_mock_category: Mock
) -> None:
    created_category = CategoryORM(id="category-1", name="new category")
    repository_mock_category.create.return_value = created_category

    result = service_category.create_category(CategoryCreateSchema(name="new category"))

    repository_mock_category.create.assert_called_once_with(name="new category")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {"id": "category-1", "name": "new category"}


@pytest.mark.parametrize(
    ("payload", "expected_name"),
    [
        pytest.param(
            CategoryUpdateSchema(name="Обновить заголовок"),  # payload
            "Обновить заголовок",  # expected_title
        ),
        pytest.param(
            CategoryUpdateSchema(name="Готово"),  # payload
            "Готово",  # expected_title
        ),
    ],
)
def test_update_category_updates_only_passed_fields(
    service_category: CategoryService,
    db_mock: Mock,
    repository_mock_category: Mock,
    payload: CategoryUpdateSchema,
    expected_name: str,
) -> None:
    category = CategoryORM(id="category-1", name="Старая задача")
    repository_mock_category.get_by_id.return_value = category

    result = service_category.update_category("category-1", payload)

    repository_mock_category.get_by_id.assert_called_once_with("category-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {"id": "category-1", "name": expected_name}


def test_update_category_raises_when_category_not_found(
    service_category: CategoryService,
    db_mock: Mock,
    repository_mock_category: Mock,
) -> None:
    repository_mock_category.get_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):  # Должна произойти указанная ошибка
        service_category.update_category(
            "missing-category", CategoryUpdateSchema(name="Неважно")
        )

    db_mock.commit.assert_not_called()
