from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ProductNotFoundException(Exception):
    def __init__(self, product_id: str):
        self.product_id = product_id


class DuplicateProductException(Exception):
    def __init__(self, message: str = "Product already exists"):
        self.message = message


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ProductNotFoundException)
    async def product_not_found_handler(
        request: Request,
        exc: ProductNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Product not found",
                "error": {"product_id": exc.product_id}
            }
        )

    @app.exception_handler(DuplicateProductException)
    async def duplicate_product_handler(
        request: Request,
        exc: DuplicateProductException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": exc.message,
                "error": None
            }
        )