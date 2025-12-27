from config.settings import get_settings

settings = get_settings()

class ModelRouter:
    @staticmethod
    def get_model_for_risk_level(risk_level: str) -> str:
        """
        Routes to the appropriate model based on risk/complexity.
        
        CRISIS/HIGH_RISK -> GPT-4o (Max Intelligence check)
        MEDIUM/LOW_RISK -> GPT-4o-mini (Cost efficiency)
        """
        if risk_level in ["CRISIS", "HIGH_RISK"]:
            return settings.MODEL_CRISIS # e.g. gpt-4o
        elif risk_level == "MEDIUM_RISK":
            return settings.MODEL_MEDIUM_RISK # e.g. gpt-4o-mini
        else:
            return settings.MODEL_LOW_RISK # e.g. gpt-4o-mini

    @staticmethod
    def get_classification_model() -> str:
        """Always use the cheaper model for classification tasks."""
        return settings.MODEL_MEDIUM_RISK
