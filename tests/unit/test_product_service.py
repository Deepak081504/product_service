from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import MagicMock, patch

import pytest

from app.services.product_service import ProductService
from app.core.exceptions import (
    ProductNotFoundException,
    DuplicateProductException,
)
from app.schemas.product import ProductCreate, ProductPatch, ProductUpdate


@pytest.fixture
def service():
    return ProductService()


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def sample_product():
    return SimpleNamespace(
        id=uuid4(),
        name="Gaming Mouse",
        description="Wireless Gaming Mouse",
        price=Decimal("1500.00"),
        quantity=20,
        category="Accessories",
        status="ACTIVE",
    )


@pytest.fixture
def product_data():
    return ProductCreate(
        name="Gaming Mouse",
        description="Wireless Gaming Mouse",
        price=Decimal("1500.00"),
        quantity=20,
        category="Accessories",
        status="ACTIVE",
    )


def test_create_product_success(service, db, product_data, sample_product, monkeypatch):
    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_by_name",
        lambda db, name: None,
    )
    monkeypatch.setattr(
        "app.services.product_service.product_repository.create",
        lambda db, data: sample_product,
    )

    result = service.create_product(db, product_data)

    assert result.name == "Gaming Mouse"
    assert result.price == Decimal("1500.00")


def test_create_duplicate_product(service, db, product_data, sample_product, monkeypatch):
    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_by_name",
        lambda db, name: sample_product,
    )

    with pytest.raises(DuplicateProductException):
        service.create_product(db, product_data)


def test_get_product_success(service, db, sample_product, monkeypatch):
    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_by_id",
        lambda db, product_id: sample_product,
    )

    result = service.get_product(db, sample_product.id)

    assert result.id == sample_product.id


def test_get_product_not_found(service, db, monkeypatch):
    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_by_id",
        lambda db, product_id: None,
    )

    with pytest.raises(ProductNotFoundException):
        service.get_product(db, uuid4())


def test_list_products_success(service, db, sample_product, monkeypatch):
    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_all",
        lambda **kwargs: ([sample_product], 1),
    )

    result = service.list_products(db, page=1, size=10)

    assert len(result["items"]) == 1
    assert result["totalItems"] == 1
    assert result["totalPages"] == 1


def test_list_products_invalid_price_range(service, db):
    with pytest.raises(Exception) as exc_info:
        service.list_products(
            db,
            min_price=Decimal("2000"),
            max_price=Decimal("1000"),
        )

    assert exc_info.value.status_code == 400


def test_delete_product_success(service, db, sample_product, monkeypatch):
    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_by_id",
        lambda db, product_id: sample_product,
    )

    deleted = []

    monkeypatch.setattr(
        "app.services.product_service.product_repository.delete",
        lambda db, product: deleted.append(product),
    )

    service.delete_product(db, sample_product.id)

    assert len(deleted) == 1
    assert deleted[0].id == sample_product.id


def test_update_product_success(service, db, sample_product, product_data, monkeypatch):
    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_by_id",
        lambda db, product_id: sample_product,
    )
    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_by_name",
        lambda db, name: None,
    )
    monkeypatch.setattr(
        "app.services.product_service.product_repository.update",
        lambda db, product, data: product,
    )

    result = service.update_product(db, sample_product.id, product_data)

    assert result.id == sample_product.id


def test_patch_product_success(service, db, sample_product, monkeypatch):
    patch_data = ProductPatch(price=Decimal("2000.00"))

    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_by_id",
        lambda db, product_id: sample_product,
    )
    monkeypatch.setattr(
        "app.services.product_service.product_repository.patch",
        lambda db, product, data: product,
    )

    result = service.patch_product(db, sample_product.id, patch_data)

    assert result.id == sample_product.id


def test_patch_duplicate_product(service, db, sample_product, monkeypatch):
    patch_data = ProductPatch(name="Existing Product")

    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_by_id",
        lambda db, product_id: sample_product,
    )
    monkeypatch.setattr(
        "app.services.product_service.product_repository.get_by_name",
        lambda db, name: SimpleNamespace(id=uuid4()),
    )

    with pytest.raises(DuplicateProductException):
        service.patch_product(db, sample_product.id, patch_data)
