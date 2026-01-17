from app.service.base import BaseService
from app.wallet.models import Wallets


class WalletsService(BaseService):
    model = Wallets
