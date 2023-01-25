from fastapi import FastAPI
from app.api.routes import menus, submenus, dishes

app = FastAPI()


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


app.include_router(
    menus.router,
    prefix="/api/v1/menus",
    tags=["menus"])

app.include_router(
    submenus.router,
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=["submenus"])

app.include_router(
    dishes.router,
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["dishes"])
