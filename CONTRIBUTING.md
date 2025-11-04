# Contributing to AI-SRE with Kagent and Llama 3.2

Thank you for your interest in contributing! We welcome contributions from the community.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear title and description
- Steps to reproduce the issue
- Expected vs actual behavior
- System information (OS, Python version, etc.)

### Suggesting Enhancements

We love new ideas! Please open an issue with:
- A clear title and description
- Use cases and benefits
- Potential implementation approach

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/sebbycorp/AI-SRE-With-Kagent-OSS-Llama3.2.git
   cd AI-SRE-With-Kagent-OSS-Llama3.2
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

4. **Run tests**
   ```bash
   python -m unittest discover tests -v
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all CI checks pass

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

### Testing

- Write unit tests for new functionality
- Ensure existing tests still pass
- Aim for good test coverage
- Test edge cases and error conditions

### Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Include examples for new features
- Keep documentation clear and concise

### Commit Messages

Use clear, descriptive commit messages:
- `Add: new feature or functionality`
- `Fix: bug fix`
- `Update: changes to existing feature`
- `Docs: documentation changes`
- `Test: test additions or changes`
- `Refactor: code restructuring`

## 🏗️ Project Structure

```
.
├── src/                    # Source code
│   ├── agent.py           # Main agent implementation
│   ├── llm_client.py      # Llama client
│   ├── monitoring.py      # System monitoring
│   ├── log_analyzer.py    # Log analysis
│   ├── incident_detector.py  # Incident detection
│   └── remediation.py     # Remediation engine
├── tests/                 # Unit tests
├── examples/              # Example scripts
├── config/                # Configuration files
└── docs/                  # Additional documentation
```

## 🧪 Testing Your Changes

Run the full test suite:
```bash
python -m unittest discover tests -v
```

Run specific tests:
```bash
python -m unittest tests.test_monitoring
```

Run examples:
```bash
PYTHONPATH=. python examples/system_monitoring_example.py
```

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Questions?

Feel free to:
- Open an issue for discussion
- Join our community discussions
- Reach out to the maintainers

Thank you for making AI-SRE better! 🚀
