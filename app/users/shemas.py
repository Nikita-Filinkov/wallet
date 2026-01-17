from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserShortResponse(BaseModel):
    id: int
    email: str
    wallets: list[UUID]
    model_config = ConfigDict(from_attributes=True)
