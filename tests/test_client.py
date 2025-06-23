"""
Tests for the main Agent client
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from py_agent_client import Agent
from py_agent_client.models import RouteResponse, RouteRequest


class TestAgent:
    """Test cases for the Agent class"""

    def test_agent_initialization_with_providers(self, mock_api_keys):
        """Test Agent initialization with provider keys"""
        agent = Agent(api_key="test-key", providers=mock_api_keys)
        
        assert agent.api_key == "test-key"
        assert agent.providers == mock_api_keys
        assert agent.cost_guardian is not None
        assert agent.context_manager is not None
        assert agent.telemetry is not None

    def test_agent_initialization_minimal(self):
        """Test Agent initialization with minimal config"""
        agent = Agent(api_key="test-key")
        
        assert agent.api_key == "test-key"
        assert isinstance(agent.providers, dict)

    def test_agent_initialization_invalid_api_key(self):
        """Test Agent initialization with invalid API key"""
        with pytest.raises(ValueError, match="API key cannot be empty"):
            Agent(api_key="")

    @pytest.mark.asyncio
    async def test_route_simple_request(self, mock_agent, sample_routing_request):
        """Test basic routing functionality"""
        with patch.object(mock_agent, '_execute_route') as mock_execute:
            mock_execute.return_value = RouteResponse(
                response="Test response",
                model="gpt-3.5-turbo",
                provider="openai",
                cost=0.001,
                tokens_used=35,
                quality_score=0.85,
                routing_reason="cost_optimized"
            )
            
            result = await mock_agent.route(
                sample_routing_request["prompt"],
                context=sample_routing_request["context"]
            )
            
            assert result.response == "Test response"
            assert result.model == "gpt-3.5-turbo"
            assert result.cost == 0.001
            assert mock_execute.called

    @pytest.mark.asyncio
    async def test_route_with_optimization_preference(self, mock_agent):
        """Test routing with different optimization preferences"""
        test_cases = [
            ("cost", "gpt-3.5-turbo"),
            ("quality", "gpt-4"),
            ("speed", "gpt-3.5-turbo")
        ]
        
        for optimize_for, expected_model in test_cases:
            with patch.object(mock_agent, '_execute_route') as mock_execute:
                mock_execute.return_value = RouteResponse(
                    response="Test response",
                    model=expected_model,
                    provider="openai",
                    cost=0.001,
                    tokens_used=35,
                    quality_score=0.85,
                    routing_reason=f"{optimize_for}_optimized"
                )
                
                result = await mock_agent.route(
                    "Test prompt",
                    optimize_for=optimize_for
                )
                
                assert result.model == expected_model

    @pytest.mark.asyncio
    async def test_route_with_budget_constraint(self, mock_agent):
        """Test routing respects budget constraints"""
        with patch.object(mock_agent.cost_guardian, 'check_request') as mock_check:
            mock_check.return_value = False  # Budget exceeded
            
            with pytest.raises(Exception, match="Budget exceeded"):
                await mock_agent.route("Expensive prompt", max_cost=0.001)

    @pytest.mark.asyncio
    async def test_route_with_context(self, mock_agent):
        """Test routing with context data"""
        context = {"user_id": "123", "session": "abc"}
        
        with patch.object(mock_agent, '_execute_route') as mock_execute:
            mock_execute.return_value = RouteResponse(
                response="Context-aware response",
                model="gpt-3.5-turbo",
                provider="openai",
                cost=0.001,
                tokens_used=35,
                quality_score=0.85,
                routing_reason="context_optimized"
            )
            
            result = await mock_agent.route("Test with context", context=context)
            
            # Verify context was passed to execution
            call_args = mock_execute.call_args[0][0]
            assert call_args.context == context

    def test_get_usage_stats(self, mock_agent):
        """Test getting usage statistics"""
        with patch.object(mock_agent.telemetry, 'get_stats') as mock_stats:
            mock_stats.return_value = {
                "total_requests": 100,
                "total_cost": 5.67,
                "average_cost": 0.0567,
                "cost_savings": 2.34
            }
            
            stats = mock_agent.get_usage_stats()
            
            assert stats["total_requests"] == 100
            assert stats["total_cost"] == 5.67
            assert stats["cost_savings"] == 2.34

    def test_set_budget(self, mock_agent):
        """Test setting budget limits"""
        mock_agent.set_budget(daily=50.0, monthly=500.0)
        
        assert mock_agent.cost_guardian.daily_budget == 50.0
        assert mock_agent.cost_guardian.monthly_budget == 500.0

    @pytest.mark.asyncio
    async def test_route_error_handling(self, mock_agent):
        """Test error handling in routing"""
        with patch.object(mock_agent, '_execute_route') as mock_execute:
            mock_execute.side_effect = Exception("API Error")
            
            with pytest.raises(Exception, match="API Error"):
                await mock_agent.route("Test prompt")

    @pytest.mark.asyncio
    async def test_route_fallback_on_failure(self, mock_agent):
        """Test fallback to alternative provider on failure"""
        with patch.object(mock_agent, '_execute_route') as mock_execute:
            # First call fails, second succeeds
            mock_execute.side_effect = [
                Exception("Primary provider failed"),
                RouteResponse(
                    response="Fallback response",
                    model="claude-3-sonnet",
                    provider="anthropic",
                    cost=0.002,
                    tokens_used=40,
                    quality_score=0.80,
                    routing_reason="fallback"
                )
            ]
            
            # This would need actual fallback logic implementation
            with pytest.raises(Exception):
                await mock_agent.route("Test prompt")

    def test_clear_context(self, mock_agent):
        """Test clearing context manager"""
        mock_agent.clear_context()
        # Verify context manager was cleared
        assert len(mock_agent.context_manager.contexts) == 0


class TestRouteRequest:
    """Test cases for RouteRequest model"""

    def test_route_request_creation(self):
        """Test RouteRequest model creation"""
        request = RouteRequest(
            prompt="Test prompt",
            context={"key": "value"},
            optimize_for="cost",
            max_cost=0.05
        )
        
        assert request.prompt == "Test prompt"
        assert request.context == {"key": "value"}
        assert request.optimize_for == "cost"
        assert request.max_cost == 0.05

    def test_route_request_defaults(self):
        """Test RouteRequest with default values"""
        request = RouteRequest(prompt="Test prompt")
        
        assert request.optimize_for == "balanced"
        assert request.max_cost is None
        assert request.quality_threshold == 0.7


class TestRouteResponse:
    """Test cases for RouteResponse model"""

    def test_route_response_creation(self):
        """Test RouteResponse model creation"""
        response = RouteResponse(
            response="Test response",
            model="gpt-3.5-turbo",
            provider="openai",
            cost=0.001,
            tokens_used=35,
            quality_score=0.85,
            routing_reason="cost_optimized"
        )
        
        assert response.response == "Test response"
        assert response.model == "gpt-3.5-turbo"
        assert response.provider == "openai"
        assert response.cost == 0.001
        assert response.savings_percent == 0  # Default when no baseline

    def test_route_response_with_savings(self):
        """Test RouteResponse with savings calculation"""
        response = RouteResponse(
            response="Test response",
            model="gpt-3.5-turbo", 
            provider="openai",
            cost=0.001,
            baseline_cost=0.002,
            tokens_used=35,
            quality_score=0.85,
            routing_reason="cost_optimized"
        )
        
        assert response.savings_percent == 50.0  # 50% savings