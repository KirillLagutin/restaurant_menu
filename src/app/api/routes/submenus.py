from fastapi import APIRouter, HTTPException, status
from app.api.schemas import SubmenuBase, SubmenuDb
from app.db.models import Base, Menu, Submenu, Dish
from app.db.database import db, engine
from uuid import UUID

Base.metadata.create_all(bind=engine)

router = APIRouter()


# Get All Submenus
# --------------------------------------------------------------------
@router.get('/',
            response_model=list[SubmenuDb],
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
             response_model=SubmenuDb,
             status_code=status.HTTP_201_CREATED)
def create_submenu(menu_id: UUID, submenu: SubmenuBase):
    menu = db.query(Menu).get(menu_id)

    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no menu with id: {menu_id}")

    new_submenu = Submenu(
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
@router.get('/{submenu_id}',
            response_model=SubmenuDb,
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
              response_model=SubmenuDb,
              status_code=status.HTTP_200_OK)
def update_submenu(submenu_id: UUID, submenu: SubmenuBase):
    submenu_update = db.query(Submenu).get(submenu_id)

    if submenu_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found")

    submenu_update.title = submenu.title
    submenu_update.description = submenu.description

    db.commit()
    db.refresh(submenu_update)

    return submenu_update


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
