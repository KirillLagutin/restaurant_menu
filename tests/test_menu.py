from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# data = {
#     'title': 'Test title menu',
#     'description': 'Test description menu',
# }

def test_get_all_menus():
    responce = client.get('/api/v1/menus')
    assert responce.status_code == 200


def test_create_menu():
    responce = client.post('/api/v1/menus')
    assert responce.status_code == 404


def test_get_menu():
    responce = client.get('/api/v1/menus/{menu_id}')
    assert responce.status_code == 404


def test_update_menu():
    responce = client.patch('/api/v1/menus/{menu_id}')
    assert responce.status_code == 404


def test_delete_menu():
    responce = client.delete('/api/v1/menus/{menu_id}')
    assert responce.status_code == 404
