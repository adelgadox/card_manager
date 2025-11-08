# Card Manager API Documentation

This document describes all available API endpoints, request parameters, and response formats for the Card Manager application.

## Base URL

```
http://127.0.0.1:5000
```

## Endpoints Overview

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Dashboard | No |
| GET | `/add_card` | Card form | No |
| POST | `/add_card` | Create card | No |
| GET | `/add_transaction` | Transaction form | No |
| POST | `/add_transaction` | Create transaction | No |
| GET | `/transactions` | List transactions | No |
| POST | `/delete_card/<id>` | Delete card | No |

---

## Dashboard

### GET `/`

Returns the main dashboard with all cards and monthly statistics.

**Response**: HTML page displaying:
- List of all cards with current balances
- Monthly statistics (income, expenses, savings)
- Color-coded indicators

**Example**:
```
GET http://127.0.0.1:5000/
```

---

## Card Management

### GET `/add_card`

Displays the form to add a new card.

**Response**: HTML page with card creation form

**Example**:
```
GET http://127.0.0.1:5000/add_card
```

### POST `/add_card`

Creates a new debit or credit card.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Card name (max 100 chars) |
| card_type | string | Yes | "debit" or "credit" |
| balance | float | Yes | Initial balance/debt |

**Example Request**:
```http
POST /add_card HTTP/1.1
Content-Type: application/x-www-form-urlencoded

name=Chase+Checking&card_type=debit&balance=1000.00
```

**Success Response**:
- **Code**: 302 (Redirect)
- **Redirect**: `/` (Dashboard)

**Validation**:
- `name` must not be empty
- `card_type` must be "debit" or "credit"
- `balance` must be a valid number

---

## Transaction Management

### GET `/add_transaction`

Displays the form to add a new transaction.

**Response**: HTML page with transaction form
- Includes list of available cards
- Pre-filled with today's date

**Example**:
```
GET http://127.0.0.1:5000/add_transaction
```

### POST `/add_transaction`

Creates a new income or expense transaction.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| card_id | integer | Yes | ID of the card to use |
| transaction_type | string | Yes | "income" or "expense" |
| amount | float | Yes | Transaction amount |
| description | string | Yes | Transaction description (max 200 chars) |
| category | string | Yes | Transaction category |
| date | string | Yes | Date in YYYY-MM-DD format |

**Available Categories**:
- Food & Dining
- Shopping
- Transportation
- Bills & Utilities
- Entertainment
- Healthcare
- Salary
- Business
- Investment
- Other

**Example Request**:
```http
POST /add_transaction HTTP/1.1
Content-Type: application/x-www-form-urlencoded

card_id=1&transaction_type=expense&amount=50.00&description=Grocery+Shopping&category=Food+%26+Dining&date=2024-01-15
```

**Success Response**:
- **Code**: 302 (Redirect)
- **Redirect**: `/` (Dashboard)

**Balance Update Logic**:

**Debit Card**:
- Income: `balance = balance + amount`
- Expense: `balance = balance - amount`

**Credit Card**:
- Income: `balance = balance - amount` (payment reduces debt)
- Expense: `balance = balance + amount` (expense increases debt)

---

### GET `/transactions`

Retrieves all transactions sorted by date (most recent first).

**Response**: HTML page displaying:
- Transaction date
- Associated card name
- Transaction type (income/expense)
- Category
- Description
- Amount

**Example**:
```
GET http://127.0.0.1:5000/transactions
```

---

## Card Deletion

### POST `/delete_card/<id>`

Deletes a specific card and all associated transactions.

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Card ID to delete |

**Example Request**:
```http
POST /delete_card/1 HTTP/1.1
```

**Success Response**:
- **Code**: 302 (Redirect)
- **Redirect**: `/` (Dashboard)

**Error Response**:
- **Code**: 404
- **Description**: Card not found

**Note**: This operation is permanent and will also delete all transactions associated with this card (CASCADE DELETE).

---

## Data Models

### Card

```python
{
    "id": int,
    "name": str,           # max 100 characters
    "card_type": str,      # "debit" or "credit"
    "balance": float       # current balance or debt
}
```

### Transaction

```python
{
    "id": int,
    "card_id": int,                # foreign key to Card
    "transaction_type": str,       # "income" or "expense"
    "amount": float,
    "description": str,            # max 200 characters
    "category": str,               # max 50 characters
    "date": datetime               # transaction date
}
```

---

## Error Handling

The application uses Flask's default error handling. Common errors:

### 404 Not Found
Returned when accessing a non-existent resource (e.g., invalid card ID).

### 500 Internal Server Error
Returned when there's a server-side error (e.g., database issues).

### Form Validation Errors
Missing or invalid form data will result in browser-side validation errors before submission.

---

## Monthly Statistics Calculation

The dashboard calculates monthly statistics using the following logic:

```python
# Group transactions by month (YYYY-MM)
# For each month:
monthly_stats = {
    'income': sum(transactions where type='income'),
    'expenses': sum(transactions where type='expense'),
    'savings': income - expenses
}
```

---

## Response Formats

All endpoints return HTML responses rendered using Jinja2 templates. The application does not currently provide JSON API responses.

For programmatic access, consider:
1. Parsing HTML responses
2. Direct database access
3. Extending the application with JSON endpoints

---

## Rate Limiting

Currently, there are no rate limits implemented. For production use, consider adding:
- Request throttling
- User authentication
- API keys

---

## Future API Enhancements

Planned improvements:
- [ ] RESTful JSON API endpoints
- [ ] API authentication (JWT tokens)
- [ ] Pagination for large transaction lists
- [ ] Filtering and search capabilities
- [ ] Bulk operations
- [ ] Export endpoints (CSV, PDF)

---

## Examples

### Complete Workflow Example

1. **Add a debit card**:
```http
POST /add_card
name=My Checking&card_type=debit&balance=5000.00
```

2. **Add income**:
```http
POST /add_transaction
card_id=1&transaction_type=income&amount=3000.00&description=Monthly Salary&category=Salary&date=2024-01-01
```

3. **Add expense**:
```http
POST /add_transaction
card_id=1&transaction_type=expense&amount=150.00&description=Groceries&category=Food & Dining&date=2024-01-05
```

4. **View all transactions**:
```http
GET /transactions
```

5. **Check dashboard**:
```http
GET /
```

---

## Notes

- All POST requests should include `Content-Type: application/x-www-form-urlencoded`
- Dates must be in `YYYY-MM-DD` format
- Decimal amounts are supported (e.g., 123.45)
- Database changes are committed immediately
- No undo functionality currently available

---

For more information, see the [main README](../README.md) or visit the [GitHub repository](https://github.com/adelgadox/card_manager).
