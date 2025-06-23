"""
Telemetry collection and analytics utilities for py-agent-client.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


class TelemetryCollector:
    """Recolecta métricas de uso y desempeño de las rutas."""

    # ------------------------------------------------------------------ #
    # API pública
    # ------------------------------------------------------------------ #
    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []
        self.stats: Dict[str, Any] = {
            "total_requests": 0,
            "total_cost": 0.0,
            "total_tokens": 0,
            "average_cost": 0.0,
            "average_quality": 0.0,
            "average_response_time": 0.0,
            "cost_savings": 0.0,
            "savings_percent": 0.0,
        }

    def record(self, *, event_type: str, payload: Dict[str, Any] | None = None) -> None:
        """
        Registra un evento genérico.

        Los tests llaman a este método; internamente delega a `record_request`.
        """
        data = payload.copy() if payload else {}
        data["event_type"] = event_type
        self.record_request(data)

    def get_stats(self) -> Dict[str, Any]:
        """Devuelve una copia de las estadísticas agregadas."""
        return self.stats.copy()

    def get_events(self) -> List[Dict[str, Any]]:
        """Devuelve todos los eventos registrados hasta el momento."""
        return self.events.copy()

    def clear_events(self) -> None:
        """Limpia eventos y reinicia estadísticas."""
        self.events.clear()
        self.__init__()  # reinicia stats

    # ------------------------------------------------------------------ #
    # API interna / compatibilidad
    # ------------------------------------------------------------------ #
    def record_request(self, event_data: Dict[str, Any]) -> None:
        """Registra un evento detallado y actualiza estadísticas."""
        event_data["timestamp"] = datetime.utcnow().isoformat()
        self.events.append(event_data)
        self._update_stats(event_data)

    # ------------------------------------------------------------------ #
    # Helpers privados
    # ------------------------------------------------------------------ #
    def _update_stats(self, event_data: Dict[str, Any]) -> None:
        """Actualiza contadores simples para consultas rápidas."""
        self.stats["total_requests"] += 1

        if "cost" in event_data:
            self.stats["total_cost"] += event_data["cost"]
            self.stats["average_cost"] = (
                self.stats["total_cost"] / self.stats["total_requests"]
            )

        if "tokens_used" in event_data:
            self.stats["total_tokens"] += event_data["tokens_used"]


# ---------------------------------------------------------------------- #
# Alias para compatibilidad con importaciones que esperen `Telemetry`
# ---------------------------------------------------------------------- #
Telemetry = TelemetryCollector  # type: ignore
__all__ = ["TelemetryCollector", "Telemetry"]
