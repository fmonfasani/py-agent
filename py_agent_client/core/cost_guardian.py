"""Cost management and budget controls"""

from typing import Any, Dict


class BudgetExceededError(Exception):
    """Exception raised when budget limits are exceeded"""

    def __init__(self, message: str, budget_type: str = "daily"):
        super().__init__(message)
        self.budget_type = budget_type


class CostGuardian:
    """Budget management and cost tracking"""

    def __init__(self, daily_budget: float = 100.0, monthly_budget: float = 1000.0):
        self.daily_budget = daily_budget
        self.monthly_budget = monthly_budget
        self.current_daily_spend = 0.0
        self.current_monthly_spend = 0.0

    def check_request(self, estimated_cost: float) -> bool:
        """Check if request is within budget"""
        if self.current_daily_spend + estimated_cost > self.daily_budget:
            raise BudgetExceededError("Daily budget exceeded")
        return True

    def track_spend(self, actual_cost: float) -> None:
        """Track actual spending"""
        self.current_daily_spend += actual_cost
        self.current_monthly_spend += actual_cost

    def get_remaining_budget(self) -> tuple:
        """Get remaining daily and monthly budget"""
        daily_remaining = self.daily_budget - self.current_daily_spend
        monthly_remaining = self.monthly_budget - self.current_monthly_spend
        return daily_remaining, monthly_remaining
