# Development Setup Guide

This guide covers setting up the py-agent-client development environment and contributing to the project.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Git
- Make (optional, for convenience)

### 1. Clone Repository
```bash
# Create GitHub organization first: https://github.com/organizations/new
# Organization name: py-agent

# Clone the client repository
git clone https://github.com/py-agent/client.git
cd client
```

### 2. Development Setup
```bash
# Install in development mode with all dependencies
make install-dev

# Or manually:
pip install -e ".[dev]"
pre-commit install
```

### 3. Verify Installation
```bash
# Run tests to ensure everything works
make test

# Run full CI pipeline locally
make ci
```

## 📁 Project Structure

```
py-agent/client/
├── py_agent_client/           # Main package
│   ├── __init__.py           # Package initialization
│   ├── client.py             # Main Agent class
│   ├── models.py             # Pydantic data models
│   ├── exceptions.py         # Custom exceptions
│   ├── core/                 # Core components
│   │   ├── router.py         # Routing logic
│   │   ├── cost_guardian.py  # Budget management
│   │   ├── context_manager.py # Session management
│   │   └── telemetry.py      # Analytics collection
│   └── providers/            # AI provider adapters
│       ├── openai_adapter.py
│       ├── anthropic_adapter.py
│       └── deepseek_adapter.py
├── tests/                    # Test suite
│   ├── conftest.py          # Test configuration
│   ├── test_client.py       # Main tests
│   ├── test_cost_guardian.py
│   └── integration/         # Integration tests
├── examples/                 # Usage examples
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   └── integrations.py
├── docs/                     # Documentation
├── .github/                  # GitHub workflows
│   ├── workflows/
│   │   ├── ci.yml           # CI pipeline
│   │   └── publish.yml      # PyPI publishing
│   └── ISSUE_TEMPLATE/      # Issue templates
├── pyproject.toml           # Project configuration
├── setup.py                 # Setup script
├── requirements.txt         # Dependencies
├── requirements-dev.txt     # Dev dependencies
├── Makefile                 # Development commands
├── tox.ini                  # Multi-Python testing
├── mkdocs.yml              # Documentation config
└── README.md               # Main documentation
```

## 🛠️ Development Workflow

### Daily Development
```bash
# Start development
git checkout -b feature/your-feature-name

# Make changes, then test
make test

# Format and lint code
make format
make lint

# Type checking
make type-check

# Run full CI locally before pushing
make ci

# Commit and push
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
```

### Running Tests
```bash
# Quick test run
pytest

# With coverage
make test-cov

# Integration tests only
make test-integration

# Test across Python versions
tox

# Specific test file
pytest tests/test_client.py -v

# Specific test method
pytest tests/test_client.py::TestAgent::test_route_simple_request -v
```

### Code Quality
```bash
# Format code
black py_agent_client tests
isort py_agent_client tests

# Or use make command
make format

# Lint code
flake8 py_agent_client tests
make lint

# Type checking
mypy py_agent_client
make type-check

# Security scanning
bandit -r py_agent_client
safety check
make security
```

## 🚢 Release Process

### Version Management
```bash
# Bump version (patch, minor, major)
bump2version patch

# Or manually update version in:
# - py_agent_client/__init__.py
# - pyproject.toml
```

### Building and Publishing
```bash
# Build package
make build

# Check package
make release-check

# Upload to test PyPI
make upload-test

# Upload to production PyPI
make upload
```

### GitHub Release Process
1. **Create Release Branch**
   ```bash
   git checkout -b release/v0.1.0
   ```

2. **Update Changelog**
   - Update `CHANGELOG.md` with new features
   - Update version numbers

3. **Create Pull Request**
   - Title: "Release v0.1.0"
   - Include changelog in description

4. **Merge and Tag**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

5. **GitHub Actions** will automatically:
   - Run CI tests
   - Build package
   - Publish to PyPI
   - Create GitHub release

## 📊 Monitoring and Analytics

### Local Development Analytics
```bash
# View test coverage
make test-cov
open htmlcov/index.html

# Performance benchmarks
pytest tests/benchmarks/ --benchmark-only

# Memory profiling
python -m memory_profiler examples/basic_usage.py
```

