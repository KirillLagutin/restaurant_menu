from pydantic import BaseModel
from uuid import UUID, uuid4


# Menu
# --------------------------------------------------------------------
class MenuBase(BaseModel):
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0


class MenuDb(MenuBase):
    id: UUID

    class Config:
        orm_mode = True


# Submenu
# --------------------------------------------------------------------
class SubmenuBase(BaseModel):
    title: str
    description: str
    dishes_count: int = 0


class SubmenuDb(SubmenuBase):
    id: UUID

    class Config:
        orm_mode = True


# Dish
# --------------------------------------------------------------------
class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishDb(DishBase):
    id: UUID

    class Config:
        orm_mode = True
