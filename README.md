# Payment Methods API

A mock API for managing user payment methods, supporting both credit cards and MPESA wallets.

## Features

- Get all payment methods for a user
- Get default payment method
- Set default payment method
- Delete a payment method

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd disapamock
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the development server:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Charge Recurrent Payment
- **URL**: `/api/recurrent/payment/charge`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "userId": "USER-X",
    "pgCode": "PG_1007",
    "amount": 105.00,
    "currency": "TZS",
    "requestSource": "hypermart",
    "productId": "PROD001",
    "enticementChannel": "SMS",
    "songCode": "SONG_XX",
    "songName": "SONG_POP",
    "artist": "ART_XX"
  }
  ```
- **Required Fields**: `userId`, `amount`, `currency`, `productId`
- **Optional Fields**: `requestSource` (default: "hypermart"), `pgCode`, `enticementChannel`, `songCode`, `songName`, `artist`
- **### Response Status

Possible values for the `status` field in the response:

| Status | Description |
|--------|-------------|
| PENDING | Payment has been initiated but not yet processed |
| PROCESSING | Payment is currently being processed |
| COMPLETED | Payment was successfully processed |
| FAILED | Payment processing failed |
| DECLINED | Payment was declined by the payment gateway |
| REFUNDED | Payment was refunded to the customer |
| PARTIALLY_REFUNDED | Only part of the payment was refunded |
| CANCELLED | Payment was cancelled before completion |
| EXPIRED | Payment link or authorization expired |
| AUTHORIZED | Payment is authorized but not yet captured |
| VOIDED | Authorization was voided before completion |

### Response
  ```json
  {
    "success": true,
    "message": "Recurrent payment processed successfully",
    "data": {
      "transactionId": "TXN12345678",
      "userId": "USER-X",
      "amount": 105.00,
      "currency": "TZS",
      "productId": "PROD001",
      "status": "COMPLETED", /* Possible values: PENDING, PROCESSING, COMPLETED, FAILED, DECLINED, 
                              REFUNDED, PARTIALLY_REFUNDED, CANCELLED, EXPIRED, 
                              AUTHORIZED, VOIDED */
      "timestamp": "2025-05-24T12:00:00Z",
      "metadata": {
        "requestSource": "hypermart",
        "pgCode": "PG_1007",
        "enticementChannel": "SMS",
        "songCode": "SONG_XX",
        "songName": "SONG_POP",
        "artist": "ART_XX"
      }
    }
  }
  ```

### 2. Get All Payment Methods
- **URL**: `/api/users/{userId}/payment-methods`
- **Method**: `GET`
- **Response**: List of all payment methods for the user

### 2. Get Default Payment Method
- **URL**: `/api/users/{userId}/payment-methods/default`
- **Method**: `GET`
- **Response**: Default payment method details

### 3. Set Default Payment Method
- **URL**: `/api/users/{userId}/payment-methods/default`
- **Method**: `PATCH`
- **Body**:
  ```json
  {
    "type": "creditcard" | "mpesa",
    "id": "<payment-method-id>"
  }
  ```
- **Response**: Success/error message

### 4. Delete Payment Method
- **URL**: `/api/users/{userId}/payment-methods/{methodId}`
- **Method**: `DELETE`
- **Response**: Success/error message

## Testing

### Using Postman
1. Import the `Payment_Methods_API.postman_collection.json` file into Postman
2. The collection includes all available endpoints including the new Recurrent Payment Charge
3. Make sure to update any variables (like `userId`) in the Postman environment if needed

### Using cURL

#### Charge Recurrent Payment
```bash
curl -X POST http://localhost:5000/api/recurrent/payment/charge \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "USER-X",
    "pgCode": "PG_1007",
    "amount": 105.00,
    "currency": "TZS",
    "requestSource": "hypermart",
    "productId": "PROD001",
    "enticementChannel": "SMS",
    "songCode": "SONG_XX",
    "songName": "SONG_POP",
    "artist": "ART_XX"
  }'
```

#### Other Endpoints

#### Get All Payment Methods
1. Import the `Payment_Methods_API.postman_collection.json` file into Postman
2. Make sure the API server is running
3. Execute the requests from the collection

### Using cURL

#### Get All Payment Methods
```bash
curl http://localhost:5000/api/users/1/payment-methods
```

#### Get Default Payment Method
```bash
curl http://localhost:5000/api/users/1/payment-methods/default
```

#### Set Default Payment Method
```bash
curl -X PATCH http://localhost:5000/api/users/1/payment-methods/default \
  -H "Content-Type: application/json" \
  -d '{"type": "creditcard", "id": "c073669a-4ee7-49c1-8a3d-924bc19d8ee9"}'
```

#### Delete Payment Method
```bash
curl -X DELETE http://localhost:5000/api/users/1/payment-methods/c073669a-4ee7-49c1-8a3d-924bc19d8ee9
```

## Sample Data

By default, the API comes with sample data for user ID "1" including:
- 2 credit cards (one set as default)
- 1 MPESA wallet (default)

## License

This project is licensed under the MIT License.
