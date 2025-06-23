"""Main Agent class for py-agent-client"""

import time
import uuid
from typing import Any, Dict, Optional

from py_agent_client.core.context_manager import ContextManager
from py_agent_client.core.cost_guardian import CostGuardian
from py_agent_client.core.router import Router
from py_agent_client.core.telemetry import TelemetryCollector
from py_agent_client.models import RouteRequest, RouteResponse


class Agent:
    """Intelligent AI API routing agent"""

    def __init__(self, api_key: str, providers: Optional[Dict[str, str]] = None):
        """Initialize the Agent with API keys."""
        if not api_key:
            raise ValueError("API key cannot be empty")

        self.api_key = api_key
        self.providers = providers or {}

        # Initialize core components
        self.cost_guardian = CostGuardian()
        self.context_manager = ContextManager()
        self.telemetry = TelemetryCollector()
        self.router = Router()

    async def route(
        self,
        prompt: str,
        *,
        context: Optional[Dict[str, Any]] = None,
        optimize_for: str = "balanced",
        max_cost: Optional[float] = None,
    ) -> RouteResponse:
        """Route request to optimal AI provider."""
        # Check budget first
        estimated_cost = 0.001
        budget_ok = self.cost_guardian.check_request(estimated_cost)
        if budget_ok is False:
            raise Exception("Budget exceeded")

        # Track spending
        self.cost_guardian.track_spend(estimated_cost)

        # Create RouteRequest object
        request = RouteRequest(
            prompt=prompt,
            context=context,
            optimize_for=optimize_for,
            max_cost=max_cost,
        )

        # Execute routing
        result = await self._execute_route(request)

        # Ensure we return RouteResponse
        if isinstance(result, dict):
            result = RouteResponse(**result)

        # Record telemetry
        self.telemetry.record_request(
            {
                "request_id": getattr(result, "request_id", str(uuid.uuid4())),
                "cost": getattr(result, "cost", estimated_cost),
                "tokens_used": getattr(result, "tokens_used", len(prompt.split())),
                "model": getattr(result, "model", "unknown"),
                "quality_score": getattr(result, "quality_score", 0.85),
            }
        )

        return result

    async def _execute_route(self, request: RouteRequest) -> Dict[str, Any]:
        """Execute routing logic"""
        # Get routing decision
        routing_decision = self.router.route_request(
            request.prompt,
            optimize_for=request.optimize_for,
            max_cost=request.max_cost,
        )

        # Mock response (TODO: implement actual provider calls)
        return {
            "response": f"Mock response for: {request.prompt[:50]}...",
            "model": routing_decision["model"],
            "provider": routing_decision["provider"],
            "cost": 0.001,
            "tokens_used": len(request.prompt.split()) + 20,
            "quality_score": 0.85,
            "routing_reason": routing_decision["routing_reason"],
            "response_time": 1.2,
            "request_id": str(uuid.uuid4()),
        }

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return self.telemetry.get_stats()

    def set_budget(
        self, daily: Optional[float] = None, monthly: Optional[float] = None
    ):
        """Set budget limits"""
        if daily is not None:
            self.cost_guardian.daily_budget = daily
        if monthly is not None:
            self.cost_guardian.monthly_budget = monthly

    def clear_context(self, session_id: Optional[str] = None):
        """Clear context manager"""
        self.context_manager.clear_context(session_id)

    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data"""
        return {
            "efficiency_score": 0.85,
            "best_model_for_cost": "gpt-3.5-turbo",
            "best_model_for_quality": "gpt-4",
            "avg_response_time": 1.2,
        }

    def get_recommendations(self) -> list:
        """Get optimization recommendations"""
        return [
            "Consider using gpt-3.5-turbo for simple queries",
            "Enable context compression for better efficiency",
            "Set budget alerts at 80% threshold",
        ]
