from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from app.database import serializable_session
from app.exceptions import NotEnoughFunds
from app.service.base import BaseService
from app.wallet.models import Wallets
from app.wallet.shemas import SWalletBalance


class WalletsService(BaseService):
    model = Wallets

    @classmethod
    async def deposit_balance(cls, wallet_uuid: UUID, amount: Decimal):
        async with serializable_session() as session:
            query = select(cls.model).where(cls.model.wallet_uuid == wallet_uuid)
            result = await session.execute(query)
            wallet = result.scalar_one_or_none()

            if not wallet:
                return None
            wallet.balance += amount
        return SWalletBalance(wallet_uuid=wallet.wallet_uuid, balance=wallet.balance)

    @classmethod
    async def withdraw_balance(cls, wallet_uuid: UUID, amount: Decimal):
        async with serializable_session() as session:
            query = select(cls.model).where(cls.model.wallet_uuid == wallet_uuid)
            result = await session.execute(query)
            wallet = result.scalar_one_or_none()

            if not wallet:
                return None
            if wallet.balance < amount:
                raise NotEnoughFunds()
            wallet.balance -= amount

        return SWalletBalance(wallet_uuid=wallet.wallet_uuid, balance=wallet.balance)
