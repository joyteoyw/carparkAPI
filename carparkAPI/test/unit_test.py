import pytest
from carparkapi import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# API 1: GET CAR BY ID
def test_get_car_by_id_success(client):
    # Test GET /car/<int: id> with valid car ID
    response = client.get('/car/1')
    assert response.status_code == 200   
    assert response.json['response'] == "success"

def test_get_car_by_id_not_found(client):
    # Test GET /car/<int: id> with invalid car ID
    response = client.get('/car/999999')  
    assert response.status_code == 404
    assert response.json['response'] == "error"

# API 2: ADD NEW CAR
def test_add_car_success(client):
    new_car = {
        "id": 9999,
        "model": "Tesla Model X",
        "colour": "White",
        "lot": 9999
    }
    response = client.post('/car/add', json=new_car)
    assert response.status_code == 201
    assert response.json['response'] == "success"
    assert response.json['data']['id'] == 9999

def test_add_car_existing_car(client):
    new_car = {
        "id": 9999,
        "model": "Tesla Model X",
        "colour": "White",
        "lot": 8888
    }
    response = client.post('/car/add', json=new_car)
    assert response.status_code == 400
    assert response.json['response'] == "error"
    assert response.json['error'] == "Car with ID 9999 already exists."

def test_add_car_occupied_lot(client):
    new_car = {
        "id": 8888,
        "model": "Tesla Model X",
        "colour": "Yellow",
        "lot": 9999
    }
    response = client.post('/car/add', json=new_car)
    assert response.status_code == 400
    assert response.json['response'] == "error"
    assert response.json['error'] == "Lot 9999 is already occupied."

def test_add_car_missing_value(client):
    new_car = {
        "id": "",
        "model": "Tesla Model X",
        "colour": "Yellow",
        "lot": 9999
    }
    response = client.post('/car/add', json=new_car)
    assert response.status_code == 400
    assert response.json['response'] == "error"
    assert response.json['error'] == "Car must have ID, model, colour, and lot."

def test_add_car_invalid_type(client):
    new_car = {
        "id": "8888",
        "model": "Tesla Model X",
        "colour": "Yellow",
        "lot": 9999
    }
    response = client.post('/car/add', json=new_car)
    assert response.status_code == 400
    assert response.json['response'] == "error"
    assert response.json['error'] == "Car ID must be an Integer value."

# API 3: DELETE CAR
def test_delete_car_success(client):
    response = client.delete('/car/delete/9999')
    assert response.status_code == 200
    assert response.json['response'] == "success"
    assert response.json['message'] == "Car deleted successfully"

def test_delete_car_not_found(client):
    response = client.delete('/car/delete/0')
    assert response.status_code == 404
    assert response.json['response'] == "error"
    assert response.json['error'] == "Car with ID 0 not found."


# ADDITIONAL CONTEXTUAL API (NOT GRADED)
def test_get_car_lots_success(client):
    response = client.get('/car/lots')
    assert response.status_code == 200   
    assert response.json['response'] == "success"