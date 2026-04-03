from pydantic import BaseModel, computed_field, Field


class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


user = User(first_name="Samyak", last_name="Subedi")

# Without @computed_field
user.model_dump()  # {"first_name": "Samyak", "last_name": "Subedi"}
# full_name missing ❌ — Pydantic doesn't know about plain @property

# With @computed_field
user.model_dump()  # {"first_name": "Samyak", "last_name": "Subedi", "full_name": "Samyak Subedi"}
# full_name included ✅ — Pydantic knows about it

# ----------------------------------------------------------------------------


class Booking(BaseModel):
    user_id: int
    room_id: int
    nights: int = Field(..., ge=1)
    rate_per_night: float

    @computed_field
    @property
    def total_amount(self) -> float:
        return self.nights * self.rate_per_night


booking = Booking(user_id=123, room_id=456, nights=3, rate_per_night=100)

print(booking.total_amount)
print(booking.model_dump())
