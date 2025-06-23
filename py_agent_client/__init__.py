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

from py_agent_client.client import Agent
from py_agent_client.models import RouteRequest, RouteResponse
from py_agent_client.core.cost_guardian import CostGuardian, BudgetExceededError
from py_agent_client.core.context_manager import ContextManager
from py_agent_client.core.telemetry import TelemetryCollector
from py_agent_client.exceptions import (
    PyAgentError,
    ProviderError,
    RoutingError,
    QualityThresholdError,
)

__version__ = "0.1.0"
__author__ = "py-agent Team"
__email__ = "hello@py-agent.com"
__license__ = "MIT"
__url__ = "https://py-agent.com"
__description__ = "Intelligent AI API routing with automatic cost optimization"

# Public API
__all__ = [
    # Core classes
    "Agent",
    "CostGuardian", 
    "ContextManager",
    "TelemetryCollector",
    
    # Data models
    "RouteRequest",
    "RouteResponse",
    
    # Exceptions
    "PyAgentError",
    "ProviderError", 
    "RoutingError",
    "QualityThresholdError",
    "BudgetExceededError",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__url__",
    "__description__",
]

# Version information
VERSION_INFO = tuple(map(int, __version__.split(".")))

# Configuration defaults
DEFAULT_CONFIG = {
    "routing": {
        "optimization_mode": "balanced",  # cost, quality, speed, balanced
        "quality_threshold": 0.7,
        "max_retries": 3,
        "timeout": 30.0,
    },
    "budget": {
        "daily_limit": 100.0,
        "monthly_limit": 1000.0,
        "alert_threshold": 0.8,
    },
    "providers": {
        "openai": {
            "enabled": True,
            "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            "max_tokens": 4096,
        },
        "anthropic": {
            "enabled": True, 
            "models": ["claude-3-sonnet", "claude-3-opus"],
            "max_tokens": 4096,
        },
        "deepseek": {
            "enabled": True,
            "models": ["deepseek-chat", "deepseek-coder"],
            "max_tokens": 4096,
        },
    },
    "telemetry": {
        "enabled": True,
        "batch_size": 100,
        "flush_interval": 300,  # seconds
    },
}

def get_version() -> str:
    """Get the package version."""
    return __version__

def get_version_info() -> tuple:
    """Get version information as a tuple."""
    return VERSION_INFO

def configure(config: dict = None) -> None:
    """
    Configure global settings for py-agent-client.
    
    Args:
        config: Configuration dictionary to override defaults
        
    Example:
        >>> import py_agent_client
        >>> py_agent_client.configure({
        ...     "routing": {"optimization_mode": "cost"},
        ...     "budget": {"daily_limit": 50.0}
        ... })
    """
    if config:
        # Deep merge configuration
        # Implementation would go here
        pass

# Package-level logging configuration
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Suppress warnings from dependencies by default
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("anthropic").setLevel(logging.WARNING)