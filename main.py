from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Product
from schemas import ProductCreate, ProductResponse


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Amazon Backend System",
    description="E-commerce backend API built with FastAPI",
    version="1.0.0"
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Amazon Backend API is running",
        "status": "success"
    }


# --------------------------------------------------
# CREATE PRODUCT
# --------------------------------------------------

@app.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# --------------------------------------------------
# GET ALL PRODUCTS
# --------------------------------------------------

@app.get("/products", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()

    return products


# --------------------------------------------------
# GET PRODUCT BY ID
# --------------------------------------------------

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# --------------------------------------------------
# SEARCH PRODUCTS
# --------------------------------------------------

@app.get("/products/search/{keyword}", response_model=list[ProductResponse])
def search_products(
    keyword: str,
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.name.ilike(f"%{keyword}%")
    ).all()

    return products


# --------------------------------------------------
# UPDATE PRODUCT
# --------------------------------------------------

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = updated_product.name
    product.description = updated_product.description
    product.price = updated_product.price
    product.category = updated_product.category
    product.stock = updated_product.stock

    db.commit()
    db.refresh(product)

    return product


# --------------------------------------------------
# DELETE PRODUCT
# --------------------------------------------------

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }