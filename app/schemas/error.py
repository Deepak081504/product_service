from typing import Any
from pydantic import BaseModel, ConfigDict


class ErrorDetail(BaseModel):
    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: Any | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "message": "Product not found",
                "error": {
                    "product_id": "product-uuid"
                }
            }
        }
    )