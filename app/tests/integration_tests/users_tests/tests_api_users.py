import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    ["email", "password", "status_code"],
    [
        ("t@t.com", "t", 200),
        ("test@test.com", "w", 409),
        ("q@q.com", "q", 200),
        ("tt.com", "t", 422),
    ],
)
@pytest.mark.asyncio
async def test_register_user(email, password, status_code, asyncclient: AsyncClient):
    response = await asyncclient.post(
        "/v1/auth/register", json={"email": email, "password": password}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ["email", "password", "status_code"],
    [
        ("test@test.com", "test", 200),
        ("nikita@example.com", "nikita", 200),
        ("wrong@wrong.com", "wrong", 401),
    ],
)
@pytest.mark.asyncio
async def test_logging_user(email, password, status_code, asyncclient: AsyncClient):
    response = await asyncclient.post(
        "/v1/auth/login", json={"email": email, "password": password}
    )
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_logout_user(auth_asyncclient: AsyncClient):
    response = await auth_asyncclient.post("/v1/auth/logout")
    cookies = response.cookies
    wallet_cookie = cookies.get("wallet_access_token")
    assert response.status_code == 200
    assert wallet_cookie is None
