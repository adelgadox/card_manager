from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func, extract
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    card_type = db.Column(db.String(20), nullable=False)  # 'debit' or 'credit'
    balance = db.Column(db.Float, default=0.0)
    transactions = db.relationship('Transaction', backref='card', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Card {self.name} - {self.card_type}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.description} - ${self.amount}>'

# Initialize database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    cards = Card.query.all()

    # Calculate monthly statistics
    transactions = Transaction.query.all()
    monthly_stats = {}

    for transaction in transactions:
        month_key = transaction.date.strftime('%Y-%m')
        if month_key not in monthly_stats:
            monthly_stats[month_key] = {'income': 0, 'expenses': 0, 'savings': 0}

        if transaction.transaction_type == 'income':
            monthly_stats[month_key]['income'] += transaction.amount
        else:
            monthly_stats[month_key]['expenses'] += transaction.amount

    # Calculate savings
    for month in monthly_stats:
        monthly_stats[month]['savings'] = monthly_stats[month]['income'] - monthly_stats[month]['expenses']

    # Sort by month (most recent first)
    sorted_months = sorted(monthly_stats.items(), reverse=True)

    return render_template('index.html', cards=cards, monthly_stats=sorted_months)

@app.route('/add_card', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        name = request.form['name']
        card_type = request.form['card_type']
        balance = float(request.form['balance'])

        new_card = Card(name=name, card_type=card_type, balance=balance)
        db.session.add(new_card)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_card.html')

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        card_id = int(request.form['card_id'])
        transaction_type = request.form['transaction_type']
        amount = float(request.form['amount'])
        description = request.form['description']
        category = request.form['category']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d')

        card = Card.query.get(card_id)

        # Update card balance
        if card.card_type == 'debit':
            if transaction_type == 'expense':
                card.balance -= amount
            else:  # income
                card.balance += amount
        else:  # credit card
            if transaction_type == 'expense':
                card.balance += amount  # Credit card balance increases with expenses
            else:  # income
                card.balance -= amount  # Income reduces credit card debt

        # Create transaction
        new_transaction = Transaction(
            card_id=card_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            category=category,
            date=date
        )

        db.session.add(new_transaction)
        db.session.commit()

        return redirect(url_for('index'))

    cards = Card.query.all()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('add_transaction.html', cards=cards, today=today)

@app.route('/transactions')
def transactions():
    all_transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', transactions=all_transactions)

@app.route('/delete_card/<int:card_id>', methods=['POST'])
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
