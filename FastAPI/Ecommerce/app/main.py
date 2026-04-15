from fastapi import FastAPI, HTTPException, Query, Path, status
from services.products import (
    get_all_products1,
    get_all_products2,
    addProducts1,
    deleteProduct,
)
from schema.product import Product
from uuid import UUID


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI"}


# ↑ This is literally equivalent to:

# def root():
#     return {"message": "Welcome"}

# root = app.get("/")(root)  # Two calls chained!


# @app.get("/products")
# def getProducts():
#     try:
#         return get_all_products1()
#     except IndexError:
#         raise HTTPException(status_code=404, detail="Products Not Found")


@app.get("/products")
def list_products(
    name: str = Query(
        # ...,
        default=None,
        min_length=1,
        max_length=50,
        description="Search Product by name (Case Insensitive)",
    ),
    sort_by_price: bool = Query(
        default=None, description="Sort products by price (True/False)"
    ),
    sorting_order: str = Query(
        default=None, enum=["asc", "desc"], description="Sort order"
    ),
    limit: int = Query(default=5, ge=5, le=25, description="Number of items to return"),
):

    products = get_all_products1()
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]
        if len(products) == 0:
            raise HTTPException(404, f"No any product foun with name :{name}")
        # return len(products)
    if sort_by_price and sorting_order:
        reverse = sorting_order == "desc"  # True if sorting is in descending order

        products = sorted(products, key=lambda p: p["price"], reverse=reverse)
        print("Original Length : ", len(products))
    return {
        "length": len(products[:limit]),
        "products": products[:limit],
    }


@app.get("/products/{product_id}")
def getProductById(
    product_id: str = Path(
        min_length=36, max_length=36, description="UUID of the product"
    ),
):
    products = get_all_products1()

    product = [p for p in products if p.get("id") == product_id]
    if len(product) == 0:
        raise HTTPException(404, "Product Not Found")

    return {"product": product}


@app.post("/products", status_code=status.HTTP_201_CREATED)
def addProduct(product: Product):
    products = get_all_products2()
    products.append(product.model_dump(mode="json"))
    addProducts1(products)
    return {"message": "Product Added successfully"}


@app.delete("/products", status_code=status.HTTP_200_OK)
def delete_Product(productId: UUID):
    try:
        deleteProduct(str(productId))
    except ValueError as e:
        raise HTTPException(404, str(e))
    return {"Product deleted"}
