from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# data = {
#     'title': 'Test title menu',
#     'description': 'Test description menu',
# }
#
#
# def test_get_all_menus():
#     responce = client.get('/')
#     assert responce.status_code == 200


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
