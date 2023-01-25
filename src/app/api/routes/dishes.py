from fastapi import APIRouter, HTTPException, status
from src.app.api.schemas import DishBase, DishDb
from src.app.db.models import Base, Submenu, Dish
from src.app.db.database import db, engine
from uuid import UUID

Base.metadata.create_all(bind=engine)

router = APIRouter()


# Get All Dishes
# --------------------------------------------------------------------
@router.get('/',
            response_model=list[DishDb],
            status_code=status.HTTP_200_OK)
def get_all_dishes():
    dishes = db.query(Dish).all()

    if dishes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dishes not found")

    return dishes


# Create Dish
# --------------------------------------------------------------------
@router.post('/',
             response_model=DishDb,
             status_code=status.HTTP_201_CREATED)
def create_dish(submenu_id: UUID, dish: DishBase):
    submenu = db.query(Submenu).get(submenu_id)

    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no submenu with id: {submenu_id}")

    new_dish = Dish(
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id
    )

    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)

    return new_dish


# Get Dish
# --------------------------------------------------------------------
@router.get('/{dish_id}',
            response_model=DishDb,
            status_code=status.HTTP_200_OK)
def get_dish(dish_id: UUID):
    dish = db.query(Dish).get(dish_id)

    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found")

    dish.price = dish.price

    return dish


# Update Dish
# --------------------------------------------------------------------
@router.patch('/{dish_id}',
              response_model=DishDb,
              status_code=status.HTTP_200_OK)
def update_dish(dish_id: UUID, dish: DishBase):
    dish_update = db.query(Dish).get(dish_id)

    if dish_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found")

    dish_update.title = dish.title
    dish_update.description = dish.description
    dish_update.price = dish.price

    db.commit()
    db.refresh(dish_update)

    return dish_update


# Delete Dish
# --------------------------------------------------------------------
@router.delete('/{dish_id}',
               status_code=status.HTTP_200_OK)
def delete_dish(dish_id: UUID):
    dish_to_delete = db.query(Dish).get(dish_id)

    if dish_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found")

    db.delete(dish_to_delete)
    db.commit()

    return {
        "status": 'true',
        "message": "The dish has been deleted"
    }
