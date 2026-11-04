from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    quantity: int = Field(default=0, ge=0)
    category: str = Field(min_length=2, max_length=50)
    status: Literal["ACTIVE", "INACTIVE"] = "ACTIVE"

    @field_validator("name", "category")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Must contain at least 2 characters")
        return value


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductPatch(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: Decimal | None = Field(
        default=None, gt=0, max_digits=10, decimal_places=2
    )
    quantity: int | None = Field(default=None, ge=0)
    category: str | None = Field(default=None, min_length=2, max_length=50)
    status: Literal["ACTIVE", "INACTIVE"] | None = None

    @field_validator("name", "category")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if len(value) < 2:
                raise ValueError("Must contain at least 2 characters")
        return value


class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
