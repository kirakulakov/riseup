# catalog_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

# Hardcoded sneaker data
sneakers = [
    {
        "id": 1,
        "name": "Nike Air Max 90",
        "description": "The Air Jordan 1 Retro High is a classic sneaker that never goes out of style.",
        "price": 9999,
        "image_url": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/zwxes8uud05rkuei1mpt/air-max-90-mens-shoes-6n3vKB.png"
    },
    {
        "id": 2,
        "name": "Nike Air Force 1 LV8 5",
        "description": "The Nike Air Max 90 is a timeless classic with unmatched comfort and style.",
        "price": 8999,
        "image_url": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/6d742bce-ba92-4e66-8263-0532bbdeb78f/air-force-1-lv8-5-big-kids-shoes-k8Jkw3.png"
    },
    {
        "id": 3,
        "name": "Nike Air Force 1 '07",
        "description": "Experience ultimate comfort and energy return with the Adidas Ultraboost.",
        "price": 8999,
        "image_url": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/b7d9211c-26e7-431a-ac24-b0540fb3c00f/air-force-1-07-mens-shoes-jBrhbr.png"
    },
    {
        "id": 4,
        "name": "Nike Air Force 1 '07 (Women's)",
        "description": "The Puma RS-X combines retro style with modern technology for a unique look.",
        "price": 7999,
        "image_url": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/8d752b32-17e8-40bc-ac1a-7a8849957a12/air-force-1-07-womens-shoes-PqdxJw.png"
    },
    {
        "id": 5,
        "name": "Nike Air Force 1 '07 Next Nature",
        "description": "The New Balance 990v5 offers premium comfort and classic American craftsmanship.",
        "price": 8999,
        "image_url": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/d86cc16f-67d2-4781-a01f-7ea19eeba5cd/air-force-1-07-next-nature-womens-shoes-fvxZ0g.png"
    },
    {
        "id": 6,
        "name": "Nike Air Force 1 '07 LV8",
        "description": "The New Balance 990v5 offers premium comfort and classic American craftsmanship.",
        "price": 8999,
        "image_url": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/a9b83f5c-af29-49b5-a784-989974e9c531/air-force-1-07-lv8-mens-shoes-3Q0nlJ.png"
    }
]

@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate):
    new_product = product.dict()
    new_product["id"] = len(sneakers) + 1
    sneakers.append(new_product)
    return new_product

@app.get("/products", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100):
    return sneakers[skip : skip + limit]

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int):
    for product in sneakers:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)