from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import (
    ProductCreate,
    ProductPatch,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import product_service

router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: ProductCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    product = product_service.create_product(db, product_data)
    response.headers["Location"] = f"/api/v1/products/{product.id}"
    return product


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    return product_service.get_product(db, product_id)


@router.get("")
def list_products(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    category: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    min_price: Decimal | None = Query(default=None, alias="minPrice", gt=0),
    max_price: Decimal | None = Query(default=None, alias="maxPrice", gt=0),
    sort: str = Query(default="name,asc", pattern=r"^(name|price),(asc|desc)$"),
    db: Session = Depends(get_db),
):
    return product_service.list_products(
        db=db,
        page=page,
        size=size,
        category=category,
        status_filter=status_filter,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
    )


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
):
    return product_service.update_product(db, product_id, product_data)


@router.patch("/{product_id}", response_model=ProductResponse)
def patch_product(
    product_id: UUID,
    product_data: ProductPatch,
    db: Session = Depends(get_db),
):
    return product_service.patch_product(db, product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    product_service.delete_product(db, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
