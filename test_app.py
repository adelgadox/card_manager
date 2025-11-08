import pytest
from datetime import datetime
from app import app, db, Card, Transaction

@pytest.fixture
def client():
    """Create a test client with a temporary database"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def debit_card():
    """Create a debit card with initial balance"""
    card = Card(name='Test Debit Card', card_type='debit', balance=1000.0)
    db.session.add(card)
    db.session.commit()
    return card

@pytest.fixture
def credit_card():
    """Create a credit card with initial balance"""
    card = Card(name='Test Credit Card', card_type='credit', balance=0.0)
    db.session.add(card)
    db.session.commit()
    return card

class TestAddExpense:
    """Unit tests for adding expense transactions"""

    def test_add_expense_to_debit_card_reduces_balance(self, client, debit_card):
        """Test that adding an expense to a debit card reduces its balance"""
        initial_balance = debit_card.balance
        expense_amount = 100.0

        response = client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'expense',
            'amount': expense_amount,
            'description': 'Test Grocery Shopping',
            'category': 'Food & Dining',
            'date': '2024-01-15'
        }, follow_redirects=True)

        # Check response is successful
        assert response.status_code == 200

        # Check that balance was reduced
        updated_card = Card.query.get(debit_card.id)
        assert updated_card.balance == initial_balance - expense_amount
        assert updated_card.balance == 900.0

    def test_add_expense_to_credit_card_increases_balance(self, client, credit_card):
        """Test that adding an expense to a credit card increases its balance (debt)"""
        initial_balance = credit_card.balance
        expense_amount = 200.0

        response = client.post('/add_transaction', data={
            'card_id': credit_card.id,
            'transaction_type': 'expense',
            'amount': expense_amount,
            'description': 'Test Online Shopping',
            'category': 'Shopping',
            'date': '2024-01-15'
        }, follow_redirects=True)

        # Check response is successful
        assert response.status_code == 200

        # Check that balance (debt) increased
        updated_card = Card.query.get(credit_card.id)
        assert updated_card.balance == initial_balance + expense_amount
        assert updated_card.balance == 200.0

    def test_expense_transaction_is_saved_correctly(self, client, debit_card):
        """Test that expense transaction is saved with correct data"""
        response = client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'expense',
            'amount': 50.0,
            'description': 'Test Gas Station',
            'category': 'Transportation',
            'date': '2024-01-20'
        }, follow_redirects=True)

        # Check response is successful
        assert response.status_code == 200

        # Verify transaction was created
        transaction = Transaction.query.filter_by(card_id=debit_card.id).first()
        assert transaction is not None
        assert transaction.transaction_type == 'expense'
        assert transaction.amount == 50.0
        assert transaction.description == 'Test Gas Station'
        assert transaction.category == 'Transportation'
        assert transaction.date.strftime('%Y-%m-%d') == '2024-01-20'

    def test_multiple_expenses_cumulative_effect(self, client, debit_card):
        """Test that multiple expenses have cumulative effect on balance"""
        initial_balance = debit_card.balance

        # Add first expense
        client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'expense',
            'amount': 100.0,
            'description': 'Expense 1',
            'category': 'Food & Dining',
            'date': '2024-01-15'
        })

        # Add second expense
        client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'expense',
            'amount': 150.0,
            'description': 'Expense 2',
            'category': 'Shopping',
            'date': '2024-01-16'
        })

        # Check final balance
        updated_card = Card.query.get(debit_card.id)
        assert updated_card.balance == initial_balance - 100.0 - 150.0
        assert updated_card.balance == 750.0

        # Check both transactions exist
        transactions = Transaction.query.filter_by(card_id=debit_card.id).all()
        assert len(transactions) == 2

    def test_expense_with_different_categories(self, client, debit_card):
        """Test expenses can be added with different categories"""
        categories = ['Food & Dining', 'Shopping', 'Transportation', 'Bills & Utilities', 'Entertainment']

        for i, category in enumerate(categories):
            client.post('/add_transaction', data={
                'card_id': debit_card.id,
                'transaction_type': 'expense',
                'amount': 10.0,
                'description': f'Test {category}',
                'category': category,
                'date': '2024-01-15'
            })

        # Verify all transactions were created
        transactions = Transaction.query.filter_by(card_id=debit_card.id).all()
        assert len(transactions) == 5

        # Verify each category was saved
        saved_categories = [t.category for t in transactions]
        for category in categories:
            assert category in saved_categories

    def test_large_expense_on_debit_card(self, client, debit_card):
        """Test that large expense can reduce balance to negative (overdraft)"""
        large_expense = 1500.0  # More than initial balance

        response = client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'expense',
            'amount': large_expense,
            'description': 'Large Purchase',
            'category': 'Shopping',
            'date': '2024-01-15'
        }, follow_redirects=True)

        assert response.status_code == 200

        # Check balance went negative (overdraft)
        updated_card = Card.query.get(debit_card.id)
        assert updated_card.balance == 1000.0 - 1500.0
        assert updated_card.balance == -500.0

    def test_expense_decimal_amounts(self, client, debit_card):
        """Test that expenses with decimal amounts are handled correctly"""
        response = client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'expense',
            'amount': 25.99,
            'description': 'Coffee Shop',
            'category': 'Food & Dining',
            'date': '2024-01-15'
        }, follow_redirects=True)

        assert response.status_code == 200

        updated_card = Card.query.get(debit_card.id)
        assert updated_card.balance == 1000.0 - 25.99
        assert updated_card.balance == 974.01


class TestAddIncome:
    """Unit tests for adding income transactions"""

    def test_add_income_to_debit_card_increases_balance(self, client, debit_card):
        """Test that adding income to a debit card increases its balance"""
        initial_balance = debit_card.balance
        income_amount = 500.0

        response = client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'income',
            'amount': income_amount,
            'description': 'Monthly Salary',
            'category': 'Salary',
            'date': '2024-01-01'
        }, follow_redirects=True)

        # Check response is successful
        assert response.status_code == 200

        # Check that balance was increased
        updated_card = Card.query.get(debit_card.id)
        assert updated_card.balance == initial_balance + income_amount
        assert updated_card.balance == 1500.0

    def test_add_income_to_credit_card_reduces_balance(self, client, credit_card):
        """Test that adding income (payment) to a credit card reduces its balance (debt)"""
        # First add some debt to the credit card
        credit_card.balance = 500.0
        db.session.commit()

        initial_balance = credit_card.balance
        payment_amount = 200.0

        response = client.post('/add_transaction', data={
            'card_id': credit_card.id,
            'transaction_type': 'income',
            'amount': payment_amount,
            'description': 'Credit Card Payment',
            'category': 'Salary',
            'date': '2024-01-15'
        }, follow_redirects=True)

        # Check response is successful
        assert response.status_code == 200

        # Check that balance (debt) was reduced
        updated_card = Card.query.get(credit_card.id)
        assert updated_card.balance == initial_balance - payment_amount
        assert updated_card.balance == 300.0

    def test_income_transaction_is_saved_correctly(self, client, debit_card):
        """Test that income transaction is saved with correct data"""
        response = client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'income',
            'amount': 750.0,
            'description': 'Freelance Project Payment',
            'category': 'Business',
            'date': '2024-01-10'
        }, follow_redirects=True)

        # Check response is successful
        assert response.status_code == 200

        # Verify transaction was created
        transaction = Transaction.query.filter_by(card_id=debit_card.id).first()
        assert transaction is not None
        assert transaction.transaction_type == 'income'
        assert transaction.amount == 750.0
        assert transaction.description == 'Freelance Project Payment'
        assert transaction.category == 'Business'
        assert transaction.date.strftime('%Y-%m-%d') == '2024-01-10'

    def test_multiple_incomes_cumulative_effect(self, client, debit_card):
        """Test that multiple incomes have cumulative effect on balance"""
        initial_balance = debit_card.balance

        # Add first income
        client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'income',
            'amount': 300.0,
            'description': 'Income 1',
            'category': 'Salary',
            'date': '2024-01-01'
        })

        # Add second income
        client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'income',
            'amount': 200.0,
            'description': 'Income 2',
            'category': 'Business',
            'date': '2024-01-05'
        })

        # Check final balance
        updated_card = Card.query.get(debit_card.id)
        assert updated_card.balance == initial_balance + 300.0 + 200.0
        assert updated_card.balance == 1500.0

        # Check both transactions exist
        transactions = Transaction.query.filter_by(card_id=debit_card.id).all()
        assert len(transactions) == 2

    def test_income_with_different_categories(self, client, debit_card):
        """Test incomes can be added with different categories"""
        categories = ['Salary', 'Business', 'Investment', 'Other']

        for category in categories:
            client.post('/add_transaction', data={
                'card_id': debit_card.id,
                'transaction_type': 'income',
                'amount': 100.0,
                'description': f'Test {category}',
                'category': category,
                'date': '2024-01-15'
            })

        # Verify all transactions were created
        transactions = Transaction.query.filter_by(card_id=debit_card.id).all()
        assert len(transactions) == 4

        # Verify each category was saved
        saved_categories = [t.category for t in transactions]
        for category in categories:
            assert category in saved_categories

    def test_income_decimal_amounts(self, client, debit_card):
        """Test that incomes with decimal amounts are handled correctly"""
        response = client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'income',
            'amount': 1234.56,
            'description': 'Bonus Payment',
            'category': 'Salary',
            'date': '2024-01-15'
        }, follow_redirects=True)

        assert response.status_code == 200

        updated_card = Card.query.get(debit_card.id)
        assert updated_card.balance == 1000.0 + 1234.56
        assert updated_card.balance == 2234.56

    def test_income_pays_off_credit_card_completely(self, client, credit_card):
        """Test that income payment can completely pay off credit card debt"""
        # Set credit card debt
        credit_card.balance = 300.0
        db.session.commit()

        # Pay off entire debt
        response = client.post('/add_transaction', data={
            'card_id': credit_card.id,
            'transaction_type': 'income',
            'amount': 300.0,
            'description': 'Full Payment',
            'category': 'Salary',
            'date': '2024-01-15'
        }, follow_redirects=True)

        assert response.status_code == 200

        # Check balance is now zero
        updated_card = Card.query.get(credit_card.id)
        assert updated_card.balance == 0.0

    def test_income_overpayment_on_credit_card(self, client, credit_card):
        """Test that overpaying a credit card results in negative balance (credit)"""
        # Set credit card debt
        credit_card.balance = 100.0
        db.session.commit()

        # Pay more than debt
        response = client.post('/add_transaction', data={
            'card_id': credit_card.id,
            'transaction_type': 'income',
            'amount': 150.0,
            'description': 'Overpayment',
            'category': 'Salary',
            'date': '2024-01-15'
        }, follow_redirects=True)

        assert response.status_code == 200

        # Check balance is negative (credit on account)
        updated_card = Card.query.get(credit_card.id)
        assert updated_card.balance == 100.0 - 150.0
        assert updated_card.balance == -50.0


class TestCombinedTransactions:
    """Unit tests for combined income and expense transactions"""

    def test_income_and_expense_net_effect_on_debit_card(self, client, debit_card):
        """Test the net effect of income and expenses on debit card balance"""
        initial_balance = debit_card.balance

        # Add income
        client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'income',
            'amount': 500.0,
            'description': 'Salary',
            'category': 'Salary',
            'date': '2024-01-01'
        })

        # Add expense
        client.post('/add_transaction', data={
            'card_id': debit_card.id,
            'transaction_type': 'expense',
            'amount': 200.0,
            'description': 'Shopping',
            'category': 'Shopping',
            'date': '2024-01-05'
        })

        # Check net effect
        updated_card = Card.query.get(debit_card.id)
        expected_balance = initial_balance + 500.0 - 200.0
        assert updated_card.balance == expected_balance
        assert updated_card.balance == 1300.0

    def test_income_and_expense_net_effect_on_credit_card(self, client, credit_card):
        """Test the net effect of expenses and income payments on credit card"""
        initial_balance = credit_card.balance  # 0.0

        # Add expense (increase debt)
        client.post('/add_transaction', data={
            'card_id': credit_card.id,
            'transaction_type': 'expense',
            'amount': 400.0,
            'description': 'Shopping',
            'category': 'Shopping',
            'date': '2024-01-05'
        })

        # Add payment (reduce debt)
        client.post('/add_transaction', data={
            'card_id': credit_card.id,
            'transaction_type': 'income',
            'amount': 150.0,
            'description': 'Payment',
            'category': 'Salary',
            'date': '2024-01-15'
        })

        # Check net effect
        updated_card = Card.query.get(credit_card.id)
        expected_balance = initial_balance + 400.0 - 150.0
        assert updated_card.balance == expected_balance
        assert updated_card.balance == 250.0

    def test_multiple_mixed_transactions(self, client, debit_card):
        """Test multiple mixed transactions to verify correct accounting"""
        initial_balance = debit_card.balance

        transactions_data = [
            ('income', 1000.0),
            ('expense', 150.0),
            ('expense', 75.50),
            ('income', 200.0),
            ('expense', 300.0),
        ]

        for trans_type, amount in transactions_data:
            client.post('/add_transaction', data={
                'card_id': debit_card.id,
                'transaction_type': trans_type,
                'amount': amount,
                'description': f'Test {trans_type}',
                'category': 'Other',
                'date': '2024-01-15'
            })

        # Calculate expected balance
        expected = initial_balance + 1000.0 - 150.0 - 75.50 + 200.0 - 300.0

        updated_card = Card.query.get(debit_card.id)
        assert updated_card.balance == expected
        assert updated_card.balance == 1674.50

        # Verify all transactions were created
        transactions = Transaction.query.filter_by(card_id=debit_card.id).all()
        assert len(transactions) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
