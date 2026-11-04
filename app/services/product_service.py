import logging
from decimal import Decimal
from math import ceil
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ProductNotFoundException,
    DuplicateProductException,
)
from app.repositories.product_repository import product_repository
from app.schemas.product import ProductCreate, ProductPatch, ProductUpdate


logger = logging.getLogger(__name__)


class ProductService:

    def create_product(self, db: Session, product_data: ProductCreate):
        logger.info("Creating product: %s", product_data.name)

        existing_product = product_repository.get_by_name(
            db, product_data.name
        )

        if existing_product:
            logger.warning("Duplicate product name: %s", product_data.name)
            raise DuplicateProductException("Product name already exists")

        try:
            product = product_repository.create(db, product_data)
            logger.info("Product created successfully: %s", product.id)
            return product

        except IntegrityError:
            db.rollback()
            logger.exception("Database integrity error while creating product")
            raise DuplicateProductException("Product name already exists")

    def get_product(self, db: Session, product_id: UUID):
        logger.info("Fetching product: %s", product_id)

        product = product_repository.get_by_id(db, product_id)

        if not product:
            logger.warning("Product not found: %s", product_id)
            raise ProductNotFoundException(str(product_id))

        return product

    def list_products(
        self,
        db: Session,
        page: int = 1,
        size: int = 10,
        category: str | None = None,
        status_filter: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        sort: str = "name,asc",
    ):
        logger.info("Listing products: page=%s, size=%s", page, size)

        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="minPrice cannot be greater than maxPrice",
                )

        products, total_items = product_repository.get_all(
            db=db,
            page=page,
            size=size,
            category=category,
            status=status_filter,
            min_price=min_price,
            max_price=max_price,
            sort=sort,
        )

        logger.info("Retrieved %s products", total_items)

        return {
            "items": products,
            "page": page,
            "size": size,
            "totalItems": total_items,
            "totalPages": ceil(total_items / size) if total_items else 0,
        }

    def update_product(
        self,
        db: Session,
        product_id: UUID,
        product_data: ProductUpdate,
    ):
        logger.info("Updating product: %s", product_id)

        product = self.get_product(db, product_id)

        existing_product = product_repository.get_by_name(
            db, product_data.name
        )

        if existing_product and existing_product.id != product_id:
            logger.warning("Duplicate product name: %s", product_data.name)
            raise DuplicateProductException("Product name already exists")

        try:
            updated_product = product_repository.update(
                db, product, product_data
            )
            logger.info("Product updated successfully: %s", product_id)
            return updated_product

        except IntegrityError:
            db.rollback()
            logger.exception("Database integrity error while updating product")
            raise DuplicateProductException("Product name already exists")

    def patch_product(
        self,
        db: Session,
        product_id: UUID,
        product_data: ProductPatch,
    ):
        logger.info("Partially updating product: %s", product_id)

        product = self.get_product(db, product_id)

        update_data = product_data.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] is not None:
            existing_product = product_repository.get_by_name(
                db, update_data["name"]
            )

            if existing_product and existing_product.id != product_id:
                logger.warning("Duplicate product name: %s", update_data["name"])
                raise DuplicateProductException("Product name already exists")

        try:
            updated_product = product_repository.patch(
                db, product, product_data
            )
            logger.info("Product patched successfully: %s", product_id)
            return updated_product

        except IntegrityError:
            db.rollback()
            logger.exception("Database integrity error while patching product")
            raise DuplicateProductException("Product name already exists")

    def delete_product(self, db: Session, product_id: UUID):
        logger.info("Deleting product: %s", product_id)

        product = self.get_product(db, product_id)
        product_repository.delete(db, product)

        logger.info("Product deleted successfully: %s", product_id)


product_service = ProductService()
