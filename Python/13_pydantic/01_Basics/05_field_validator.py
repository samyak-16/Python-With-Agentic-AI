from pydantic import BaseModel, field_validator, model_validator


class User(BaseModel):
    username: str

    @field_validator("username")
    @classmethod  # Required in pydantic v2
    def username_length(cls, value):
        if len(value) < 4:
            raise ValueError("Username must be atleast 4 characters")

        return value
        #  — Pydantic takes whatever your function returns and stores it as the field value:


class UserSignup(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")  # run after all fields are validated
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwordss don't match")
        return self


# Testing
user1 = UserSignup(username="Samyak", password="1234", confirm_password="1234")  # ✅
user2 = UserSignup(username="Samyak", password="1234", confirm_password="abcd")  # ❌
