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
        json={ "description" : "uwu", "completed"   : "true"})
    assert response.status_code == 200
    global uuid_
    uuid_ =  response.json()
    assert response.json() != {}

def test_read_task_by_id():
    req = "/task/" + uuid_
    response = client.get(req)
     
    assert response.status_code == 200
    assert response.json() != {}
    
      
def test_read_all_task():
    response = client.get('/task')
    assert response.status_code == 200


def test_read_true_task():
    response = client.get(
        '/task?completed=true')
    tasks = response.json()
    for task in tasks:
        print(tasks[task])
        assert tasks[task]["completed"] == True

    assert response.status_code == 200


def test_read_false_task():
    response = client.get(
        '/task?completed=false')
    tasks = response.json()
    for task in tasks:
        print(tasks[task])
        assert tasks[task]["completed"] == False

    assert response.status_code == 200


def test_replace_task():
    req = "/task/" + uuid_
    response = client.put(req, json={"description": "Replacing a task", "completed": "true"})
    
    assert response.status_code == 200
    

def test_alters_task():
    req = "/task/" + uuid_
    response = client.patch(req, json={"description": "Altering a task", "completed": "true"})
    
    assert response.status_code == 200
    

def test_delete_task_by_id():
    req = "/task/" + uuid_
    response = client.delete(req)
    
    assert response.status_code == 200