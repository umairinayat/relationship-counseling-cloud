import re
from typing import List, Tuple, Dict, Any

class SafetyGuardrails:
    def __init__(self):
        self.prohibited_topics = [
            r"how to kill",
            r"buy drugs",
            r"revenge porn"
        ]
        self.crisis_keywords = [
            r"suicid",
            r"kill myself",
            r"want to die",
            r"hurt myself"
        ]

    def detect_input_risk(self, text: str) -> Dict[str, Any]:
        """
        Layer 1: Input Risk Detection
        Returns: {is_safe: bool, risk_type: str, reason: str}
        """
        # Crisis Check
        for p in self.crisis_keywords:
            if re.search(p, text, re.IGNORECASE):
                return {"is_safe": False, "risk_type": "CRISIS", "reason": "Crisis keyword detected"}

        # Prohibited Topic Check
        for p in self.prohibited_topics:
            if re.search(p, text, re.IGNORECASE):
                return {"is_safe": False, "risk_type": "PROHIBITED", "reason": "Prohibited topic detected"}
                
        return {"is_safe": True, "risk_type": "NONE", "reason": ""}

    def validate_response(self, text: str) -> Tuple[bool, str]:
        """
        Layer 2: Response Constraints
        Checks generated text for forbidden patterns.
        """
        forbidden = [
            (r"you should leave", "Directive advice"),
            (r"you have \w+ disorder", "Diagnosis attempt"),
            (r"definitely", "False certainty")
        ]
        
        for pattern, reason in forbidden:
            if re.search(pattern, text, re.IGNORECASE):
                return False, reason
                
        return True, ""

    def get_hard_refusal(self, risk_type: str) -> str:
        """
        Layer 3: Hard Refusal & Escalation
        """
        if risk_type == "CRISIS":
            return "I am an AI and cannot support you safely in this crisis. Please immediately contact 988 or go to the nearest emergency room."
        elif risk_type == "PROHIBITED":
            return "I cannot discuss that topic as it violates safety guidelines."
        return "I am unable to continue this conversation."
