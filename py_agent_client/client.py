"""Main Agent class for py-agent-client"""

import time
import uuid
from typing import Any, Dict, Optional

from py_agent_client.core.context_manager import ContextManager
from py_agent_client.core.cost_guardian import CostGuardian
from py_agent_client.core.router import Router
from py_agent_client.core.telemetry import TelemetryCollector


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
        context: Optional[Dict[str, Any]] = None,
        optimize_for: str = "balanced",
        max_cost: Optional[float] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Route request to optimal AI provider."""
        start_time = time.time()
        request_id = str(uuid.uuid4())

        # Create route request
        route_request = {
            "prompt": prompt,
            "context": context,
            "optimize_for": optimize_for,
            "max_cost": max_cost,
        }

        try:
            result = await self._execute_route(route_request)
            result["request_id"] = request_id
            result["response_time"] = time.time() - start_time

            # Track metrics
            self.telemetry.record_request(
                {
                    "request_id": request_id,
                    "cost": result.get("cost", 0),
                    "tokens_used": result.get("tokens_used", 0),
                    "model": result.get("model"),
                    "quality_score": result.get("quality_score", 0),
                }
            )

            return result

        except Exception as e:
            # Record error and re-raise
            self.telemetry.record_request({"request_id": request_id, "error": str(e)})
            raise

    async def _execute_route(self, route_request: Dict[str, Any]) -> Dict[str, Any]:
        """Execute routing logic"""
        prompt = route_request["prompt"]

        # Get routing decision
        routing_decision = self.router.route_request(
            prompt,
            optimize_for=route_request.get("optimize_for", "balanced"),
            max_cost=route_request.get("max_cost"),
        )

        # Check budget
        estimated_cost = routing_decision.get("max_cost", 0.001)
        self.cost_guardian.check_request(estimated_cost)

        # Mock response (TODO: implement actual provider calls)
        response = {
            "response": f"Mock response for: {prompt[:50]}...",
            "model": routing_decision["model"],
            "provider": routing_decision["provider"],
            "cost": estimated_cost * 0.8,  # Simulate cost optimization
            "tokens_used": len(prompt.split()) + 20,
            "quality_score": 0.85,
            "routing_reason": routing_decision["routing_reason"],
        }

        # Track spending
        self.cost_guardian.track_spend(response["cost"])

        return response

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
