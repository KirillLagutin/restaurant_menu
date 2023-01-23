from fastapi import APIRouter, HTTPException, status
from app.api.schemas import MenuBase, SubmenuBase, DishBase
from app.db.models import Menu, Submenu, Dish
from main import db
from uuid import UUID
import uuid

router = APIRouter()


# Get All Menus
# --------------------------------------------------------------------
@router.get('/',
            response_model=list[MenuBase],
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
@router.post('/',
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
@router.get('/{menu_id}',
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
@router.patch('/{menu_id}',
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
@router.delete('/{menu_id}',
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
