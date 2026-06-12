# Contributing

Thank you for your interest in contributing to the Port Scanner project! Here are some guidelines to help you get started.

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/portForge.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -e .`
6. Install development dependencies: `pip install -r requirements.txt`

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep lines under 88 characters

## Testing

- Write tests for new functionality
- Ensure all tests pass before submitting a pull request: `pytest tests/`
- Run linting checks: `flake8 src/`
- Run type checking: `mypy src/`

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Add tests if applicable
4. Update documentation if needed
5. Run all checks (tests, linting, type checking)
6. Commit your changes: `git commit -m "description of changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a pull request on GitHub

## Reporting Issues

Please use the GitHub issue tracker to report bugs or suggest features.