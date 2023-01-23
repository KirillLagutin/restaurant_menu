from pydantic import BaseModel
from uuid import UUID
import uuid


class MenuBase(BaseModel):
    id: UUID = uuid.uuid4()
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    id: UUID = uuid.uuid4()
    title: str
    description: str
    dishes_count: int = 0

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    id: UUID = uuid.uuid4()
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
