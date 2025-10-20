# Contributing to Data Quality Framework with Great Expectations

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](https://github.com/galafis/data-quality-framework-great-expectations/issues) section
2. If not, create a new issue with:
   - A clear title
   - Detailed description of the problem or suggestion
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Screenshots if applicable

### Submitting Changes

1. **Fork the Repository**
   ```bash
   git clone https://github.com/galafis/data-quality-framework-great-expectations.git
   cd data-quality-framework-great-expectations
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make Your Changes**
   - Write clear, concise code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

4. **Run Tests**
   ```bash
   pytest -v
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: clear description of your changes"
   ```
   
   Follow commit message conventions:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for changes to existing features
   - `Docs:` for documentation changes
   - `Test:` for test additions/changes

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template with details about your changes

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting PR
- Aim for at least 80% code coverage
- Use pytest fixtures for test setup

### Documentation

- Update README.md if adding new features
- Add docstrings to all functions and classes
- Include code examples for new functionality
- Update existing documentation if modifying features

## Project Structure

```
data-quality-framework-great-expectations/
├── great_expectations/       # Great Expectations configuration
│   └── expectations/        # Expectation suites
├── notebooks/               # Python scripts and notebooks
├── data/                    # Sample data files
├── tests/                   # Test files
├── images/                  # Documentation images
├── .github/workflows/       # CI/CD workflows
└── README.md               # Project documentation
```

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the `question` label
- Contact the maintainer: Gabriel Demetrios Lafis

## Code of Conduct

Please note that this project follows a Code of Conduct. By participating, you are expected to uphold this code.

Thank you for contributing! 🎉
