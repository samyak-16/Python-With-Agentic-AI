from typing import Optional

from pydantic import BaseModel, Field
import re  # regular expression


class Employee(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee Name",
        examples="Samak Raj Subedi",
    )
    department: Optional[str] = "General"

    salary: float = Field(
        ...,
        ge=10000,  # Greater tahn or equal to
        # ge,gt,le,lt,regex
        le=100000,
        description="Annual Salary in USD ",
    )


class User(BaseModel):
    email: str = Field(..., regex=r"")
    phone: str = Field(..., regex=r"")
    age: int = Field(
        ...,
        ge=0,
        le=150,
        description="Age in years",
    )
    discount: float = Field(..., le=0, description="Discount Percentage")
