# Fetch Backend Internship Challenge

This is a Flask-based REST API that implements the functionality outlined in the Fetch Backend Internship Challenge. The API allows you to add points, spend points, and retrieve a user's point balance by payer.

## Installation

1. Clone the repository.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the app:
    ```bash
    python app.py
    ```

The app will start on port 8000.

## API Endpoints

### 1. Add Points
**Route**: `/add`  
**Method**: `POST`

Example Request:
```json
{
    "payer": "DANNON",
    "points": 1000,
    "timestamp": "2020-11-02T14:00:00Z"
}
