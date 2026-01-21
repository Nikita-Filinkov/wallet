import asyncio
import json
from datetime import datetime

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.users.models import Users
from app.wallet.models import Wallets


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def load_mock_data(model: str):
    with open(f"app/tests/mok_files/mock_{model}.json", encoding="utf-8") as file:
        return json.load(file)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    users = load_mock_data("users")
    wallets = load_mock_data("wallets")

    for wallet in wallets:
        wallet["created_at"] = datetime.strptime(wallet["created_at"], "%Y-%m-%d")
        wallet["updated_at"] = datetime.strptime(wallet["updated_at"], "%Y-%m-%d")

    async with async_session_maker() as session:
        await session.execute(insert(Users).values(users))
        await session.execute(insert(Wallets).values(wallets))
        await session.commit()

    yield


@pytest_asyncio.fixture(scope="function")
async def asyncclient():
    async with LifespanManager(fastapi_app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://test"
        ) as ac:
            yield ac


@pytest_asyncio.fixture(scope="session")
async def auth_asyncclient():
    async with LifespanManager(fastapi_app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://test"
        ) as auth_ac:
            login_response = await auth_ac.post(
                url="/auth/login", json={"email": "test@test.com", "password": "test"}
            )
            auth_ac.cookies.update(login_response.cookies)
            yield auth_ac


@pytest_asyncio.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
