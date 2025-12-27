import logging
import time
from typing import Dict, Any

logger = logging.getLogger("monitoring")

class MonitoringClient:
    def __init__(self):
        # In production this would connect to Datadog/Prometheus
        pass

    def log_request(self, latency_ms: float, risk_level: str, model: str):
        logger.info(f"REQUEST METRICS: latency={latency_ms}ms risk={risk_level} model={model}")

    def log_classification(self, user_id: str, input_hash: str, risk_dcit: Dict[str, Any]):
        logger.info(f"CLASSIFICATION: user={user_id} risk={risk_dcit.get('risk_level')}")

    def alert_crisis(self, user_id: str, context: str):
        # In production: PagerDuty / SMS alert
        logger.critical(f"CRISIS ALERT: User {user_id}. Context: {context}")

    def log_error(self, component: str, error: str):
        logger.error(f"COMPONENT ERROR [{component}]: {error}")
