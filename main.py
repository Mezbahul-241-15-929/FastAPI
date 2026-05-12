from fastapi import FastAPI
from models import Product

app = FastAPI()

products = [
    Product(id=1, name="Phone", price=500.0, quantity=10),
    Product(id=2, name="Laptop", price=1000.0, quantity=5)
]

@app.get("/")
def greet():
    return "Welcome to FastAPI"

@app.get("/products")
def get_all_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"error": "Product not found"}

@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product