from fastapi import FastAPI,Depends
from models import Product

from database import SessionLocal,engine
import database_model

from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


database_model.Base.metadata.create_all(bind=engine)



products = [
    Product(id=1, name="Phone", price=500.0, quantity=10),
    Product(id=2, name="Laptop", price=1000.0, quantity=5)
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()

    count = db.query(database_model.Product).count()
    if count ==0:
        for product in products:
            db.add(database_model.Product(**product.model_dump()))
        db.commit()


init_db()

@app.get("/")
def greet():
    return "Welcome to FastAPI"

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_model.Product).all()
    return db_products

@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()
    if db_product:
        return db_product
    return {"error": "Product not found"}

@app.post("/products")
def create_product(product: Product,db: Session = Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated successfully"
    
    else:
        return {"error": "Product not found"}

@app.delete("/products/{id}")
def delete_product(id: int,db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    else: return {"error": "Product not found"}
        