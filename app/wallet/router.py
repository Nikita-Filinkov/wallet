from uuid import UUID

from fastapi import APIRouter, Depends

from app.exceptions import DontHaveThisWallet, NotEnoughFunds
from app.users.dependencies import get_current_user
from app.users.shemas import UserShortResponse
from app.wallet.service import WalletsService
from app.wallet.shemas import SChangeBalance, SWalletBalance

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.patch("/{wallet_uuid}", response_model=SWalletBalance)
async def change_balance(
    wallet_uuid: UUID,
    operation_data: SChangeBalance,
    current_user: UserShortResponse = Depends(get_current_user),
) -> SWalletBalance:

    if operation_data.operation_type == "deposit":
        result = await WalletsService.deposit_balance(
            wallet_uuid=wallet_uuid, amount=operation_data.amount
        )
        if result is None:
            raise NotEnoughFunds
        return result
    elif operation_data.operation_type == "withdraw":
        if wallet_uuid in current_user.wallets:
            result = await WalletsService.withdraw_balance(
                wallet_uuid=wallet_uuid, amount=operation_data.amount
            )
        else:
            raise DontHaveThisWallet
        return result


@router.get("/{wallet_uuid}", response_model=SWalletBalance)
async def get_balance(
    wallet_uuid: UUID, current_user: UserShortResponse = Depends(get_current_user)
) -> SWalletBalance:
    if wallet_uuid in current_user.wallets:
        wallet = await WalletsService.find_one_or_none(wallet_uuid=wallet_uuid)
        return SWalletBalance(
            wallet_uuid=wallet.wallet_uuid,
            balance=wallet.balance,
            updated_at=wallet.updated_at,
        )
    else:
        raise DontHaveThisWallet
