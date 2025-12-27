import re
from typing import List

class FailureDetector:
    """
    Analyzes interactions for emotional and technical failures.
    """
    
    @staticmethod
    def detect_emotional_failure(response_text: str) -> List[str]:
        failures = []
        
        # 1. False Reassurance
        if re.search(r"everything will be (fine|okay)", response_text, re.IGNORECASE):
            failures.append("FALSE_REASSURANCE")
            
        # 2. Directive Advice
        if re.search(r"you (should|must|need to) break up", response_text, re.IGNORECASE):
            failures.append("DIRECTIVE_ADVICE")
            
        # 3. Amateur Diagnosis
        if re.search(r"you have (depression|anxiety|bpd)", response_text, re.IGNORECASE):
            failures.append("AMATEUR_DIAGNOSIS")
            
        return failures
