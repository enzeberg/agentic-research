# Contributing to Agentic Research System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agentic-research
   ```

2. **Install uv** (if not already installed)
   ```bash
   # See https://docs.astral.sh/uv/
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run tests**
   ```bash
   uv run pytest
   ```

## Code Style

### Python Style Guide
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for all public functions/classes

### Formatting
```bash
# Format code
uv run black src/

# Check linting
uv run ruff check src/

# Type checking
uv run mypy src/
```

### Docstring Format
```python
def function_name(arg1: str, arg2: int) -> bool:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
    pass
```

## Testing

### Writing Tests
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Include docstrings

### Running Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_memory.py

# Run with coverage
uv run pytest --cov=src
```

## Pull Request Process

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Ensure quality**
   ```bash
   uv run black src/
   uv run ruff check src/
   uv run mypy src/
   uv run pytest
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks

## Adding New Features

### New Agent
1. Create agent file in `src/agents/`
2. Implement agent class with required methods
3. Add tests in `tests/`
4. Update workflow if needed
5. Document in README and ARCHITECTURE

### New Tool
1. Create tool file in `src/tools/`
2. Implement tool interface
3. Add tests
4. Integrate with Research Agent
5. Update documentation

### New LLM Provider
1. Update `src/llm/router.py`
2. Add configuration in `src/config.py`
3. Update `.env.example`
4. Add tests
5. Update documentation

## Documentation

### Code Documentation
- All public functions/classes need docstrings
- Include type hints
- Explain complex logic with comments

### User Documentation
- Update README.md for user-facing changes
- Update ARCHITECTURE.md for system changes
- Add examples for new features

## Issue Reporting

### Bug Reports
Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
- Error messages/logs

### Feature Requests
Include:
- Description of the feature
- Use case
- Proposed implementation (optional)
- Alternatives considered

## Code Review

### Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No breaking changes (or documented)
- [ ] Performance impact considered
- [ ] Security implications reviewed

## Questions?

Feel free to:
- Open an issue for discussion
- Ask in pull request comments
- Contact maintainers

Thank you for contributing!
