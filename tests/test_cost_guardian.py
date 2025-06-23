"""
Tests for the CostGuardian component
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from py_agent_client.core.cost_guardian import CostGuardian, BudgetExceededError


class TestCostGuardian:
    """Test cases for CostGuardian"""

    def test_initialization(self):
        """Test CostGuardian initialization"""
        guardian = CostGuardian(daily_budget=50.0, monthly_budget=500.0)
        
        assert guardian.daily_budget == 50.0
        assert guardian.monthly_budget == 500.0
        assert guardian.current_daily_spend == 0.0
        assert guardian.current_monthly_spend == 0.0

    def test_initialization_with_defaults(self):
        """Test CostGuardian with default values"""
        guardian = CostGuardian()
        
        assert guardian.daily_budget == 100.0  # Default
        assert guardian.monthly_budget == 1000.0  # Default

    def test_check_request_within_budget(self, cost_guardian):
        """Test request check when within budget"""
        result = cost_guardian.check_request(estimated_cost=10.0)
        
        assert result is True

    def test_check_request_exceeds_daily_budget(self, cost_guardian):
        """Test request check when exceeding daily budget"""
        # Set current spend close to limit
        cost_guardian.current_daily_spend = 95.0
        
        with pytest.raises(BudgetExceededError, match="Daily budget exceeded"):
            cost_guardian.check_request(estimated_cost=10.0)

    def test_check_request_exceeds_monthly_budget(self, cost_guardian):
        """Test request check when exceeding monthly budget"""
        # Set current spend close to limit
        cost_guardian.current_monthly_spend = 995.0
        
        with pytest.raises(BudgetExceededError, match="Monthly budget exceeded"):
            cost_guardian.check_request(estimated_cost=10.0)

    def test_track_spend(self, cost_guardian):
        """Test spend tracking"""
        initial_daily = cost_guardian.current_daily_spend
        initial_monthly = cost_guardian.current_monthly_spend
        
        cost_guardian.track_spend(actual_cost=5.50)
        
        assert cost_guardian.current_daily_spend == initial_daily + 5.50
        assert cost_guardian.current_monthly_spend == initial_monthly + 5.50

    def test_get_remaining_budget(self, cost_guardian):
        """Test getting remaining budget"""
        cost_guardian.current_daily_spend = 25.0
        cost_guardian.current_monthly_spend = 150.0
        
        daily_remaining, monthly_remaining = cost_guardian.get_remaining_budget()
        
        assert daily_remaining == 75.0  # 100 - 25
        assert monthly_remaining == 850.0  # 1000 - 150

    def test_suggest_cheaper_alternative(self, cost_guardian):
        """Test getting cheaper alternatives"""
        alternatives = cost_guardian.suggest_cheaper_alternative(
            original_model="gpt-4",
            estimated_cost=0.05
        )
        
        assert isinstance(alternatives, list)
        assert len(alternatives) > 0
        
        # Check that suggested alternatives are actually cheaper
        for alt in alternatives:
            assert alt["estimated_cost"] < 0.05

    def test_reset_daily_budget(self, cost_guardian):
        """Test resetting daily budget"""
        cost_guardian.current_daily_spend = 50.0
        cost_guardian.reset_daily_budget()
        
        assert cost_guardian.current_daily_spend == 0.0

    def test_reset_monthly_budget(self, cost_guardian):
        """Test resetting monthly budget"""
        cost_guardian.current_monthly_spend = 200.0
        cost_guardian.reset_monthly_budget()
        
        assert cost_guardian.current_monthly_spend == 0.0

    def test_set_budget_limits(self, cost_guardian):
        """Test updating budget limits"""
        cost_guardian.set_budget_limits(daily=75.0, monthly=750.0)
        
        assert cost_guardian.daily_budget == 75.0
        assert cost_guardian.monthly_budget == 750.0

    def test_get_usage_percentage(self, cost_guardian):
        """Test getting usage percentage"""
        cost_guardian.current_daily_spend = 30.0
        cost_guardian.current_monthly_spend = 200.0
        
        daily_pct, monthly_pct = cost_guardian.get_usage_percentage()
        
        assert daily_pct == 30.0  # 30/100 * 100
        assert monthly_pct == 20.0  # 200/1000 * 100

    def test_estimate_cost_for_tokens(self, cost_guardian):
        """Test cost estimation for token count"""
        cost = cost_guardian.estimate_cost_for_tokens(
            model="gpt-3.5-turbo",
            input_tokens=100,
            output_tokens=50
        )
        
        assert isinstance(cost, float)
        assert cost > 0

    def test_estimate_cost_for_prompt(self, cost_guardian):
        """Test cost estimation for prompt"""
        cost = cost_guardian.estimate_cost_for_prompt(
            model="gpt-3.5-turbo",
            prompt="This is a test prompt for cost estimation"
        )
        
        assert isinstance(cost, float)
        assert cost > 0

    @patch('py_agent_client.core.cost_guardian.datetime')
    def test_auto_reset_daily_budget(self, mock_datetime, cost_guardian):
        """Test automatic daily budget reset"""
        # Set up mock to simulate new day
        yesterday = datetime.now() - timedelta(days=1)
        today = datetime.now()
        
        cost_guardian.last_daily_reset = yesterday
        cost_guardian.current_daily_spend = 50.0
        
        mock_datetime.now.return_value = today
        
        # This should trigger auto-reset
        cost_guardian.check_request(10.0)
        
        assert cost_guardian.current_daily_spend == 0.0

    def test_budget_exceeded_error(self):
        """Test BudgetExceededError exception"""
        error = BudgetExceededError(
            budget_type="daily",
            current_spend=105.0,
            budget_limit=100.0,
            requested_cost=10.0
        )
        
        assert error.budget_type == "daily"
        assert error.current_spend == 105.0
        assert error.budget_limit == 100.0
        assert error.requested_cost == 10.0

    def test_get_spend_history(self, cost_guardian):
        """Test getting spend history"""
        # Add some spend
        cost_guardian.track_spend(10.0)
        cost_guardian.track_spend(5.0)
        
        history = cost_guardian.get_spend_history()
        
        assert isinstance(history, list)
        assert len(history) >= 2

    def test_export_budget_report(self, cost_guardian):
        """Test exporting budget report"""
        cost_guardian.current_daily_spend = 45.0
        cost_guardian.current_monthly_spend = 300.0
        
        report = cost_guardian.export_budget_report()
        
        assert "daily_budget" in report
        assert "monthly_budget" in report
        assert "daily_spend" in report
        assert "monthly_spend" in report
        assert "daily_remaining" in report
        assert "monthly_remaining" in report

    def test_intelligent_budget_recommendations(self, cost_guardian):
        """Test intelligent budget recommendations"""
        # Simulate usage patterns
        for _ in range(10):
            cost_guardian.track_spend(2.5)  # 25.0 total
        
        recommendations = cost_guardian.get_budget_recommendations()
        
        assert isinstance(recommendations, dict)
        assert "suggested_daily_budget" in recommendations
        assert "suggested_monthly_budget" in recommendations
        assert "reasoning" in recommendations