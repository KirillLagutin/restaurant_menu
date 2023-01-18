from src.db.database import Base, engine
from src.models.models import Menu, Submenu, Dish

print("Creating database ....")

Base.metadata.create_all(engine)
