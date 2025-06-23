"""
Data models for py-agent-client

This module defines Pydantic models for request/response data structures,
configuration objects, and internal data representations.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


class OptimizationMode(str, Enum):
    """Optimization modes for request routing."""
    COST = "cost"
    QUALITY = "quality"
    SPEED = "speed"
    BALANCED = "balanced"


class ProviderName(str, Enum):
    """Supported AI providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"


class RouteRequest(BaseModel):
    """Request model for AI routing."""
    
    prompt: str = Field(..., description="The prompt to send to the AI model")
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context data for the request"
    )
    optimize_for: OptimizationMode = Field(
        default=OptimizationMode.BALANCED,
        description="Optimization preference for routing"
    )
    max_cost: Optional[float] = Field(
        default=None,
        ge=0,
        description="Maximum cost limit for this request"
    )
    quality_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum quality score required"
    )
    timeout: Optional[float] = Field(
        default=30.0,
        gt=0,
        description="Request timeout in seconds"
    )
    max_tokens: Optional[int] = Field(
        default=None,
        gt=0,
        description="Maximum tokens in response"
    )
    temperature: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=2.0,
        description="Temperature for response generation"
    )
    preferred_providers: Optional[List[ProviderName]] = Field(
        default=None,
        description="Preferred providers in order of preference"
    )
    excluded_providers: Optional[List[ProviderName]] = Field(
        default=None,
        description="Providers to exclude from routing"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for context management"
    )
    user_id: Optional[str] = Field(
        default=None,
        description="User ID for personalization"
    )
    
    @validator('prompt')
    def prompt_not_empty(cls, v):
        """Validate that prompt is not empty."""
        if not v or not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()
    
    @validator('preferred_providers', 'excluded_providers')
    def validate_provider_lists(cls, v):
        """Validate provider lists don't conflict."""
        if v is not None:
            # Remove duplicates while preserving order
            seen = set()
            return [x for x in v if not (x in seen or seen.add(x))]
        return v


class RouteResponse(BaseModel):
    """Response model for AI routing."""
    
    response: str = Field(..., description="The AI model's response")
    model: str = Field(..., description="Model that generated the response")
    provider: ProviderName = Field(..., description="Provider that served the request")
    cost: float = Field(..., ge=0, description="Cost of the request in USD")
    tokens_used: int = Field(..., ge=0, description="Total tokens used")
    quality_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Estimated quality score of the response"
    )
    routing_reason: str = Field(
        ...,
        description="Reason why this model/provider was selected"
    )
    response_time: float = Field(
        ...,
        ge=0,
        description="Response time in seconds"
    )
    baseline_cost: Optional[float] = Field(
        default=None,
        ge=0,
        description="What the cost would have been with default routing"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID used for this request"
    )
    request_id: str = Field(..., description="Unique identifier for this request")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def savings_percent(self) -> float:
        """Calculate percentage savings compared to baseline."""
        if self.baseline_cost and self.baseline_cost > 0:
            return ((self.baseline_cost - self.cost) / self.baseline_cost) * 100
        return 0.0
    
    @property
    def cost_per_token(self) -> float:
        """Calculate cost per token."""
        if self.tokens_used > 0:
            return self.cost / self.tokens_used
        return 0.0


class ModelInfo(BaseModel):
    """Information about an AI model."""
    
    name: str = Field(..., description="Model name")
    provider: ProviderName = Field(..., description="Provider of the model")
    cost_per_input_token: float = Field(..., ge=0, description="Cost per input token")
    cost_per_output_token: float = Field(..., ge=0, description="Cost per output token")
    max_tokens: int = Field(..., gt=0, description="Maximum tokens supported")
    context_window: int = Field(..., gt=0, description="Context window size")
    quality_tier: str = Field(..., description="Quality tier (low, medium, high)")
    speed_tier: str = Field(..., description="Speed tier (slow, medium, fast)")
    capabilities: List[str] = Field(
        default_factory=list,
        description="Model capabilities (code, analysis, creative, etc.)"
    )
    enabled: bool = Field(default=True, description="Whether model is enabled")


class ProviderConfig(BaseModel):
    """Configuration for an AI provider."""
    
    name: ProviderName = Field(..., description="Provider name")
    api_key: str = Field(..., description="API key for the provider")
    base_url: Optional[str] = Field(default=None, description="Custom base URL")
    enabled: bool = Field(default=True, description="Whether provider is enabled")
    max_requests_per_minute: Optional[int] = Field(
        default=None,
        gt=0,
        description="Rate limit for requests per minute"
    )
    timeout: float = Field(default=30.0, gt=0, description="Request timeout")
    retry_attempts: int = Field(
        default=3,
        ge=0,
        description="Number of retry attempts"
    )
    models: List[ModelInfo] = Field(
        default_factory=list,
        description="Available models for this provider"
    )


