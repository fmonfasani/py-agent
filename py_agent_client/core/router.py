"""Intelligent routing logic for AI providers"""

from typing import Dict, Any, Optional, List


class Router:
    """Routes requests to optimal AI providers"""
    
    def __init__(self):
        self.routing_rules = {
            "simple_qa": {"model": "gpt-3.5-turbo", "max_cost": 0.01},
            "code_generation": {"model": "gpt-4", "max_cost": 0.05},
            "analysis": {"model": "deepseek-coder", "max_cost": 0.02},
            "creative": {"model": "claude-3-sonnet", "max_cost": 0.03}
        }
    
    def route_request(
        self, 
        prompt: str, 
        optimize_for: str = "balanced",
        max_cost: Optional[float] = None
    ) -> Dict[str, Any]:
        """Route request to optimal provider"""
        
        # Simple heuristic routing (MVP)
        if "code" in prompt.lower() or "function" in prompt.lower():
            category = "code_generation"
        elif "analyze" in prompt.lower() or "analysis" in prompt.lower():
            category = "analysis"
        elif len(prompt.split()) < 20 and "?" in prompt:
            category = "simple_qa"
        else:
            category = "creative"
        
        rule = self.routing_rules.get(category, self.routing_rules["simple_qa"])
        
        return {
            "model": rule["model"],
            "provider": self._get_provider_for_model(rule["model"]),
            "max_cost": rule["max_cost"],
            "routing_reason": f"{category}_optimized"
        }
    
    def _get_provider_for_model(self, model: str) -> str:
        """Get provider name for a model"""
        if "gpt" in model:
            return "openai"
        elif "claude" in model:
            return "anthropic"
        elif "deepseek" in model:
            return "deepseek"
        else:
            return "openai"  # default