#  What is serialization in general ??
# ----> Serialization is the process to  convert a complex data type like pydantic model into normal Objects like
# Python Dict
# JSON Strings
# XML


from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

# model_config = settings for the model, ConfigDict = the way to write those settings cleanly.


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    createdAt: datetime
    address: Address
    tags: List[str] = []

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime("%d-%m-%Y")}
    )
    # When converthing to json_string datetime becomes : "createdAt":"15-03-2024"

    # "Whenever you encounter a datetime field during serialization, run this function on it instead of default behavior"

    # lambda v: v.strftime("%d-%m-%Y") → takes the datetime object v and formats it into a custom string.


user = User(
    id=1,
    name="Samyak",
    email="h@hitesh.ai",
    createdAt=datetime(2024, 3, 15),
    address=Address(street="Godhuli Marg", city="Biratnagar", zip_code="52211"),
    is_active=False,
    tags=["Premium"],
)


python_dict = user.model_dump()
python_json = user.model_dump_json()
# print(user)

print(python_json)
# print("=" * 100)
# print(python_dict)
