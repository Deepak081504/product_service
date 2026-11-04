from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductPatch, ProductUpdate


class ProductRepository:

    def create(self, db: Session, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    def get_by_id(self, db: Session, product_id: UUID) -> Product | None:
        return db.get(Product, product_id)

    def get_by_name(self, db: Session, name: str) -> Product | None:
        statement = select(Product).where(
            func.lower(Product.name) == name.strip().lower()
        )
        return db.scalar(statement)

    def get_all(
        self,
        db: Session,
        page: int = 1,
        size: int = 10,
        category: str | None = None,
        status: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        sort: str = "name,asc",
    ) -> tuple[list[Product], int]:

        statement = select(Product)

        if category:
            statement = statement.where(Product.category.ilike(category))

        if status:
            statement = statement.where(Product.status == status)

        if min_price is not None:
            statement = statement.where(Product.price >= min_price)

        if max_price is not None:
            statement = statement.where(Product.price <= max_price)

        total_statement = select(func.count()).select_from(
            statement.order_by(None).subquery()
        )
        total_items = db.scalar(total_statement) or 0

        sort_field, _, sort_order = sort.partition(",")

        if sort_field == "price":
            order_column = Product.price
        else:
            order_column = Product.name

        if sort_order.lower() == "desc":
            statement = statement.order_by(order_column.desc())
        else:
            statement = statement.order_by(order_column.asc())

        statement = statement.offset((page - 1) * size).limit(size)

        products = list(db.scalars(statement).all())

        return products, total_items

    def update(
        self,
        db: Session,
        product: Product,
        product_data: ProductUpdate,
    ) -> Product:
        update_data = product_data.model_dump()

        for field, value in update_data.items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)

        return product

    def patch(
        self,
        db: Session,
        product: Product,
        product_data: ProductPatch,
    ) -> Product:
        update_data = product_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)

        return product

    def delete(self, db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()


product_repository = ProductRepository()
