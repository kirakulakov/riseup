# catalog_service/main.py
import os
import threading

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.middleware.cors import CORSMiddleware

from kafka_utils import get_kafka_consumer
import os
from dotenv import load_dotenv

load_dotenv()


def handle_user_event(event):
    if event['event'] == 'user_created':
        print(f"New user created: {event['username']}")
        # You can perform any necessary actions here, such as creating a user profile


def start_kafka_consumer():
    consumer = get_kafka_consumer('user_events')
    for message in consumer:
        handle_user_event(message.value)


# Start Kafka consumer in a separate thread
kafka_thread = threading.Thread(target=start_kafka_consumer)
kafka_thread.start()

# Database setup
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/sneakershop"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String)


Base.metadata.create_all(bind=engine)


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    image_url: str


class ProductResponse(ProductCreate):
    id: int


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("shutdown")
def shutdown_event():
    kafka_thread.join()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db=Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products", response_model=list[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db=Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
