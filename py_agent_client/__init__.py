"""
py-agent-client: Intelligent AI API routing with automatic cost optimization

This package provides intelligent routing between multiple AI providers (OpenAI,
Anthropic, DeepSeek) with automatic cost optimization, quality assurance, and
comprehensive analytics.

Basic Usage:
    >>> from py_agent_client import Agent
    >>> agent = Agent(api_key="your-key")
    >>> result = await agent.route("Explain quantum computing")
    >>> print(f"Response: {result.response}")
    >>> print(f"Cost: ${result.cost:.4f}")

Key Features:
    - Intelligent model routing for cost optimization
    - Real-time budget monitoring and controls
    - Quality threshold enforcement
    - Session context management
    - Comprehensive usage analytics
    - Provider failover and redundancy
"""
