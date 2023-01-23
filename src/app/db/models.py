from app.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import String, Float, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                index=True,
                default=uuid.uuid4())

    title = Column(String, index=True)
    description = Column(String, index=True)

    submenus = relationship('Submenu',
                            backref='menu',
                            cascade='all, delete-orphan')


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                index=True,
                default=uuid.uuid4())

    title = Column(String, index=True)
    description = Column(String, index=True)

    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))

    dishes = relationship('Dish',
                          backref='submenu',
                          cascade='all, delete-orphan')


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                index=True,
                default=uuid.uuid4())

    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)

    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
