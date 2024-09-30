import sys
import os
import pytest

# Add the parent directory to the system path so that `app` can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test adding all the required transactions
def test_add_points(client):
    # Adding points as per the challenge
    transactions = [
        { "payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" },
        { "payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z" },
        { "payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z" },
        { "payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z" },
        { "payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z" }
    ]

    # Post each transaction and check status
    for transaction in transactions:
        response = client.post('/add', json=transaction)
        assert response.status_code == 200

# Test spending points and checking if the balance is correct
def test_spend_points(client):
    # Spend 5000 points
    response = client.post('/spend', json={ "points": 5000 })
    assert response.status_code == 200
    
    # Expected response from the spend operation
    expected_spend_response = [
        { "payer": "DANNON", "points": -100 },
        { "payer": "UNILEVER", "points": -200 },
        { "payer": "MILLER COORS", "points": -4700 }
    ]
    
    # Check if the spend response is as expected
    spend_data = response.get_json()
    assert spend_data == expected_spend_response

# Test getting the correct balance after the transactions
def test_get_balance(client):
    # Check the balance
    response = client.get('/balance')
    data = response.get_json()

    # Expected final balance after spending
    expected_balance = {
        "DANNON": 1000,
        "UNILEVER": 0,
        "MILLER COORS": 5300
    }

    # Check if balance is correct
    assert data == expected_balance
