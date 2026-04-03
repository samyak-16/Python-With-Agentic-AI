from pydantic import BaseModel, model_validator


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
