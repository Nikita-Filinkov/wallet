from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.exceptions import (
    MaxAmountExceeded,
    MoreTowDecimalAfterComma,
    NegativeAmount,
    WrongAmount,
    WrongOperationType,
)


class SWalletBalance(BaseModel):
    wallet_uuid: UUID
    balance: Decimal
    updated_at: datetime


class SChangeBalance(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )
    operation_type: Literal["deposit", "withdraw"]
    amount: Decimal = Field(
        description="Сумма от 0.01 до 10,000,000 с максимум 2 знаками после запятой",
        examples=["0.01", "100.50", "10000000"],
    )

    @field_validator("amount", mode="before")
    def normalize_amount(cls, v):
        if v is None:
            raise WrongAmount

        if isinstance(v, str):
            v = v.strip()
            if v == "":
                raise WrongAmount
            v = v.replace(",", ".")
            if v.count(".") > 1:
                raise WrongAmount
            try:
                v = Decimal(v)
            except Exception:
                raise WrongAmount
        return v

    @field_validator("amount")
    def validate_amount_value(cls, v: Decimal):
        if v is None or v.is_nan() or v.is_infinite():
            raise WrongAmount

        if v <= Decimal("0"):
            raise NegativeAmount

        if v > Decimal("10000000"):
            raise MaxAmountExceeded

        exponent = v.as_tuple().exponent
        if exponent is not None and exponent < -2:
            raise MoreTowDecimalAfterComma
        return v

    @field_validator("operation_type", mode="before")
    def validate_operation_type(cls, v):
        if v is None:
            raise WrongOperationType

        if isinstance(v, str):
            v = v.strip().lower()
            if v not in ["deposit", "withdraw"]:
                raise WrongOperationType
        return v
