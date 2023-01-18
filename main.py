from fastapi import FastAPI, status, HTTPException
from src.db.database import SessionLocal
from src.schemas.schemas import MenuBase, SubmenuBase, DishBase
from typing import List
from uuid import UUID
import uuid
from src.models.models import Menu, Submenu, Dish

app = FastAPI()
db = SessionLocal()

URI = '/api/v1/menus'


######################################################################
###############################  MENU  ###############################
######################################################################

# Get All Menus
# --------------------------------------------------------------------
@app.get(URI,
         response_model=List[MenuBase],
         status_code=status.HTTP_200_OK)
def get_all_menus():
    menus = db.query(Menu).all()

    if menus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menus not found")

    for menu in menus:
        menu.submenus_count = db.query(
            Menu.id == Submenu.menu_id).count()

    return menus


# Create Menu
# --------------------------------------------------------------------
@app.post(URI,
          response_model=MenuBase,
          status_code=status.HTTP_201_CREATED)
def create_menu(menu: MenuBase):
    new_menu = Menu(
        id=uuid.uuid4(),
        title=menu.title,
        description=menu.description,
    )

    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)

    return new_menu


# Get Menu
# --------------------------------------------------------------------
@app.get(URI + '/{menu_id}',
         response_model=MenuBase,
         status_code=status.HTTP_200_OK)
def get_menu(menu_id: UUID):
    menu = db.query(Menu).get(menu_id)

    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found")

    menu.submenus_count = db.query(
        Submenu.menu_id == menu_id).count()

    menu.dishes_count = db.query(
        Dish.submenu_id == Submenu.id).where(
        Submenu.menu_id == menu_id).count()

    return menu


# Update Menu
# --------------------------------------------------------------------
@app.patch(URI + '/{menu_id}',
           response_model=MenuBase,
           status_code=status.HTTP_200_OK)
def update_menu(menu_id: UUID, menu: MenuBase):
    menu_update = db.query(Menu).get(menu_id)

    if menu_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found")

    menu_update.title = menu.title
    menu_update.description = menu.description

    db.commit()

    return menu


# Delete Menu
# --------------------------------------------------------------------
@app.delete(URI + '/{menu_id}',
            status_code=status.HTTP_200_OK)
def delete_menu(menu_id: UUID):
    menu_to_delete = db.query(Menu).get(menu_id)

    if menu_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found")

    db.delete(menu_to_delete)
    db.commit()

    return {
        "status": 'true',
        "message": "The menu has been deleted"
    }


######################################################################
#############################  SUBMENU  ##############################
######################################################################

# Get All Submenus
# --------------------------------------------------------------------
@app.get(URI + '/{menu_id}/submenus',
         response_model=List[SubmenuBase],
         status_code=status.HTTP_200_OK)
def get_all_submenus():
    submenus = db.query(Submenu).all()

    if submenus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenus not found")

    return submenus


# Create Submenu
# --------------------------------------------------------------------
@app.post(URI + '/{menu_id}/submenus',
          response_model=SubmenuBase,
          status_code=status.HTTP_201_CREATED)
def create_submenu(menu_id: UUID, submenu: SubmenuBase):
    new_submenu = Submenu(
        id=uuid.uuid4(),
        title=submenu.title,
        description=submenu.description,
        menu_id=menu_id
    )

    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)

    return new_submenu


# Get Submenu
# --------------------------------------------------------------------
@app.get(URI + '/{menu_id}/submenus/{submenu_id}',
         response_model=SubmenuBase,
         status_code=status.HTTP_200_OK)
def get_submenu(submenu_id: UUID):
    submenu = db.query(Submenu).get(submenu_id)

    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found")

    submenu.dishes_count = db.query(
        Dish.submenu_id ==
        Submenu.id).count()

    return submenu


# Update Submenu
# --------------------------------------------------------------------
@app.patch(URI + '/{menu_id}/submenus/{submenu_id}',
           response_model=SubmenuBase,
           status_code=status.HTTP_200_OK)
def update_submenu(submenu_id: UUID, submenu: SubmenuBase):
    submenu_update = db.query(Submenu).get(submenu_id)

    if submenu_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found")

    submenu_update.title = submenu.title
    submenu_update.description = submenu.description

    db.commit()

    return submenu


# Delete Submenu
# --------------------------------------------------------------------
@app.delete(URI + '/{menu_id}/submenus/{submenu_id}',
            status_code=status.HTTP_200_OK)
def delete_submenu(submenu_id: UUID):
    submenu_to_delete = db.query(Submenu).get(submenu_id)

    if submenu_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found")

    db.delete(submenu_to_delete)
    db.commit()

    return {
        "status": 'true',
        "message": "The submenu has been deleted"
    }


######################################################################
###############################  DISH  ###############################
######################################################################

# Get All Dishes
# --------------------------------------------------------------------
@app.get(URI + '/{menu_id}/submenus/{submenu_id}/dishes',
         response_model=List[DishBase],
         status_code=status.HTTP_200_OK)
def get_all_dishes():
    dishes = db.query(Dish).all()

    if dishes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dishes not found")

    return dishes


# Create Dish
# --------------------------------------------------------------------
@app.post(URI + '/{menu_id}/submenus/{submenu_id}/dishes',
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
@app.get(URI + '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
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
@app.patch(URI + '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
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
@app.delete(URI + '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
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
