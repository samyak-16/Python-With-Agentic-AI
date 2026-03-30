from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool = True


product1 = Product(id=1, name="Laptop", price=999.99, in_stock=False)


product2 = Product(id=2, name="Mouse", price=20.99)

product3 = Product(
    id=3,
    name="Keyboard",
)
