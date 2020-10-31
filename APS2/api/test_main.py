from fastapi.testclient import TestClient
from .main import app

uuid_ = 0 

client = TestClient(app)

def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

def test_read_empty_task():
    response = client.get('/task')
    assert response.status_code == 200 
    assert response.json() == {}

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

def test_read_task_by_incorrect_id():
    req = "/task/a8abdc8e-7ded-467b-bcc2-34398593958d"
    response = client.get(req)
    assert response.status_code == 404

def test_read_all_task():
    response = client.get('/task')
    assert response.status_code == 200

def test_read_true_task():
    response = client.get(
        '/task?completed=true')
    tasks = response.json()
    for task in tasks:
        assert tasks[task]["completed"] == True

    assert response.status_code == 200

def test_read_false_task():
    response = client.get(
        '/task?completed=false')
    tasks = response.json()
    for task in tasks:
        assert tasks[task]["completed"] == False

    assert response.status_code == 200


def test_replace_task_by_id():
    req = "/task/" + uuid_
    response = client.put(req, json={"description": "Replacing a task", "completed": "true"})
    
    assert response.status_code == 200

def test_replace_task_by_incorrect_id():
    req = "/task/a8abdc8e-7ded-467b-bcc2-34398593958a"
    response = client.put(req, json={"description": "Replacing a task", "completed": "true"})
    
    assert response.status_code == 404
    

def test_alters_task_by_id():
    req = "/task/" + uuid_
    response = client.patch(req, json={"description": "Altering a task", "completed": "true"})
    
    assert response.status_code == 200

def test_alters_task_by_incorrect_id():
    req = "/task/a8abdc8e-7ded-467b-bcc2-34398593958b"
    response = client.patch(req, json={"description": "Altering a task", "completed": "true"})
    
    assert response.status_code == 404
    

def test_delete_task_by_id():
    req = "/task/" + uuid_
    response = client.delete(req)
    
    assert response.status_code == 200

def test_delete_task_by_incorrect_id():
    req = "/task/a8abdc8e-7ded-467b-bcc2-34398593958c"
    response = client.delete(req)
    
    assert response.status_code == 404


def test_create_multiple_tasks_and_check():
    mock = [
        { "description": "mock1", "completed": True},
        { "description": "mock2", "completed": True},
        { "description": "mock3", "completed": False},
        { "description": "mock4", "completed": False}
        ]   
    ids = []

    #Adiciona o mock no DB
    for item in mock:
        response = client.post("/task",json=item)
        ids.append(response.json())
    
    # Lista todas as tasks 
    response = client.get('/task')
    tasks = response.json()
    
    # Checa se bate o que foi adicionado com o que existe na request
    for i in  range(len(tasks)):
        assert tasks[ids[i]] == mock[i]

    # Deleta todas as tasks adicionadas
    for i in ids:
        req = "/task/" + i
        response = client.delete(req)
        assert response.status_code == 200
    
    # Checa se as tasks estão vazias
    response = client.get("/task")
    assert response.json() == {}
    

