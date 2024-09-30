import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # add our parent directory for proper path

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_points(client):
    # as per directions
    transactions = [
        { "payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" },
        { "payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z" },
        { "payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z" },
        { "payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z" },
        { "payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z" }
    ]

    # run post request for each (/add) and make sure they all give 200 status codes
    for transaction in transactions:
        response = client.post('/add', json=transaction)
        assert response.status_code == 200

# now we can test spending our points we added
def test_spend_points(client):
    response = client.post('/spend', json={ "points": 5000 }) # spend 5000
    assert response.status_code == 200 # make sure it's still 200
    
    expected_spend_response = [ # here's our expected result of which we will compare our actual to
        { "payer": "DANNON", "points": -100 },
        { "payer": "UNILEVER", "points": -200 },
        { "payer": "MILLER COORS", "points": -4700 }
    ]
    
    spend_data = response.get_json()
    assert spend_data == expected_spend_response # check if they're the same

# lets also test checking our balance after spending
def test_get_balance(client):
    response = client.get('/balance')
    data = response.get_json()

    expected_balance = { # expected to compare to
        "DANNON": 1000,
        "UNILEVER": 0,
        "MILLER COORS": 5300
    }

    assert data == expected_balance # shouldl be the same
