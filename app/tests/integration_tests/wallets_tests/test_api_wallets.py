import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(['wallet_uuid', 'operation_type', 'amount', 'status_code', 'detail'], [
    ('7137abbc-ca3c-4ce1-9369-a4f1cdeabb0d', 'withdraw', 1000, 200, None),
    ('7137abbc-ca3c-4ce1-9369-a4f1cdeabb0d', 'withdraw', 1000, 409, "Недостаточно средств"),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'deposit', 1000, 200, None),
    ('3fa85f64-ca3c-5e1a-9369-2c963f66afa6', 'put', 1000, 400, "Тип операции должен быть 'deposit' или 'withdraw'"),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'deposit', 0, 400, "Число должно быть положительным"),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'deposit', -1, 400, "Число должно быть положительным"),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'deposit', 0.01, 200, None),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'deposit', 1.1, 200, None),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'deposit', "1.1", 200, None),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'deposit', "1,1", 200, None),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'deposit', "1,,1", 400, "Не верный формат ввода 'amount'"),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'deposit', 1.111, 400, "Введено больше двух цифр после запятой"),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'deposit', 10000001, 400, "Введённое число превышает 10000000"),
])
@pytest.mark.asyncio
async def test_change_balance(wallet_uuid, operation_type, status_code, amount, detail, auth_asyncclient: AsyncClient):
    response = await auth_asyncclient.patch(f"/wallet/{wallet_uuid}",
                                            json={"operation_type": operation_type, "amount": amount})
    assert response.status_code == status_code
    response_data = response.json()
    assert response_data.get("detail") == detail


@pytest.mark.parametrize(['wallet_uuid', 'balance', 'status_code', 'detail'], [
    ('7137abbc-ca3c-4ce1-9369-a4f1cdeabb0d', "0.00", 200, None),
    ('7137abbc-ca3c-4ce1-9369-a4f1cd', None, 422, "Неверный формат UUID кошелька"),
    ('3fa85f64-5717-4562-b3fc-2c963f66afa6', None, 403, "У вас нет такого кошелька"),
    ('8137abbc-ca3c-4ce1-9369-a4f1cdeabb0d', None, 404, "Кошелек не найден"),
])
@pytest.mark.asyncio
async def test_get_balance(wallet_uuid, balance, status_code, detail, auth_asyncclient: AsyncClient):
    response = await auth_asyncclient.get(f"/wallet/{wallet_uuid}")
    assert response.status_code == status_code
    response_data = response.json()
    assert response_data.get("balance") == balance
    assert response_data.get("detail") == detail
