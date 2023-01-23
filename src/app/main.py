from fastapi import FastAPI
from app.api import menus  # , submenus, dishes
from app.db.database import database, engine
from app.db.database import SessionLocal

app = FastAPI()

db = SessionLocal()

# @app.on_event("startup")
# def startup():
#     database.connect()
#
#
# @app.on_event("shutdown")
# def shutdown():
#     database.disconnect()


app.include_router(menus.router, prefix=f"/menus", tags=["menus"])
# app.include_router(submenus.router, prefix=f"/menus", tags=["submenus"])
# app.include_router(dishes.router, prefix=f"/menus", tags=["submenus"])

# app.include_router(menus.router, prefix=f"/menus", tags=["menus"])
# app.include_router(submenus.router, prefix=f"/menus/{menu_id}/submenus", tags=["submenus"])
# app.include_router(dishes.router, prefix=f"/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["submenus"])
