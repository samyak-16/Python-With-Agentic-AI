from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime


#  Multiple Field Validation
class Person(BaseModel):
    first_name: str
    last_name: str

    @field_validator(
        "first_name", "last_name"
    )  # Pydantic calls your validator twice — once per field: So, here the fn runs two times in total
    @classmethod
    def names_must_be_capitalize(cls, value):
        print(value)
        if not value.istitle():
            raise ValueError("Names must be capatilized")

        return value


person1 = Person(first_name="Samyak Raj", last_name="Subedi")


# --------------------------------------------


# Usecase of field_validator to update the attributes
class User(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, v):
        return v.lower().strip()


u1 = User(email="SAMYAKRAJSUBEDI@GMAIL.com")

print(u1.email)


# -----------------------------------------------

# Normalising price to float if it is passed as string with $ sign


class Product(BaseModel):
    price: str  # $4.44
    field_validator("price", mode="before")

    @classmethod
    def parse_price(cls, v):
        if isinstance(v, str):
            return float(v.replace("$", "").replace(",", "."))
        return v


# -----------------------------------------------


#  Validate Date using model_validator
class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    @classmethod
    def validate_date_range(self):
        if self.start_date >= self.end_date:
            raise ValueError("End date must be after start date")
        return self
