import pytest

from app.users.service import UsersService


@pytest.mark.parametrize(
    ["email", "is_present"],
    [
        ("test@test.com", True),
        ("nikita@example.com", True),
        ("...", False),
    ],
)
@pytest.mark.asyncio
async def test_find_user_by_email(email, is_present):
    user = await UsersService.find_one_or_none(email=email)

    if is_present:
        assert user is not None
        assert user.email == email
    else:
        assert user is None


@pytest.mark.parametrize(
    ["id_user", "email", "is_present"],
    [
        (1, "test@test.com", True),
        (2, "nikita@example.com", True),
        (6, "...", False),
    ],
)
@pytest.mark.asyncio
async def test_find_user_by_id(id_user, email, is_present):
    user_response = await UsersService.find_by_id(id_user)

    if is_present:
        assert user_response is not None
        assert user_response.id == id_user
        assert user_response.email == email
    else:
        assert user_response is None
