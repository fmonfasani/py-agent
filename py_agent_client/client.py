"""Main Agent class for py-agent-client."""

from __future__ import annotations

import time
import uuid
from typing import Any, Dict, Optional

from py_agent_client.core.context_manager import ContextManager
from py_agent_client.core.cost_guardian import CostGuardian
from py_agent_client.core.router import Router
from py_agent_client.core.telemetry import Telemetry  # antes TelemetryCollector
from py_agent_client.models import RouteRequest, RouteResponse


class Agent:
    """Intelligent AI-API routing agent."""

    def __init__(self, api_key: str, providers: Optional[Dict[str, str]] = None) -> None:
        if not api_key:
            raise ValueError("API key cannot be empty")

        self.api_key: str = api_key
        self.providers: Dict[str, str] = providers or {}

        # Core components
        self.cost_guardian = CostGuardian()
        self.context_manager = ContextManager()
        self.telemetry = Telemetry()
        self.router = Router()

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    async def route(
        self,
        prompt: str,
        *,
        context: Optional[Dict[str, Any]] = None,
        optimize_for: str = "balanced",
        max_cost: Optional[float] = None,
        **kwargs,
    ) -> RouteResponse:
        """Route a prompt and return a `RouteResponse` instance."""
        request_id = str(uuid.uuid4())
        started_at = time.time()

        # Build high-level request model
        req = RouteRequest(
            prompt=prompt,
            context=context,
            optimize_for=optimize_for,
            max_cost=max_cost,
        )

        try:
            # Call the internal executor (can be monkey-patched in tests)
            result = await self._execute_route(req, **kwargs)

            # Ensure result is a RouteResponse
            if isinstance(result, dict):
                result = RouteResponse(**result)

            # Enrich with timing / ids
            result.request_id = request_id
            result.response_time = time.time() - started_at

            # Telemetry
            self.telemetry.record(
                event_type="route",
                payload={
                    "request_id": request_id,
                    "model": result.model,
                    "provider": result.provider,
                    "cost": result.cost,
                    "tokens": result.tokens_used,
                    "quality": result.quality_score,
                },
            )
            return result

        except Exception as exc:
            # Telemetry for error paths
            self.telemetry.record(
                event_type="error",
                payload={"request_id": request_id, "error": str(exc)},
            )
            raise

    def get_usage_stats(self) -> Dict[str, Any]:
        return self.telemetry.get_stats()

    def set_budget(self, *, daily: Optional[float] = None, monthly: Optional[float] = None) -> None:
        self.cost_guardian.set_budget_limits(daily=daily, monthly=monthly)

    def clear_context(self, session_id: Optional[str] = None) -> None:
        self.context_manager.clear_context(session_id)

    # --------------------------------------------------------------------- #
    # Internals
    # --------------------------------------------------------------------- #
    async def _execute_route(self, req: RouteRequest, **kwargs) -> RouteResponse | Dict[str, Any]:
        """Choose a provider, enforce budgets and return a mock response.

        In real code this would call the selected LLM provider.
        """
        decision = self.router.route_request(
            req.prompt,
            optimize_for=req.optimize_for,
            max_cost=req.max_cost,
        )

        est_cost = decision.get("max_cost", 0.001)
        self.cost_guardian.check_request(est_cost)  # will raise on overflow
        self.cost_guardian.track_spend(est_cost)

        # ---- Mock provider call ------------------------------------------------
        return {
            "response": f"Mock response for: {req.prompt[:50]}…",
            "model": decision["model"],
            "provider": decision["provider"],
            "cost": est_cost * 0.8,  # pretend we saved 20 %
            "tokens_used": len(req.prompt.split()) + 20,
            "quality_score": 0.85,
            "routing_reason": decision["routing_reason"],
        }
