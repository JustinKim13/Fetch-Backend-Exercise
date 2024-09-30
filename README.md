# Fetch Backend Internship Challenge

This is a Flask-based REST API that allows you to add points, spend points, and retrieve a user's point balance by payer.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JustinKim13/Fetch-Backend-Exercise.git`
   ```
3. Move into the correct directory:
   ```bash
   cd fetch-backend-exercise`
   ```
5. Install the required dependencies:
6. ```bash
   pip install -r requirements.txt`
   ```
7. Run the app:
8. ```bash
   python app.py`
   ```

The app will start on port 8000 by default.

## API Endpoints to Check

### 1. Add Points
**Route**: `/add`  
**Method**: `POST`

Example Request:
`{
    "payer": "DANNON",
    "points": 1000,
    "timestamp": "2020-11-02T14:00:00Z"
}`

This request will add 1000 points from the payer **DANNON** with the timestamp specified, and should return a status code of 200.

### 2. Spend Points
**Route**: `/spend`  
**Method**: `POST`

Example Request:
`{
    "points": 5000
}`

This request will attempt to spend 5000 points, starting with the oldest points first, and will return a breakdown of how many points were deducted from each payer.

Example Response:
`[
    { "payer": "DANNON", "points": -1000 },
    { "payer": "MILLER COORS", "points": -4000 }
]`

### 3. Get Points Balance
**Route**: `/balance`  
**Method**: `GET`

Example Response:
`{
    "DANNON": 1000,
    "UNILEVER": 0,
    "MILLER COORS": 5300
}`

This request will return the current balance of points by payer. No JSON request needed, as this is a GET request.

