from pydantic import (
    BaseModel,
    Field,
    AnyUrl,
    EmailStr,
    HttpUrl,
    field_validator,
    model_validator,
    computed_field,
)
from typing import Annotated, Literal, Optional, List
from datetime import datetime
from uuid import UUID


class Dimensions(BaseModel):
    length: float = Field(gt=0, strict=True, description="Length in cm")
    width: float = Field(gt=0, strict=True, description="Width in cm")
    height: float = Field(gt=0, strict=True, description="Height in cm")


class Seller(BaseModel):
    seller_id: UUID
    name: str = Field(
        min_length=2,
        max_length=60,
        description="Name of the seller (2-60)",
        title="Seller Name",
        examples=["Mi Store", "Sam Store"],
    )
    email: EmailStr
    website: HttpUrl

    @field_validator("email", mode="after")
    @classmethod
    def validate_seller_email_domain(cls, value: str):
        allowed_domains = ["example.com", "test.com"]
        domain = value.strip().split("@")[-1]
        if domain not in allowed_domains:
            raise ValueError("Invalid email domain")
        return value


class Product(BaseModel):
    id: UUID

    sku: Annotated[
        str, Field(min_length=6, max_length=30, description="Stock keeping unit")
    ]

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, value: str):
        if "-" not in value:
            raise ValueError("SKU must have '-'")
        last = value.split("-")[-1]

        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must end with 3-digit sequence like -234")
        return value

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=40,
            description="Name of the product",
            examples=["Apple vision Pro", "Samsung Ultra"],
        ),
    ]

    description: Annotated[
        str,
        Field(min_length=3, max_length=200, description="Description of the product"),
    ]
    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=25,
            description="Category of the products",
            examples=["mobile", "laptop"],
        ),
    ]

    brand: Annotated[
        str, Field(min_length=2, max_length=40, examples=["Apple", "Xiaomi"])
    ]
    price: Annotated[float, Field(gt=0, strict=True, description="Base price in NPR")]
    currency: Literal["INR"] = "INR"
    discount_percent: Annotated[
        int, Field(ge=0, le=50, description="Discount in percentage(0-50)", default=0)
    ]
    stock: Annotated[
        int, Field(ge=0, description="Available stock : Greater than or equals to 0")
    ]
    is_active: Annotated[bool, Field(description="Is product active ? ")]

    @model_validator(mode="after")
    def validate_stock_is_active(self):
        if self.stock == 0 and self.is_active is True:
            raise ValueError("If stock is 0 is_active can't be True")
        if self.stock > 0 and self.is_active is False:
            raise ValueError("If stock is > 0 is_active can't be False")
        return self

    rating: Annotated[
        float,
        Field(ge=0, le=5, description="Rating out of 5", strict=True),
    ]
    tags: Annotated[
        Optional[List[str]],
        Field(
            description="Max 10 Keywords related to product",
            default=None,
            max_length=10,
        ),
    ]
    image_urls: Annotated[
        List[AnyUrl],
        Field(
            ...,
            max_length=10,
            min_length=1,
            description="Atleast 1 image URL of the product",
        ),
    ]

    dimensions_cm: Annotated[Dimensions, Field(...)]
    seller: Annotated[Seller, Field()]
    created_at: datetime

    @computed_field
    @property
    def total_price(self) -> float:
        discount_amt = (self.discount_percent / 100) * self.price
        discounted_price = self.price - discount_amt
        return discounted_price


# UPDATE PYDANTIC


class DimensionsUpdate(BaseModel):
    length: Annotated[
        Optional[float], Field(gt=0, strict=True, description="Length in cm")
    ] = None
    width: Annotated[
        Optional[float], Field(gt=0, strict=True, description="Width in cm")
    ] = None
    height: Annotated[
        Optional[float], Field(gt=0, strict=True, description="Height in cm")
    ] = None


class SellerUpdate(BaseModel):
    seller_id: UUID  # required — need to know which seller to update

    name: Annotated[
        Optional[str],
        Field(
            min_length=2,
            max_length=60,
            description="Name of the seller",
            title="Seller Name",
        ),
    ] = None

    email: Optional[EmailStr] = None

    website: Optional[HttpUrl] = None

    @field_validator("email", mode="after")
    @classmethod
    def validate_seller_email_domain(cls, value: str):
        if value is None:
            return value
        allowed_domains = ["example.com", "test.com"]
        domain = value.strip().split("@")[-1]
        if domain not in allowed_domains:
            raise ValueError("Invalid email domain")
        return value


class ProductUpdate(BaseModel):
    id: UUID  # required

    sku: Annotated[
        Optional[str],
        Field(min_length=6, max_length=30, description="Stock keeping unit"),
    ] = None

    name: Annotated[
        Optional[str],
        Field(min_length=3, max_length=40, description="Name of the product"),
    ] = None

    description: Annotated[
        Optional[str],
        Field(min_length=3, max_length=200, description="Description of the product"),
    ] = None

    category: Annotated[
        Optional[str],
        Field(min_length=3, max_length=25, description="Category of the products"),
    ] = None

    brand: Annotated[Optional[str], Field(min_length=2, max_length=40)] = None

    price: Annotated[
        Optional[float], Field(gt=0, strict=True, description="Base price in NPR")
    ] = None

    currency: Optional[Literal["INR"]] = None

    discount_percent: Annotated[
        Optional[int], Field(ge=0, le=50, description="Discount in percentage(0-50)")
    ] = None

    stock: Annotated[Optional[int], Field(ge=0, description="Available stock")] = None

    is_active: Annotated[Optional[bool], Field(description="Is product active?")] = None

    rating: Annotated[
        Optional[float], Field(ge=0, le=5, strict=True, description="Rating out of 5")
    ] = None

    tags: Annotated[
        Optional[List[str]], Field(description="Max 10 Keywords", max_length=10)
    ] = None

    image_urls: Annotated[
        Optional[List[AnyUrl]],
        Field(max_length=10, min_length=1, description="Image URLs"),
    ] = None

    dimensions_cm: Optional[DimensionsUpdate] = None
    seller: Optional[SellerUpdate] = None
