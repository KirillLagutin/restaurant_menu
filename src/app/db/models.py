from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


# Menu
# --------------------------------------------------------------------
class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                # index=True,
                default=uuid.uuid4())

    title = Column(String(30))
    description = Column(String(90))

    submenus = relationship("Submenu",
                            backref="menu",
                            cascade="all, delete-orphan")


# Submenu
# --------------------------------------------------------------------
class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                index=True,
                default=uuid.uuid4())

    title = Column(String(30), index=True)
    description = Column(String(90), index=True)

    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))

    dishes = relationship('Dish',
                          backref='submenu',
                          cascade='all, delete-orphan')


# Dish
# --------------------------------------------------------------------
class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                index=True,
                default=uuid.uuid4())

    title = Column(String(30), index=True)
    description = Column(String(90), index=True)
    price = Column(Float(2), index=True)

    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
