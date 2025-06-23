"""Cost management and budget controls"""

from datetime import datetime, timedelta
from typing import Any, Dict, List


class BudgetExceededError(Exception):
    """Exception raised when budget limits are exceeded"""

    def __init__(
        self,
        message: str = None,
        budget_type: str = "daily",
        current_spend: float = 0.0,
        budget_limit: float = 0.0,
        requested_cost: float = 0.0,
    ):
        # Handle both positional and keyword-only calls
        if message is None:
            message = f"{budget_type.title()} budget exceeded"
        super().__init__(message)
        self.budget_type = budget_type
        self.current_spend = current_spend
        self.budget_limit = budget_limit
        self.requested_cost = requested_cost


class CostGuardian:
    """Budget management and cost tracking"""

    def __init__(self, daily_budget: float = 100.0, monthly_budget: float = 1000.0):
        self.daily_budget = daily_budget
        self.monthly_budget = monthly_budget
        self.current_daily_spend = 0.0
        self.current_monthly_spend = 0.0
        self.spend_history: List[Dict[str, Any]] = []
        self.last_daily_reset = datetime.now()

    def check_request(self, estimated_cost: float) -> bool:
        """Check if request is within budget"""
        # Auto-reset daily budget if new day
        now = datetime.now()
        if (now - self.last_daily_reset).days >= 1:
            self.reset_daily_budget()

        if self.current_daily_spend + estimated_cost > self.daily_budget:
            raise BudgetExceededError(
                "Daily budget exceeded",
                budget_type="daily",
                current_spend=self.current_daily_spend,
                budget_limit=self.daily_budget,
                requested_cost=estimated_cost,
            )

        if self.current_monthly_spend + estimated_cost > self.monthly_budget:
            raise BudgetExceededError(
                "Monthly budget exceeded",
                budget_type="monthly",
                current_spend=self.current_monthly_spend,
                budget_limit=self.monthly_budget,
                requested_cost=estimated_cost,
            )

        return True

    def track_spend(self, actual_cost: float) -> None:
        """Track actual spending"""
        self.current_daily_spend += actual_cost
        self.current_monthly_spend += actual_cost

        # Record in history
        self.spend_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "cost": actual_cost,
                "daily_total": self.current_daily_spend,
                "monthly_total": self.current_monthly_spend,
            }
        )

    def get_remaining_budget(self) -> tuple:
        """Get remaining daily and monthly budget"""
        daily_remaining = self.daily_budget - self.current_daily_spend
        monthly_remaining = self.monthly_budget - self.current_monthly_spend
        return daily_remaining, monthly_remaining

    def suggest_cheaper_alternative(
        self, original_model: str, estimated_cost: float
    ) -> List[Dict[str, Any]]:
        """Suggest cheaper alternatives"""
        alternatives = [
            {"model": "gpt-3.5-turbo", "estimated_cost": estimated_cost * 0.1},
            {"model": "deepseek-chat", "estimated_cost": estimated_cost * 0.05},
        ]
        return [alt for alt in alternatives if alt["estimated_cost"] < estimated_cost]

    def reset_daily_budget(self) -> None:
        """Reset daily budget"""
        self.current_daily_spend = 0.0
        self.last_daily_reset = datetime.now()

    def reset_monthly_budget(self) -> None:
        """Reset monthly budget"""
        self.current_monthly_spend = 0.0

    def set_budget_limits(self, daily: float, monthly: float) -> None:
        """Set budget limits"""
        self.daily_budget = daily
        self.monthly_budget = monthly

    def get_usage_percentage(self) -> tuple:
        """Get usage percentage of budgets"""
        daily_pct = (self.current_daily_spend / self.daily_budget) * 100
        monthly_pct = (self.current_monthly_spend / self.monthly_budget) * 100
        return daily_pct, monthly_pct

    def estimate_cost_for_tokens(
        self, model: str, input_tokens: int, output_tokens: int
    ) -> float:
        """Estimate cost for token count"""
        pricing = {
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        }

        rates = pricing.get(model, {"input": 0.001, "output": 0.002})
        total_cost = (input_tokens / 1000) * rates["input"] + (
            output_tokens / 1000
        ) * rates["output"]
        return total_cost

    def estimate_cost_for_prompt(self, model: str, prompt: str) -> float:
        """Estimate cost for prompt"""
        # Rough estimation: 1 token per 4 characters
        input_tokens = len(prompt) // 4
        output_tokens = input_tokens // 2  # Assume shorter response
        return self.estimate_cost_for_tokens(model, input_tokens, output_tokens)

    def get_spend_history(self) -> List[Dict[str, Any]]:
        """Get spending history"""
        return self.spend_history.copy()

    def export_budget_report(self) -> Dict[str, Any]:
        """Export budget report"""
        daily_remaining, monthly_remaining = self.get_remaining_budget()

        return {
            "daily_budget": self.daily_budget,
            "monthly_budget": self.monthly_budget,
            "daily_spend": self.current_daily_spend,
            "monthly_spend": self.current_monthly_spend,
            "daily_remaining": daily_remaining,
            "monthly_remaining": monthly_remaining,
            "total_transactions": len(self.spend_history),
            "last_updated": datetime.now().isoformat(),
        }

    def get_budget_recommendations(self) -> Dict[str, Any]:
        """Get intelligent budget recommendations"""
        if not self.spend_history:
            return {
                "suggested_daily_budget": self.daily_budget,
                "suggested_monthly_budget": self.monthly_budget,
                "reasoning": "No usage history available",
            }

        # Simple recommendations based on usage
        avg_daily_spend = self.current_daily_spend
        suggested_daily = avg_daily_spend * 1.2  # 20% buffer
        suggested_monthly = suggested_daily * 30

        return {
            "suggested_daily_budget": suggested_daily,
            "suggested_monthly_budget": suggested_monthly,
            "reasoning": f"Based on current daily spend of ${avg_daily_spend:.4f}",
        }
