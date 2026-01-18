from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class SWalletBalance(BaseModel):
    wallet_uuid: UUID
    balance: Decimal
    updated_at: datetime


class SChangeBalance(BaseModel):
    operation_type: str
    amount: Decimal
