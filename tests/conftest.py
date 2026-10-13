from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.repositories.task import TaskRepository
from app.services.category import CategoryService
from app.services.task import TaskService


@pytest.fixture
def db_mock() -> Mock:
    """Создаём мок сессии БД один раз и переиспользуем в тестах"""
    return Mock(spec=Session)


@pytest.fixture
def repository_mock() -> Mock:
    """Создаём мок TaskRepository один раз и переиспользуем в тестах"""
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(db_mock: Mock, repository_mock: Mock) -> TaskService:
    """Создаём TaskService один раз, чтобы переиспользовать в тестах"""
    task_service = TaskService(db_mock)
    task_service.repository = repository_mock
    return task_service


@pytest.fixture
def repository_mock_category() -> Mock:
    """Создаём мок TaskRepository один раз и переиспользуем в тестах"""
    return Mock(spec=CategoryRepository)


@pytest.fixture
def service_category(db_mock: Mock, repository_mock_category: Mock) -> CategoryService:
    """Создаём TaskService один раз, чтобы переиспользовать в тестах"""
    category_service = CategoryService(db_mock)
    category_service.repository = repository_mock_category
    return category_service
