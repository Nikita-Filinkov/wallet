from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class WalletException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(WalletException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(WalletException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(WalletException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class TokenAbsentException(WalletException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class TokenInvalidFormatException(WalletException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIdNotInJWTException(WalletException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Id не был передан"


class UserNotFoundException(WalletException):
    status_code = status.HTTP_401_UNAUTHORIZED


class WalletNotFound(WalletException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Кошелек не найден"


class NotEnoughFunds(WalletException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Недостаточно средств"


class DontHaveThisWallet(WalletException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "У вас нет такого кошелька"


class NegativeAmount(WalletException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Число должно быть положительным"


class MoreTowDecimalAfterComma(WalletException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Введено больше двух цифр после запятой"


class WrongOperationType(WalletException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Тип операции должен быть 'deposit' или 'withdraw'"


class WrongAmount(WalletException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Не верный формат ввода 'amount'"


class MaxAmountExceeded(WalletException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Введённое число превышает 10000000"


def add_validation_exception_handler(app: FastAPI):
    """Добавляет кастомный обработчик ошибок валидации"""

    @app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errors = exc.errors()

        for error in errors:
            if error["type"] == "uuid_parsing":
                if "wallet_uuid" in str(error["loc"]):
                    return JSONResponse(
                        status_code=422,
                        content={
                            "detail": "Неверный формат UUID кошелька",
                            "hint": "Используйте формат: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                            "example": "123e4567-e89b-12d3-a456-426614174000",
                            "received": str(error.get("input", "")),
                        },
                    )
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    return app