class BudgetConfig(BaseModel):
    """Budget configuration."""
    
    daily_limit: float = Field(
        default=100.0,
        ge=0,
        description="Daily spending limit in USD"
    )
    monthly_limit: float = Field(
        default=1000.0,
        ge=0,
        description="Monthly spending limit in USD"
    )
    alert_threshold: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Alert when this percentage of budget is used"
    )
    auto_scale_budget: bool = Field(
        default=False,
        description="Automatically scale budget based on usage patterns"
    )


class ContextConfig(BaseModel):
    """Context management configuration."""
    
    max_context_size: int = Field(
        default=4096,
        gt=0,
        description="Maximum context size in tokens"
    )
    context_retention_hours: int = Field(
        default=24,
        gt=0,
        description="How long to retain context in hours"
    )
    enable_compression: bool = Field(
        default=True,
        description="Enable context compression"
    )
    enable_summarization: bool = Field(
        default=True,
        description="Enable context summarization"
    )


class TelemetryConfig(BaseModel):
    """Telemetry collection configuration."""
    
    enabled: bool = Field(default=True, description="Enable telemetry collection")
    batch_size: int = Field(
        default=100,
        gt=0,
        description="Batch size for telemetry uploads"
    )
    flush_interval: int = Field(
        default=300,
        gt=0,
        description="Flush interval in seconds"
    )
    include_prompts: bool = Field(
        default=False,
        description="Include prompts in telemetry (privacy setting)"
    )
    include_responses: bool = Field(
        default=False,
        description="Include responses in telemetry (privacy setting)"
    )


class AgentConfig(BaseModel):
    """Main configuration for the Agent."""
    
    api_key: str = Field(..., description="py-agent API key")
    providers: List[ProviderConfig] = Field(
        default_factory=list,
        description="Provider configurations"
    )
    budget: BudgetConfig = Field(
        default_factory=BudgetConfig,
        description="Budget configuration"
    )
    context: ContextConfig = Field(
        default_factory=ContextConfig,
        description="Context configuration"
    )
    telemetry: TelemetryConfig = Field(
        default_factory=TelemetryConfig,
        description="Telemetry configuration"
    )
    default_optimization: OptimizationMode = Field(
        default=OptimizationMode.BALANCED,
        description="Default optimization mode"
    )
    enable_fallbacks: bool = Field(
        default=True,
        description="Enable provider fallbacks"
    )
    enable_caching: bool = Field(
        default=True,
        description="Enable response caching"
    )


class UsageStats(BaseModel):
    """Usage statistics model."""
    
    total_requests: int = Field(default=0, description="Total number of requests")
    total_cost: float = Field(default=0.0, description="Total cost in USD")
    total_tokens: int = Field(default=0, description="Total tokens used")
    average_cost: float = Field(default=0.0, description="Average cost per request")
    average_quality: float = Field(default=0.0, description="Average quality score")
    average_response_time: float = Field(
        default=0.0,
        description="Average response time in seconds"
    )
    cost_savings: float = Field(default=0.0, description="Total cost savings")
    savings_percent: float = Field(default=0.0, description="Savings percentage")
    provider_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Request distribution by provider"
    )
    model_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Request distribution by model"
    )
    optimization_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Request distribution by optimization mode"
    )
    daily_costs: List[float] = Field(
        default_factory=list,
        description="Daily cost history"
    )
    quality_trend: List[float] = Field(
        default_factory=list,
        description="Quality score trend"
    )


class RoutingMetrics(BaseModel):
    """Metrics for routing decisions."""
    
    request_id: str = Field(..., description="Request identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    prompt_category: str = Field(..., description="Categorized prompt type")
    selected_model: str = Field(..., description="Selected model")
    selected_provider: str = Field(..., description="Selected provider")
    optimization_mode: OptimizationMode = Field(
        ...,
        description="Optimization mode used"
    )
    routing_time_ms: float = Field(
        ...,
        description="Time taken for routing decision in milliseconds"
    )
    alternatives_considered: List[str] = Field(
        default_factory=list,
        description="Alternative models considered"
    )
    routing_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in routing decision"
    )
    cost_factor: float = Field(..., description="Cost factor in decision")
    quality_factor: float = Field(..., description="Quality factor in decision")
    speed_factor: float = Field(..., description="Speed factor in decision")


class ErrorReport(BaseModel):
    """Error reporting model."""
    
    error_id: str = Field(..., description="Unique error identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error_type: str = Field(..., description="Type of error")
    error_message: str = Field(..., description="Error message")
    provider: Optional[str] = Field(default=None, description="Provider involved")
    model: Optional[str] = Field(default=None, description="Model involved")
    request_context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Context when error occurred"
    )
    stack_trace: Optional[str] = Field(
        default=None,
        description="Stack trace if available"
    )
    resolution: Optional[str] = Field(
        default=None,
        description="How the error was resolved"
    )