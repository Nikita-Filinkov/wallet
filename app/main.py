from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from app.exceptions import add_validation_exception_handler
from app.users.router import router as router_users
from app.wallet.router import router as router_wallet

app = FastAPI()
app.include_router(router_users)
app.include_router(router_wallet)
add_validation_exception_handler(app)

app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
)


@app.get("/api")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}
