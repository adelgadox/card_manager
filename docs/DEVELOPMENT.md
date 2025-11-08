# Development Guide

This guide provides detailed information for developers who want to contribute to or extend the Card Manager project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Project Architecture](#project-architecture)
- [Code Style](#code-style)
- [Testing](#testing)
- [Database](#database)
- [Adding New Features](#adding-new-features)
- [Debugging](#debugging)
- [Common Tasks](#common-tasks)

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Code editor (VS Code, PyCharm, etc.)
- SQLite browser (optional, for database inspection)

### Initial Setup

1. **Fork and clone the repository**:
```bash
git clone https://github.com/YOUR_USERNAME/card_manager.git
cd card_manager
```

2. **Create a virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python app.py
```

5. **Run tests**:
```bash
pytest test_app.py -v
```

---

## Development Environment

### Recommended Tools

**IDEs/Editors:**
- **VS Code**: With Python extension
- **PyCharm**: Professional or Community Edition
- **Sublime Text**: With Python packages

**VS Code Extensions:**
- Python (Microsoft)
- Pylance
- Python Test Explorer
- SQLite Viewer
- GitLens

**Browser Tools:**
- Chrome DevTools
- Firefox Developer Tools

### Environment Variables

Currently, the application uses default Flask settings. For development, you can create a `.env` file:

```bash
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///cards.db
```

---

## Project Architecture

### Application Structure

```
card_manager/
├── app.py                 # Main application file
│   ├── Flask app initialization
│   ├── Database models (Card, Transaction)
│   ├── Routes/Views
│   └── Application logic
├── templates/             # Jinja2 HTML templates
│   ├── base.html         # Base layout with navigation
│   ├── index.html        # Dashboard
│   ├── add_card.html     # Card form
│   ├── add_transaction.html  # Transaction form
│   └── transactions.html  # Transaction list
├── static/               # Static assets
│   └── css/
│       └── style.css     # Application styles
├── test_app.py           # Unit tests
└── docs/                 # Documentation
```

### Design Patterns

**MVC-like Structure:**
- **Models**: `Card` and `Transaction` classes
- **Views**: Jinja2 templates in `templates/`
- **Controllers**: Route functions in `app.py`

**Database Pattern:**
- ORM: SQLAlchemy
- Repository: Flask-SQLAlchemy integration
- Migrations: Not currently implemented (consider Flask-Migrate)

---

## Code Style

### Python Style Guide

Follow **PEP 8** standards:

```python
# Good
def calculate_monthly_savings(income, expenses):
    """Calculate net savings for a month."""
    return income - expenses

# Bad
def calcSavings(i,e):
    return i-e
```

### Naming Conventions

**Variables and Functions:**
```python
card_name = "Chase Checking"        # snake_case
transaction_type = "income"
```

**Classes:**
```python
class Card(db.Model):               # PascalCase
    pass

class Transaction(db.Model):
    pass
```

**Constants:**
```python
MAX_DESCRIPTION_LENGTH = 200        # UPPER_CASE
DEFAULT_BALANCE = 0.0
```

### Documentation

**Docstrings:**
```python
def add_transaction(card_id, amount, description):
    """
    Add a new transaction to a card.

    Args:
        card_id (int): ID of the card
        amount (float): Transaction amount
        description (str): Transaction description

    Returns:
        Transaction: The created transaction object
    """
    # Implementation
```

**Comments:**
```python
# Calculate net effect on balance
if card.card_type == 'debit':
    card.balance += amount  # Income increases debit balance
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest test_app.py -v

# Run specific test class
pytest test_app.py::TestAddExpense -v

# Run specific test
pytest test_app.py::TestAddExpense::test_add_expense_to_debit_card_reduces_balance -v

# Run with coverage
pytest test_app.py --cov=app --cov-report=html
```

### Writing Tests

**Test Structure:**
```python
class TestNewFeature:
    """Tests for new feature"""

    def test_feature_works_correctly(self, client, debit_card):
        """Test that feature works as expected"""
        # Arrange
        initial_state = debit_card.balance

        # Act
        response = client.post('/endpoint', data={...})

        # Assert
        assert response.status_code == 200
        assert debit_card.balance == expected_value
```

**Testing Best Practices:**
- One assertion per test (when possible)
- Use descriptive test names
- Test both success and failure cases
- Use fixtures for common setup
- Keep tests independent

### Test Coverage Goals

Aim for:
- **80%+** code coverage
- All critical paths tested
- Edge cases covered
- Error handling tested

---

## Database

### Schema Overview

**Card Model:**
```python
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    card_type = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    transactions = db.relationship('Transaction', backref='card',
                                   lazy=True, cascade='all, delete-orphan')
```

**Transaction Model:**
```python
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
```

### Database Operations

**Creating Records:**
```python
new_card = Card(name='Test Card', card_type='debit', balance=1000.0)
db.session.add(new_card)
db.session.commit()
```

**Querying:**
```python
# Get all cards
cards = Card.query.all()

# Get by ID
card = Card.query.get(1)

# Filter
debit_cards = Card.query.filter_by(card_type='debit').all()
```

**Updating:**
```python
card = Card.query.get(1)
card.balance += 100.0
db.session.commit()
```

**Deleting:**
```python
card = Card.query.get(1)
db.session.delete(card)
db.session.commit()
```

### Database Migrations

Currently not implemented. To add:

```bash
pip install Flask-Migrate
```

Then in `app.py`:
```python
from flask_migrate import Migrate

migrate = Migrate(app, db)
```

---

## Adding New Features

### Feature Development Workflow

1. **Create a new branch**:
```bash
git checkout -b feature/my-new-feature
```

2. **Write tests first** (TDD approach):
```python
# test_app.py
def test_new_feature(client):
    # Test implementation
    pass
```

3. **Implement the feature**:
```python
# app.py
@app.route('/new-endpoint')
def new_feature():
    # Implementation
    pass
```

4. **Run tests**:
```bash
pytest test_app.py -v
```

5. **Update documentation**:
- Update README.md
- Update API.md
- Add inline comments

6. **Commit changes**:
```bash
git add .
git commit -m "Add new feature: description"
```

7. **Push and create PR**:
```bash
git push origin feature/my-new-feature
```

### Example: Adding a New Category

1. **Update the template** (`add_transaction.html`):
```html
<option value="Education">Education</option>
```

2. **No backend changes needed** (categories are stored as strings)

3. **Add test**:
```python
def test_education_category(client, debit_card):
    response = client.post('/add_transaction', data={
        'card_id': debit_card.id,
        'category': 'Education',
        # ... other fields
    })
    assert response.status_code == 200
```

---

## Debugging

### Flask Debug Mode

Debug mode is enabled by default in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True)
```

**Features:**
- Auto-reload on code changes
- Interactive debugger in browser
- Detailed error pages

### Using Python Debugger

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use Python 3.7+ builtin
breakpoint()
```

### Logging

Add logging to debug issues:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Card balance: {card.balance}")
logger.info(f"Transaction created: {transaction.id}")
logger.error(f"Failed to process: {error}")
```

### Common Issues

**Database Locked:**
```bash
# Delete the database and restart
rm cards.db
python app.py
```

**Template Not Found:**
- Check template name matches file name
- Ensure templates are in `templates/` directory

**Static Files Not Loading:**
- Clear browser cache
- Check file path: `/static/css/style.css`

---

## Common Tasks

### Reset Database

```bash
rm cards.db
python app.py
```

### Add Sample Data

```python
# In Python console or script
from app import app, db, Card, Transaction
from datetime import datetime

with app.app_context():
    # Create cards
    debit = Card(name='Test Debit', card_type='debit', balance=1000.0)
    credit = Card(name='Test Credit', card_type='credit', balance=500.0)
    db.session.add_all([debit, credit])
    db.session.commit()

    # Create transactions
    t1 = Transaction(card_id=debit.id, transaction_type='income',
                     amount=2000.0, description='Salary',
                     category='Salary', date=datetime(2024, 1, 1))
    db.session.add(t1)
    db.session.commit()
```

### Backup Database

```bash
cp cards.db cards_backup_$(date +%Y%m%d).db
```

### Update Dependencies

```bash
pip list --outdated
pip install --upgrade flask flask-sqlalchemy
pip freeze > requirements.txt
```

---

## Performance Optimization

### Database Queries

**Bad:**
```python
for card in Card.query.all():
    print(card.transactions)  # N+1 queries
```

**Good:**
```python
cards = Card.query.options(db.joinedload('transactions')).all()
for card in cards:
    print(card.transactions)  # Single query
```

### Caching

Consider adding caching for:
- Monthly statistics calculations
- Frequently accessed data

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
@cache.cached(timeout=60)
def index():
    # Cached for 60 seconds
    pass
```

---

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest test_app.py -v
```

---

## Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)

### Tutorials
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)

---

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/adelgadox/card_manager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/adelgadox/card_manager/discussions)
- **Email**: Check repository for contact info

---

Happy coding! 🚀
