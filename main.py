from fastapi import FastAPI
from models import Product

from database import session

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
    # db connection
    db = session()
    # query
    db.query()
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

@app.put("/products/{id}")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return {"message": "Product updated successfully"}
    return {"error": "Product not found"}

@app.delete("/products/{id}")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return {"message": "Product deleted successfully"}
    return {"error": "Product not found"}