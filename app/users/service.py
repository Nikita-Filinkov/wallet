from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import async_session_maker
from app.service.base import BaseService
from app.users.models import Users
from app.users.shemas import UserShortResponse


class UsersService(BaseService):
    model = Users

    @classmethod
    async def find_by_id(cls, model_id: int) -> Optional[UserShortResponse]:
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.wallets))
                .where(cls.model.id == model_id)
            )
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if user:
                wallets = [wallet.wallet_uuid for wallet in user.wallets]
                return UserShortResponse(id=user.id, email=user.email, wallets=wallets)
            return None

    @classmethod
    async def add(cls, **data) -> Users:
        async with async_session_maker() as session:
            instance = cls.model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance
