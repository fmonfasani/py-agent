# py-agent-client

> 🚧 **Early Development** - Building intelligent AI API routing with cost optimization

## What we're building

A Python client that automatically routes AI requests to the optimal provider (OpenAI, Anthropic, DeepSeek) based on cost, quality, and speed requirements.

**Goal**: Reduce AI API costs by 30%+ through intelligent routing while maintaining quality.

## Current Status

- ✅ **Project Structure**: Complete Python package setup
- ✅ **Development Tools**: CI/CD, testing framework, code quality tools
- ✅ **Documentation**: Examples and integration guides ready
- 🏗️ **Core Engine**: Routing logic (in development)
- 📋 **Provider Adapters**: OpenAI, Anthropic, DeepSeek (planned)
- 📋 **Cost Optimization**: Budget controls and analytics (planned)
- 📋 **Context Management**: Session persistence (planned)

## Planned Features

- **Smart Routing**: Automatic model selection based on task type
- **Cost Guardian**: Real-time budget monitoring and controls
- **Quality Assurance**: Minimum quality thresholds with fallbacks
- **Analytics**: Usage tracking and optimization insights
- **Zero Lock-in**: Direct API access and provider flexibility

## Architecture (MVP)

```
py_agent_client/
├── core/
│   ├── router.py          # Intelligent routing logic
│   ├── cost_guardian.py   # Budget management
│   ├── context_manager.py # Session handling
│   └── telemetry.py       # Usage analytics
├── providers/
│   ├── openai_adapter.py  # OpenAI integration
│   ├── anthropic_adapter.py
│   └── deepseek_adapter.py
└── client.py              # Main Agent class
```

## Installation (when ready)

```bash
# Not yet published to PyPI
pip install py-agent-client
```

## Usage (planned API)

```python
from py_agent_client import Agent

# Initialize with provider API keys
agent = Agent(
    api_key="your-py-agent-key",
    providers={
        "openai": "sk-...",
        "anthropic": "sk-ant-...",
        "deepseek": "sk-..."
    }
)

# Automatic routing based on optimization preferences
result = await agent.route(
    "Explain quantum computing in simple terms",
    optimize_for="cost"  # or "quality", "speed", "balanced"
)

print(f"Response: {result.response}")
print(f"Model used: {result.model}")
print(f"Cost: ${result.cost:.4f}")
print(f"Savings: {result.savings_percent}%")
```

## Development

### Quick Setup

```bash
git clone https://github.com/fmonfasani/py-agent.git
cd py-agent
pip install -e ".[dev]"
pytest tests/
```

### Project Structure

```bash
make install-dev    # Install development dependencies
make test          # Run tests
make lint          # Code quality checks
make format        # Format code
```

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed setup and contribution guidelines.

## Roadmap

### Phase 1: MVP Foundation (4 weeks)
- [ ] Basic Agent class with provider abstractions
- [ ] Simple routing logic with heuristic rules
- [ ] Cost tracking and budget enforcement
- [ ] OpenAI, Anthropic, DeepSeek integrations
- [ ] Basic examples and documentation

### Phase 2: Optimization (8 weeks)
- [ ] ML-based routing decisions
- [ ] Advanced cost optimization algorithms
- [ ] Performance analytics dashboard
- [ ] Context management and session persistence
- [ ] Custom model support

### Phase 3: Enterprise (12 weeks)
- [ ] Self-hosted deployment options
- [ ] Advanced security and compliance features
- [ ] API rate limiting and scaling
- [ ] Custom provider integrations

## Validation Experiment

**Target**: Demonstrate ≥30% cost savings across real workloads

**Methodology**:
1. Implement heuristic routing with 3 providers
2. Test on 500 diverse prompts across different categories
3. Compare costs vs direct API usage
4. Measure quality maintenance and latency impact

**Success Metrics**:
- 30%+ cost reduction
- <250ms routing overhead
- >95% quality score maintenance

## Contributing

We're in early development and welcome contributors! 

**Current needs**:
- Core routing engine implementation
- Provider adapter development
- Testing and validation
- Documentation and examples

**Getting involved**:
1. Check [open issues](https://github.com/fmonfasani/py-agent/issues)
2. Read [DEVELOPMENT.md](DEVELOPMENT.md) for setup
3. Join discussions in [GitHub Discussions](https://github.com/fmonfasani/py-agent/discussions)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- **Repository**: [github.com/fmonfasani/py-agent](https://github.com/fmonfasani/py-agent)
- **Issues**: [Report bugs or request features](https://github.com/fmonfasani/py-agent/issues)
- **Discussions**: [Community discussions](https://github.com/fmonfasani/py-agent/discussions)

---

**Built with transparency** 🚀

*This is an honest open-source project in active development. We'll update this README as we build and validate each feature.*  