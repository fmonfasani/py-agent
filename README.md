# py-agent-client

**Intelligent API routing for AI workloads with automatic cost optimization**

[![PyPI version](https://badge.fury.io/py/py-agent-client.svg)](https://badge.fury.io/py/py-agent-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **🚧 Status**: MVP Development Phase - Building toward 30% cost savings validation

## Overview

`py-agent-client` is the core SDK of the Intelligent Agents Platform (IAP) ecosystem. It acts as an intelligent middleware layer that automatically routes AI requests to the optimal model/provider combination based on cost, quality, and speed requirements.

### Core Value Proposition

- **Automatic Cost Optimization**: Reduce AI API costs by 30%+ through intelligent routing
- **Zero Vendor Lock-in**: Switch between OpenAI, Anthropic, DeepSeek, and others seamlessly  
- **Performance Analytics**: Real-time ROI tracking and optimization insights
- **Smart Context Management**: Persistent memory and context optimization across sessions

## Quick Start

```python
from py_agent_client import Agent

# Initialize with your API keys
agent = Agent(
    api_key="your-api-key",
    providers={
        "openai": "sk-...",
        "anthropic": "sk-ant-...", 
        "deepseek": "sk-..."
    }
)

# Simple routing - automatically selects optimal model
result = agent.route(
    "Analyze Q3 sales data and find growth opportunities",
    context={"data": sales_data},
    optimize_for="quality"  # speed/cost/quality
)

print(result.response)
print(f"Cost: ${result.cost:.4f}")
print(f"Model used: {result.model}")
```

## Architecture & Strategy

### Phase 1: MVP Foundation (4 weeks, <1000 lines)

**Core Components:**
```
py_agent_client/
├── core/
│   ├── router.py          # Heuristic-based model selection
│   ├── cost_guardian.py   # Budget controls & cost tracking
│   ├── context_manager.py # Session memory & optimization
│   └── telemetry.py       # Usage analytics & insights
├── providers/
│   ├── openai_adapter.py  # OpenAI API wrapper
│   ├── anthropic_adapter.py
│   └── deepseek_adapter.py
└── client.py              # Main Agent class
```

**Strategic Focus:**
- **"Trojan Horse" Approach**: Start as a convenient abstraction layer
- **Data Collection**: Capture usage patterns for future ML optimization
- **Immediate Value**: Show cost savings from day 1 with simple heuristics

### Routing Strategy (MVP)

```python
# Initial heuristic rules (no ML required)
ROUTING_RULES = {
    "simple_qa": {"model": "gpt-3.5-turbo", "max_cost": 0.01},
    "code_generation": {"model": "gpt-4", "max_cost": 0.05},
    "analysis": {"model": "deepseek-coder", "max_cost": 0.02},
    "creative": {"model": "claude-3-sonnet", "max_cost": 0.03}
}
```

### Cost Guardian Implementation

```python
class CostGuardian:
    def __init__(self, daily_budget=50.0):
        self.daily_budget = daily_budget
        self.current_spend = 0.0
    
    def check_request(self, estimated_cost):
        if self.current_spend + estimated_cost > self.daily_budget:
            return self.suggest_cheaper_alternative()
        return True
    
    def track_spend(self, actual_cost):
        self.current_spend += actual_cost
```

## 30-Day Validation Experiment

### Objective
Demonstrate ≥30% cost savings across 3 real workloads

### Methodology
1. **Baseline Collection** (Week 1)
   - Deploy SDK with 500 diverse prompts
   - Record: GPT-4o vs GPT-3.5 vs DeepSeek performance
   - Establish cost/quality benchmarks

2. **Optimization Implementation** (Week 2-3)
   - Implement routing heuristics based on baseline data
   - Add fallback mechanisms for quality threshold failures
   - Deploy cost guardian with progressive budgeting

3. **Validation & Measurement** (Week 4)
   - A/B test: Direct API calls vs py-agent-client routing
   - Measure: cost reduction, quality maintenance, latency impact
   - Document case studies for 3 different workload types

### Success Metrics
- **Primary**: ≥30% cost reduction while maintaining quality score >0.85
- **Secondary**: <250ms additional latency, >95% routing accuracy
- **Tertiary**: Positive feedback from 3+ design partner interviews

## Development Roadmap

### Week 1-2: Core Infrastructure
- [ ] Basic Agent class with provider abstractions
- [ ] Simple routing logic with hardcoded rules
- [ ] Cost tracking and budget enforcement
- [ ] Basic telemetry collection

### Week 3: Provider Integrations
- [ ] OpenAI adapter with streaming support
- [ ] Anthropic Claude integration
- [ ] DeepSeek API wrapper
- [ ] Fallback mechanisms and error handling

### Week 4: Optimization & Testing
- [ ] Context management for session persistence
- [ ] Performance benchmarking suite
- [ ] Documentation and examples
- [ ] Design partner onboarding materials

### Post-MVP: Advanced Features
- [ ] ML-based routing optimization
- [ ] Custom fine-tuning integration
- [ ] Enterprise SSO and compliance features
- [ ] Self-hosted deployment options

## Risk Mitigation

### Technical Risks
- **Latency Overhead**: Implement caching and streaming to stay <250ms
- **API Changes**: Build adapter pattern for easy provider swapping
- **Quality Regression**: Implement quality scoring and automatic fallbacks

### Business Risks
- **Vendor Lock-in Perception**: Provide escape hatches and direct API access
- **Privacy Concerns**: Implement opt-in telemetry and local-only modes
- **Cold Start Problem**: Use public benchmarks and transparent heuristics initially

## Design Partners Program

**Target Profile**: Startups spending >$500/month on OpenAI APIs
**Commitment**: 30-day pilot with shared metrics and feedback sessions
**Benefits**: Free Pro tier, direct feature influence, case study participation

**Interested?** Email: partnerships@py-agent.dev

## Contributing

### Local Development
```bash
git clone https://github.com/py-agent/py-agent-client
cd py-agent-client
pip install -e ".[dev]"
pytest tests/
```

### Testing Strategy
- Unit tests for all routing logic
- Integration tests with real API calls (rate limited)
- Benchmark tests for performance regression detection
- End-to-end validation with sample workloads

## Monetization Model

### Tiers
- **Free**: 1,000 requests/month, basic routing
- **Pro** ($29/month): 50,000 requests, advanced optimization, analytics dashboard
- **Enterprise**: Custom pricing, self-hosted options, SLA guarantees

### Revenue Streams
- Subscription fees from Pro/Enterprise users
- Revenue sharing partnerships with AI providers
- Premium features: custom models, fine-tuning, priority support

## Data Network Effects

Every request captures:
- Task classification and context patterns
- Model performance vs cost trade-offs
- User optimization preferences and outcomes
- Quality feedback loops and failure modes

This data becomes our **sustainable competitive advantage** - the more usage, the better our routing decisions become.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- **Documentation**: [docs.py-agent.dev](https://docs.py-agent.dev)
- **Blog**: [blog.py-agent.dev](https://blog.py-agent.dev)
- **Status Page**: [status.py-agent.dev](https://status.py-agent.dev)
- **Discord**: [discord.gg/py-agent](https://discord.gg/py-agent)

---

**Built with ❤️ by the IAP team**

*Part of the broader py-agent ecosystem: `py-agent-core`, `py-agent-server`, `py-agent-tool`, `py-agent-resources`*