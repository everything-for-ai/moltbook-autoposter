# Contributing to Everything for AI

Thank you for your interest in contributing! This guide will help you get started.

## How to Contribute

### 1. Find a Project

Browse our [organization](https://github.com/everything-for-ai) to find a project that interests you.

### 2. Pick an Issue

- Look for issues labeled `good first issue` or `help wanted`
- Or create a new issue for bugs/feature requests

### 3. Fork and Clone

```bash
# Fork on GitHub, then clone
git clone https://github.com/YOUR-USERNAME/PROJECT-NAME.git
cd PROJECT-NAME
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 5. Make Changes

Follow the coding style:
- Python: PEP 8
- JavaScript: ESLint
- Comments in English or Chinese

### 6. Test Your Changes

```bash
# Run existing tests
python -m pytest

# Or manually test
python your_changed_file.py
```

### 7. Commit and Push

```bash
git add .
git commit -m "Add: Description of your changes"
git push origin feature/your-feature-name
```

### 8. Create Pull Request

Go to GitHub and create a Pull Request from your branch.

## Coding Standards

### Python Projects

```python
def function_name(param: type) -> return_type:
    """Brief description.
    
    Args:
        param: Description of parameter
    
    Returns:
        Description of return value
    """
    # Your code
    pass
```

### Project Structure

```
project-name/
├── main.py           # Entry point
├── module.py         # Core functionality
├── config.json       # Configuration
├── requirements.txt  # Dependencies
├── README.md         # Documentation
└── tests/
    └── test_*.py     # Unit tests
```

## Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Restructuring
- `test`: Testing
- `chore`: Maintenance

Example:
```
feat(weather): Add OpenWeatherMap API integration

- Implement current weather endpoint
- Add forecast support
- Improve error handling

Closes #123
```

## Code Review

All PRs require review before merging. Please be patient and responsive to feedback.

## Questions?

- Open an issue
- Check existing documentation
- Ask in discussions

Thank you for contributing! 🎉
