from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# data = {
#     'title': 'Test title dish',
#     'description': 'Test description dish',
# }

def test_get_all_dish():
    responce = client.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert responce.status_code == 200


def test_create_dish():
    responce = client.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert responce.status_code == 404


def test_get_dish():
    responce = client.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert responce.status_code == 404


def test_update_dish():
    responce = client.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert responce.status_code == 404


def test_delete_dish():
    responce = client.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert responce.status_code == 404
