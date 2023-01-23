from fastapi import APIRouter, HTTPException, status
from app.api.schemas import MenuBase, SubmenuBase, DishBase
from app.db.models import Menu, Submenu, Dish
from main import db
from uuid import UUID
import uuid

router = APIRouter()


# Get All Dishes
# --------------------------------------------------------------------
# @app.get(URI + '/{menu_id}/submenus/{submenu_id}/dishes',
@router.get('/',
            response_model=list[DishBase],
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
             response_model=DishBase,
             status_code=status.HTTP_201_CREATED)
def create_dish(submenu_id: UUID, dish: DishBase):
    new_dish = Dish(
        id=uuid.uuid4(),
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
# @app.get(URI + '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
@router.get('/{dish_id}',
            response_model=DishBase,
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
              response_model=DishBase,
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
