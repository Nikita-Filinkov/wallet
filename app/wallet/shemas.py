from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class SWalletBalance(BaseModel):
    wallet_uuid: UUID
    balance: Decimal


class SChangeBalance(BaseModel):
    operation_type: str
    amount: Decimal
