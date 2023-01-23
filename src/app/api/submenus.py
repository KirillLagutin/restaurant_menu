from fastapi import APIRouter, HTTPException, status
from app.api.schemas import MenuBase, SubmenuBase, DishBase
from app.db.models import Menu, Submenu, Dish
from main import db
from uuid import UUID
import uuid

router = APIRouter()


# Get All Submenus
# --------------------------------------------------------------------
# @app.get(URI + '/{menu_id}/submenus',
@router.get('/',
            response_model=list[SubmenuBase],
            status_code=status.HTTP_200_OK)
def get_all_submenus():
    submenus = db.query(Submenu).all()

    if submenus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenus not found")

    return submenus


# Create Submenu
# --------------------------------------------------------------------
@router.post('/',
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
# @app.get(URI + '/{menu_id}/submenus/{submenu_id}',
@router.get('/{submenu_id}',
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
@router.patch('/{submenu_id}',
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
@router.delete('/{submenu_id}',
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
