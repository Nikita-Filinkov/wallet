from fastapi import HTTPException, status


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
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = "Число должно быть положительным"


class MoreTowDecimalAfterComma(WalletException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = "Введено больше двух цифр после запятой"


class WrongOperationType(WalletException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = "Тип операции должен быть 'deposit' или 'withdraw'"


class WrongAmount(WalletException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = "Не верный формат ввода 'amount'"


class MaxAmountExceeded(WalletException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = "Введённое число превышает 10000000"