### Production Monitoring
- **Error Tracking**: Sentry integration
- **Performance**: Custom telemetry system
- **Usage Analytics**: Built-in analytics dashboard

## 🔧 Configuration

### Environment Variables
```bash
# Required for testing with real APIs
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."

# Optional: py-agent platform key
export PY_AGENT_API_KEY="your-platform-key"

# Development settings
export PY_AGENT_ENV="development"
export PY_AGENT_DEBUG="true"
```

### Development Configuration
Create `.env.local` (gitignored):
```env
OPENAI_API_KEY=sk-your-dev-key
ANTHROPIC_API_KEY=sk-ant-your-dev-key
DEEPSEEK_API_KEY=sk-your-dev-key
PY_AGENT_DEBUG=true
```

## 🐛 Debugging

### Common Issues

**Import Errors**
```bash
# Reinstall in development mode
pip install -e .
```

**Test Failures**
```bash
# Clear cache and rerun
pytest --cache-clear

# Run with verbose output
pytest -v -s
```

**Type Check Errors**
```bash
# Clear mypy cache
rm -rf .mypy_cache
mypy py_agent_client
```

### Debug Mode
```python
import py_agent_client
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("py_agent_client")
logger.setLevel(logging.DEBUG)

# Create agent with debug mode
agent = py_agent_client.Agent(
    api_key="test",
    debug=True
)
```

## 📚 Documentation

### Building Docs Locally
```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build docs
make docs

# Serve docs locally
make serve-docs
# Visit http://localhost:8000
```

### Writing Documentation
- Use **Google-style docstrings**
- Include **examples** in docstrings
- Update **API reference** for new features
- Add **examples** to `/examples` directory

### Documentation Structure
```
docs/
├── index.md              # Homepage
├── getting-started/      # Tutorials
├── guide/               # User guides
├── api/                 # API reference
├── examples/            # Code examples
└── deployment/          # Production guides
```

## 🤝 Contributing Guidelines

### Code Standards
- **PEP 8** compliance (enforced by black/flake8)
- **Type hints** for all public APIs
- **Google-style docstrings**
- **95%+ test coverage** for new code
- **No breaking changes** without major version bump

### Commit Message Format
```
type(scope): description

feat(router): add custom routing rules support
fix(cost): resolve budget calculation edge case
docs(api): update Agent class documentation
test(integration): add DeepSeek provider tests
```

### Pull Request Checklist
- [ ] Tests pass locally
- [ ] Code is formatted and linted
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact assessed

## 🏗️ Architecture Decisions

### Key Design Principles
1. **Simplicity**: Easy to use, complex under the hood
2. **Performance**: <250ms routing overhead
3. **Reliability**: Graceful degradation and fallbacks
4. **Observability**: Comprehensive metrics and logging
5. **Extensibility**: Plugin architecture for providers

### Technology Choices
- **Pydantic**: Data validation and serialization
- **httpx**: Modern async HTTP client
- **pytest**: Testing framework
- **black**: Code formatting
- **mypy**: Static type checking

## 🎯 MVP Goals Checklist

### Core Functionality
- [ ] Basic routing between OpenAI, Anthropic, DeepSeek
- [ ] Cost optimization (target: 30% savings)
- [ ] Budget management and controls
- [ ] Quality threshold enforcement
- [ ] Session context management
- [ ] Basic analytics and reporting

### Performance Targets
- [ ] <250ms routing overhead
- [ ] 95%+ uptime
- [ ] Support for 1000+ requests/minute
- [ ] <80MB memory footprint

### Quality Metrics
- [ ] 95%+ test coverage
- [ ] Zero critical security vulnerabilities
- [ ] <5 open bugs at any time
- [ ] 99%+ quality score maintenance

### Documentation
- [ ] Complete API documentation
- [ ] Integration examples for 5+ frameworks
- [ ] Production deployment guides
- [ ] Performance tuning guides

---

## 📞 Support

- **Documentation**: https://docs.py-agent.com
- **Discord**: https://discord.gg/py-agent
- **Issues**: https://github.com/py-agent/client/issues
- **Email**: hello@py-agent.com

Happy coding! 🚀