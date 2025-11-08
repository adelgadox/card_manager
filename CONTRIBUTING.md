# Contributing to Card Manager

Thank you for considering contributing to Card Manager! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Trolling or insulting remarks
- Public or private harassment
- Publishing others' private information without permission

---

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title**: Descriptive summary of the bug
2. **Steps to reproduce**: Detailed steps to reproduce the issue
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: Python version, OS, browser (if applicable)
6. **Screenshots**: If applicable

**Example:**
```markdown
**Bug**: Transaction balance not updating correctly

**Steps to Reproduce:**
1. Add a debit card with balance $1000
2. Add an expense of $100
3. Check card balance

**Expected:** Balance should be $900
**Actual:** Balance remains $1000

**Environment:** Python 3.9, macOS 13, Chrome 120
```

### Suggesting Enhancements

We welcome feature suggestions! Please create an issue with:

1. **Clear description**: What feature you'd like to see
2. **Use case**: Why this feature would be useful
3. **Proposed solution**: How you envision it working
4. **Alternatives**: Other solutions you've considered

### Contributing Code

1. **Small fixes**: Typos, documentation, small bugs - feel free to submit a PR directly
2. **New features**: Please open an issue first to discuss
3. **Large changes**: Always discuss in an issue before starting work

---

## Getting Started

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
```bash
git clone https://github.com/YOUR_USERNAME/card_manager.git
cd card_manager
```

3. **Add upstream remote**:
```bash
git remote add upstream https://github.com/adelgadox/card_manager.git
```

### Setup Development Environment

1. **Create virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run tests to verify setup**:
```bash
pytest test_app.py -v
```

---

## Development Workflow

### 1. Sync with Upstream

Before starting work, sync with the main repository:

```bash
git checkout master
git fetch upstream
git merge upstream/master
git push origin master
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/my-awesome-feature
```

**Branch Naming Convention:**
- `feature/` - New features (e.g., `feature/export-csv`)
- `fix/` - Bug fixes (e.g., `fix/balance-calculation`)
- `docs/` - Documentation (e.g., `docs/api-examples`)
- `refactor/` - Code refactoring (e.g., `refactor/database-queries`)
- `test/` - Adding tests (e.g., `test/transaction-validation`)

### 3. Make Your Changes

- Write clean, readable code
- Follow the coding standards (see below)
- Add tests for new features
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run all tests
pytest test_app.py -v

# Run specific tests
pytest test_app.py::TestAddExpense -v

# Check test coverage
pytest test_app.py --cov=app
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Add feature: description"
```

See [Commit Guidelines](#commit-guidelines) below.

### 6. Push to Your Fork

```bash
git push origin feature/my-awesome-feature
```

### 7. Create Pull Request

Go to GitHub and create a pull request from your branch to the main repository's `master` branch.

---

## Coding Standards

### Python Style

Follow **PEP 8** guidelines:

```bash
# Install flake8 for linting
pip install flake8

# Run linter
flake8 app.py test_app.py
```

**Key Points:**
- Use 4 spaces for indentation (not tabs)
- Maximum line length: 79 characters (flexible to 100 for long strings)
- Use snake_case for functions and variables
- Use PascalCase for classes
- Add docstrings to functions and classes

**Example:**
```python
def calculate_balance(card, amount, transaction_type):
    """
    Calculate new card balance after transaction.

    Args:
        card (Card): The card object
        amount (float): Transaction amount
        transaction_type (str): 'income' or 'expense'

    Returns:
        float: The new balance
    """
    if card.card_type == 'debit':
        if transaction_type == 'income':
            return card.balance + amount
        return card.balance - amount
    else:  # credit card
        if transaction_type == 'income':
            return card.balance - amount
        return card.balance + amount
```

### HTML/CSS Style

- Use 2 spaces for indentation in HTML
- Keep templates clean and readable
- Use semantic HTML5 elements
- Follow BEM methodology for CSS class names when possible

### Testing Standards

- Write tests for all new features
- Aim for 80%+ code coverage
- Use descriptive test names
- One logical assertion per test when possible
- Use fixtures for common setup

---

## Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat: Add CSV export functionality

Implement CSV export for transactions with filtering options.
Users can now export their transaction history as CSV files.

Closes #45
```

```
fix: Correct balance calculation for credit cards

Credit card balance was increasing on income transactions instead
of decreasing. Fixed the logic in add_transaction route.

Fixes #67
```

```
docs: Update API documentation with new endpoints

Added documentation for the export endpoints and updated
examples in API.md.
```

### Commit Best Practices

- **Atomic commits**: One logical change per commit
- **Clear messages**: Explain what and why, not how
- **Present tense**: "Add feature" not "Added feature"
- **Imperative mood**: "Fix bug" not "Fixes bug"

---

## Pull Request Process

### Before Submitting

✅ **Checklist:**
- [ ] Code follows the project's style guidelines
- [ ] All tests pass (`pytest test_app.py -v`)
- [ ] New tests added for new features
- [ ] Documentation updated (README, API docs, etc.)
- [ ] No unnecessary files included (.pyc, __pycache__, etc.)
- [ ] Commit messages follow guidelines
- [ ] Branch is up to date with master

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
```

### Review Process

1. **Automated checks**: GitHub Actions will run tests
2. **Code review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

### After Merge

- Delete your feature branch
- Sync your fork with upstream
- Celebrate! 🎉

---

## Reporting Bugs

### Security Vulnerabilities

**Do NOT** create public issues for security vulnerabilities.

Instead, email the maintainers directly (check repository for contact info).

### Bug Report Template

```markdown
**Describe the Bug**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., macOS 13]
- Python version: [e.g., 3.9]
- Browser: [e.g., Chrome 120]

**Additional Context**
Any other relevant information.
```

---

## Suggesting Enhancements

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions or features you've considered.

**Additional context**
Any other context, mockups, or examples.
```

---

## Development Resources

### Helpful Links

- [Main README](README.md) - Project overview
- [API Documentation](docs/API.md) - API reference
- [Development Guide](docs/DEVELOPMENT.md) - Detailed development info
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

### Getting Help

- **GitHub Issues**: For bugs and features
- **GitHub Discussions**: For questions and general discussion
- **Email**: Contact maintainers for sensitive issues

---

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Card Manager! Your efforts help make this project better for everyone. 🙏
