from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from farmer.api import farmer_router
from customer.api import customer_router
from orderAPI.api import order_router
from productAPI.api import product_router
from review.api import review_router


app = FastAPI(
    title="Local Food Market Place fastAPI",
    description="This is the main app for all the APIs",
    version="1.0",
)


app.include_router(customer_router, prefix="/customer", tags=["Customer"])
app.include_router(farmer_router, prefix="/farmer", tags=["Farmer"])
app.include_router(order_router, prefix="/order", tags=["Order"])
app.include_router(product_router, prefix="/product", tags=["Product"])
app.include_router(review_router, prefix="/review", tags=["Review"])
