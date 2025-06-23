"""
Test configuration and fixtures for py-agent-client
"""

from unittest.mock import AsyncMock, Mock

import pytest

from py_agent_client import Agent
from py_agent_client.core.context_manager import ContextManager
from py_agent_client.core.cost_guardian import CostGuardian
from py_agent_client.core.telemetry import TelemetryCollector


@pytest.fixture
def mock_api_keys():
    """Mock API keys for testing"""
    return {
        "openai": "sk-test-openai-key",
        "anthropic": "sk-ant-test-key",
        "deepseek": "sk-test-deepseek-key",
    }


@pytest.fixture
def mock_agent(mock_api_keys):
    """Create a mock Agent instance for testing"""
    agent = Agent(api_key="test-key", providers=mock_api_keys)
    return agent


@pytest.fixture
def cost_guardian():
    """Create a CostGuardian instance for testing"""
    return CostGuardian(daily_budget=100.0, monthly_budget=1000.0)


@pytest.fixture
def context_manager():
    """Create a ContextManager instance for testing"""
    return ContextManager()


@pytest.fixture
def telemetry_collector():
    """Create a TelemetryCollector instance for testing"""
    return TelemetryCollector()


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    return {
        "id": "chatcmpl-test123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-3.5-turbo",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a test response from OpenAI.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 20, "completion_tokens": 15, "total_tokens": 35},
    }


@pytest.fixture
def mock_anthropic_response():
    """Mock Anthropic API response"""
    return {
        "id": "msg_test123",
        "type": "message",
        "role": "assistant",
        "content": [
            {"type": "text", "text": "This is a test response from Anthropic."}
        ],
        "model": "claude-3-sonnet-20240229",
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": 20, "output_tokens": 15},
    }


@pytest.fixture
def sample_routing_request():
    """Sample routing request for testing"""
    return {
        "prompt": "Analyze the following data and provide insights",
        "context": {"data": [1, 2, 3, 4, 5]},
        "optimize_for": "cost",
        "max_cost": 0.05,
        "quality_threshold": 0.7,
    }


@pytest.fixture
def mock_httpx_client():
    """Mock httpx AsyncClient"""
    mock_client = AsyncMock()
    return mock_client


@pytest.fixture(autouse=True)
def disable_real_api_calls(monkeypatch):
    """Automatically disable real API calls in tests"""

    def mock_httpx_post(*args, **kwargs):
        raise RuntimeError("Real API calls are disabled in tests")

    monkeypatch.setattr("httpx.AsyncClient.post", mock_httpx_post)


@pytest.fixture
def example_prompts():
    """Collection of example prompts for testing"""
    return [
        {
            "prompt": "What is the capital of France?",
            "expected_category": "simple_qa",
            "expected_cost_tier": "low",
        },
        {
            "prompt": "Write a comprehensive analysis of machine learning trends in 2024",
            "expected_category": "analysis",
            "expected_cost_tier": "medium",
        },
        {
            "prompt": "Generate a Python function to implement a binary search tree",
            "expected_category": "code_generation",
            "expected_cost_tier": "medium",
        },
        {
            "prompt": "Write a creative short story about time travel",
            "expected_category": "creative",
            "expected_cost_tier": "high",
        },
    ]
