# Card Manager - Personal Finance Web Application

A web application to manage credit and debit cards, track transactions, and monitor your monthly savings.

## Features

- Register debit and credit cards with initial balances
- Add income and expense transactions
- Automatic balance updates:
  - **Debit cards**: Expenses reduce balance, income increases it
  - **Credit cards**: Expenses add to debt, income payments reduce it
- Transaction tracking with description, date, and category
- Monthly dashboard showing income, expenses, and savings
- Full transaction history

## Installation

1. Navigate to the project directory:
```bash
cd card_manager
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and go to:
```
http://127.0.0.1:5000
```

## Usage

1. **Add a Card**: Click "Add Card" and enter card details (name, type, initial balance)
2. **Add Transaction**: Click "Add Transaction" to record income or expenses
3. **View Dashboard**: The home page shows all your cards and monthly statistics
4. **View Transactions**: Click "Transactions" to see your complete transaction history

## Database

The application uses SQLite database (`cards.db`) which is automatically created on first run.

## Technologies Used

- Python 3
- Flask
- SQLAlchemy
- SQLite
- HTML5
- CSS3
