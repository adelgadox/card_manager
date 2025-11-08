# Card Manager - Personal Finance Web Application

A comprehensive web application to manage credit and debit cards, track transactions, and monitor your monthly savings. Built with Python Flask and modern web technologies.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Features

### Card Management
- Register unlimited debit and credit cards
- Set initial balances for each card
- View real-time balance updates
- Delete cards when no longer needed

### Transaction Tracking
- **Income transactions**: Salary, business income, investments, etc.
- **Expense transactions**: Food, shopping, bills, transportation, etc.
- Automatic balance calculations:
  - **Debit cards**: Expenses reduce balance, income increases it
  - **Credit cards**: Expenses add to debt, income payments reduce it
- Rich transaction details:
  - Description
  - Amount (supports decimals)
  - Category
  - Date

### Financial Dashboard
- Monthly statistics breakdown:
  - Total Income
  - Total Expenses
  - Net Savings (Income - Expenses)
- Color-coded savings indicators (positive/negative)
- Chronological view by month
- Complete transaction history with filters

### User Experience
- Clean, modern, responsive design
- Mobile-friendly interface
- Intuitive navigation
- Color-coded card types
- Real-time validation

## Screenshots

### Dashboard
The main dashboard displays all your cards with current balances and monthly financial statistics.

### Add Card
Simple form to register new debit or credit cards with initial balances.

### Add Transaction
Easy-to-use interface for recording income and expenses with category selection.

### Transaction History
Comprehensive view of all transactions sorted by date with full details.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Setup Steps

1. **Clone the repository** (or download the source code):
```bash
git clone https://github.com/adelgadox/card_manager.git
cd card_manager
```

2. **Create a virtual environment** (recommended):
```bash
python3 -m venv venv
```

3. **Activate the virtual environment**:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Application

1. **Start the Flask development server**:
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://127.0.0.1:5000
```

3. **Stop the server** by pressing `Ctrl+C` in the terminal.

### Production Deployment

For production environments, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn app:app
```

## Usage Guide

### Adding Your First Card

1. Click **"Add Card"** in the navigation menu
2. Enter card details:
   - **Card Name**: e.g., "Chase Checking", "Visa Credit"
   - **Card Type**: Select "Debit" or "Credit"
   - **Initial Balance**:
     - For debit: Your current account balance
     - For credit: Current debt (use 0 if no debt)
3. Click **"Add Card"**

### Recording Transactions

1. Click **"Add Transaction"** in the navigation menu
2. Select the card to use
3. Choose transaction type:
   - **Income**: Salary, payments received, refunds
   - **Expense**: Purchases, bills, fees
4. Enter amount (decimals supported)
5. Add description and select category
6. Choose the transaction date
7. Click **"Add Transaction"**

### Understanding the Dashboard

**Cards Section:**
- Green cards = Debit cards
- Red cards = Credit cards
- Balance shows current amount

**Monthly Statistics:**
- **Income**: All money received
- **Expenses**: All money spent
- **Savings**: Income - Expenses (green if positive, red if negative)

### How Transactions Affect Balances

**Debit Card:**
- Income (+$100) → Balance increases by $100
- Expense (-$50) → Balance decreases by $50

**Credit Card:**
- Expense (+$100) → Debt increases by $100
- Income/Payment (-$50) → Debt decreases by $50

## Project Structure

```
card_manager/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── test_app.py              # Unit tests
├── .gitignore               # Git ignore rules
├── templates/               # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── index.html          # Dashboard page
│   ├── add_card.html       # Add card form
│   ├── add_transaction.html # Add transaction form
│   └── transactions.html    # Transaction history
├── static/                  # Static files
│   └── css/
│       └── style.css       # Application styles
└── cards.db                 # SQLite database (auto-generated)
```

## Database Schema

### Cards Table
```sql
CREATE TABLE card (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    card_type VARCHAR(20) NOT NULL,  -- 'debit' or 'credit'
    balance FLOAT DEFAULT 0.0
);
```

### Transactions Table
```sql
CREATE TABLE transaction (
    id INTEGER PRIMARY KEY,
    card_id INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,  -- 'income' or 'expense'
    amount FLOAT NOT NULL,
    description VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (card_id) REFERENCES card(id)
);
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard with cards and monthly stats |
| GET | `/add_card` | Display add card form |
| POST | `/add_card` | Create a new card |
| GET | `/add_transaction` | Display add transaction form |
| POST | `/add_transaction` | Create a new transaction |
| GET | `/transactions` | View all transactions |
| POST | `/delete_card/<id>` | Delete a specific card |

## Testing

The project includes comprehensive unit tests covering all major functionality.

### Running Tests

```bash
# Activate virtual environment first
source venv/bin/activate

# Run all tests
pytest test_app.py -v

# Run specific test class
pytest test_app.py::TestAddExpense -v

# Run with coverage report
pytest test_app.py --cov=app
```

### Test Coverage

**18 unit tests** covering:
- ✅ Expense transactions (7 tests)
- ✅ Income transactions (8 tests)
- ✅ Combined transactions (3 tests)

**Test scenarios:**
- Balance updates for debit and credit cards
- Decimal amount handling
- Multiple transactions cumulative effects
- Different transaction categories
- Edge cases (overdraft, overpayment, full payment)

All tests use in-memory database to avoid side effects.

## Technologies Used

### Backend
- **Python 3** - Programming language
- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM for database operations
- **SQLite** - Lightweight database

### Frontend
- **HTML5** - Structure and markup
- **CSS3** - Styling and animations
- **Jinja2** - Template engine

### Testing
- **pytest 9.0.0** - Testing framework

### Development Tools
- **Git** - Version control
- **Virtual Environment (venv)** - Dependency isolation

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write unit tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

## Roadmap

Future enhancements planned:
- [ ] User authentication and multi-user support
- [ ] Data export (CSV, PDF)
- [ ] Budget planning and alerts
- [ ] Recurring transaction support
- [ ] Charts and visualizations
- [ ] Mobile app
- [ ] API for third-party integrations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created with [Claude Code](https://claude.com/claude-code)

## Support

For issues, questions, or contributions, please visit:
- **GitHub Repository**: https://github.com/adelgadox/card_manager
- **Issue Tracker**: https://github.com/adelgadox/card_manager/issues

---

**Note**: This is a development/educational project. For production use with real financial data, implement proper security measures including user authentication, HTTPS, and data encryption.
