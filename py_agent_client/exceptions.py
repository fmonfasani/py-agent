"""
Custom exceptions for py-agent-client

This module defines all custom exceptions used throughout the py-agent-client
library to provide clear error handling and debugging information.
"""

from typing import Any, Dict, Optional


class PyAgentError(Exception):
    """Base exception class for all py-agent-client errors."""

    def __init__(
        self, message: str, error_code: str = None, details: Dict[str, Any] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details,
        }


class ProviderError(PyAgentError):
    """Exception raised when AI provider API calls fail."""

    def __init__(
        self,
        message: str,
        provider: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict] = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.provider = provider
        self.status_code = status_code
        self.response_data = response_data or {}

        # Add provider info to details
        self.details.update(
            {
                "provider": provider,
                "status_code": status_code,
                "response_data": response_data,
            }
        )


class RoutingError(PyAgentError):
    """Exception raised when request routing fails."""

    def __init__(
        self,
        message: str,
        attempted_providers: list = None,
        routing_criteria: Dict = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.attempted_providers = attempted_providers or []
        self.routing_criteria = routing_criteria or {}

        self.details.update(
            {
                "attempted_providers": self.attempted_providers,
                "routing_criteria": self.routing_criteria,
            }
        )


class QualityThresholdError(PyAgentError):
    """Exception raised when response quality is below threshold."""

    def __init__(
        self, message: str, quality_score: float, threshold: float, model: str, **kwargs
    ):
        super().__init__(message, **kwargs)
        self.quality_score = quality_score
        self.threshold = threshold
        self.model = model

        self.details.update(
            {
                "quality_score": quality_score,
                "threshold": threshold,
                "model": model,
            }
        )


class BudgetExceededError(PyAgentError):
    """Exception raised when budget limits are exceeded."""

    def __init__(
        self,
        message: str,
        budget_type: str,  # "daily" or "monthly"
        current_spend: float,
        budget_limit: float,
        requested_cost: float,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.budget_type = budget_type
        self.current_spend = current_spend
        self.budget_limit = budget_limit
        self.requested_cost = requested_cost

        self.details.update(
            {
                "budget_type": budget_type,
                "current_spend": current_spend,
                "budget_limit": budget_limit,
                "requested_cost": requested_cost,
                "available_budget": budget_limit - current_spend,
            }
        )


class ConfigurationError(PyAgentError):
    """Exception raised for configuration-related errors."""

    def __init__(
        self,
        message: str,
        config_key: str = None,
        expected_type: type = None,
        actual_value: Any = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.config_key = config_key
        self.expected_type = expected_type
        self.actual_value = actual_value

        self.details.update(
            {
                "config_key": config_key,
                "expected_type": expected_type.__name__ if expected_type else None,
                "actual_value": actual_value,
            }
        )


class AuthenticationError(PyAgentError):
    """Exception raised for authentication failures."""

    def __init__(self, message: str, provider: str = None, **kwargs):
        super().__init__(message, **kwargs)
        self.provider = provider

        if provider:
            self.details.update({"provider": provider})


class RateLimitError(ProviderError):
    """Exception raised when API rate limits are exceeded."""

    def __init__(
        self,
        message: str,
        provider: str,
        retry_after: Optional[int] = None,
        limit_type: str = "requests",
        **kwargs,
    ):
        super().__init__(message, provider, **kwargs)
        self.retry_after = retry_after
        self.limit_type = limit_type

        self.details.update(
            {
                "retry_after": retry_after,
                "limit_type": limit_type,
            }
        )


class ModelNotFoundError(ProviderError):
    """Exception raised when requested model is not available."""

    def __init__(
        self,
        message: str,
        model: str,
        provider: str,
        available_models: list = None,
        **kwargs,
    ):
        super().__init__(message, provider, **kwargs)
        self.model = model
        self.available_models = available_models or []

        self.details.update(
            {
                "model": model,
                "available_models": self.available_models,
            }
        )


class TokenLimitError(PyAgentError):
    """Exception raised when token limits are exceeded."""

    def __init__(
        self, message: str, token_count: int, token_limit: int, model: str, **kwargs
    ):
        super().__init__(message, **kwargs)
        self.token_count = token_count
        self.token_limit = token_limit
        self.model = model

        self.details.update(
            {
                "token_count": token_count,
                "token_limit": token_limit,
                "model": model,
            }
        )


class ContextError(PyAgentError):
    """Exception raised for context management errors."""

    def __init__(
        self, message: str, context_id: str = None, context_size: int = None, **kwargs
    ):
        super().__init__(message, **kwargs)
        self.context_id = context_id
        self.context_size = context_size

        self.details.update(
            {
                "context_id": context_id,
                "context_size": context_size,
            }
        )


class TelemetryError(PyAgentError):
    """Exception raised for telemetry collection errors."""

    def __init__(self, message: str, telemetry_type: str = None, **kwargs):
        super().__init__(message, **kwargs)
        self.telemetry_type = telemetry_type

        if telemetry_type:
            self.details.update({"telemetry_type": telemetry_type})


# Exception hierarchy for easy catching
class APIError(ProviderError):
    """Base class for all API-related errors."""

    pass


class NetworkError(PyAgentError):
    """Exception raised for network-related errors."""

    def __init__(self, message: str, url: str = None, timeout: float = None, **kwargs):
        super().__init__(message, **kwargs)
        self.url = url
        self.timeout = timeout

        self.details.update(
            {
                "url": url,
                "timeout": timeout,
            }
        )


# Utility functions for error handling
def handle_provider_error(
    error: Exception, provider: str, context: Dict[str, Any] = None
) -> ProviderError:
    """
    Convert generic exceptions to ProviderError with context.

    Args:
        error: The original exception
        provider: Name of the AI provider
        context: Additional context information

    Returns:
        ProviderError with appropriate details
    """
    context = context or {}

    # Handle specific error types
    if hasattr(error, "status_code"):
        status_code = error.status_code
        if status_code == 401:
            return AuthenticationError(
                f"Authentication failed for {provider}",
                provider=provider,
                error_code="AUTH_FAILED",
            )
        elif status_code == 429:
            return RateLimitError(
                f"Rate limit exceeded for {provider}",
                provider=provider,
                status_code=status_code,
                error_code="RATE_LIMIT",
            )

    # Generic provider error
    return ProviderError(
        f"Provider {provider} error: {str(error)}",
        provider=provider,
        error_code="PROVIDER_ERROR",
        details=context,
    )


def format_error_message(error: PyAgentError, include_details: bool = False) -> str:
    """
    Format error message for display.

    Args:
        error: The PyAgentError to format
        include_details: Whether to include error details

    Returns:
        Formatted error message
    """
    message = str(error)

    if include_details and error.details:
        details_str = ", ".join(
            f"{k}={v}" for k, v in error.details.items() if v is not None
        )
        if details_str:
            message += f" ({details_str})"

    return message
