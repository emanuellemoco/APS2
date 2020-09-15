from fastapi.testclient import TestClient
from main import app


uuid_ = 0

client = TestClient(app)
def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_create_task():
    response = client.post(
        "/task",
        json={ "description" : "uwu", "completed"   : "false"},
        )

    assert response.status_code == 200
    global uuid_
    uuid_ =  response.json()
    assert response.json() != {}

def test_read_task_by_id():
    response = client.get(
        "/task/{uuid_}",
    )
    assert response.status_code = 200
    assert response.json() != {}
    

    
def test_read_task_all():
    response = client.get('/task')
    
    assert resposnse.status_code == 200


def test_read_task_true():
    response = client.get(
        '/task',json={
        "completed" : "True"},
    )

    assert response.status_code = 200
    assert
    

def test_read_task_false():

def test_replace_task():

def test_alters_task():
