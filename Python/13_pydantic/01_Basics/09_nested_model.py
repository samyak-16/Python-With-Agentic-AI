from typing import List, Optional
from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    postal_code: str


class User(BaseModel):
    id: int
    name: str
    address: Address


address = Address(street="123", city="Jaipur", postal_code="553321")
user = User(id=1, name="Samyak", address=address)


print("Printing")
print(user.address.model_dump())
print(type(user.address))
#  user.address is an instance of the Address class — specifically, a Pydantic BaseModel instance.


user_data = {
    "id": 1,
    "name": "Samyak",
    "address": {"street": "321sadda", "city": "paris", "postal_code": "200020"},
}

user = User(**user_data)
print("Printing User data in dict form")
print(user.model_dump())
