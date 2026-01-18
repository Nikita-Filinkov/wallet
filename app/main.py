from fastapi import FastAPI

from app.users.router import router as router_users
from app.wallet.router import router as router_wallet

app = FastAPI()
app.include_router(router_users)
app.include_router(router_wallet)


@app.get("/api")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}
