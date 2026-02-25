from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.database import engine, Base

from app.middleware.validation_handler import validation_exception_handler
from app.middleware.exception import GlobalExceptionMiddleware
from app.middleware.cors import setup_cors

from app.controllers import (
    product_controller,
    category_controller,
    customer_controller,
    order_controller
)

app = FastAPI(title="E-commerce API")

#Create tables automatically
Base.metadata.create_all(bind=engine)

setup_cors(app)

#Register middleware
app.add_middleware(GlobalExceptionMiddleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


#Register routers
app.include_router(product_controller.router)
app.include_router(category_controller.router)
app.include_router(customer_controller.router)
app.include_router(order_controller.router)