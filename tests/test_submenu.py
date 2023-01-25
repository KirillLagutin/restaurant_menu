from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# data = {
#     'title': 'Test title submenu',
#     'description': 'Test description submenu',
# }

def test_get_all_submenus():
    responce = client.get('/api/v1/menus/{menu_id}/submenus')
    assert responce.status_code == 200


def test_create_submenu():
    responce = client.post('/api/v1/menus/{menu_id}/submenus')
    assert responce.status_code == 404


def test_get_submenu():
    responce = client.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert responce.status_code == 404


def test_update_submenu():
    responce = client.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert responce.status_code == 404


def test_delete_submenu():
    responce = client.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert responce.status_code == 404
