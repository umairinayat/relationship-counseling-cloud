import re

class HallucinationControls:
    """
    Post-processing to enforce epistemic humility.
    """
    
    @staticmethod
    def enforce_epistemic_humility(text: str) -> str:
        """
        Rewrites certain sentences to be less definitive.
        """
        # Simple string replacements for demonstration.
        # In production, this might be another LLM pass or strict grammar rules.
        
        replacements = [
            (r"He is feeling", "It sounds like he might be feeling"),
            (r"She thinks", "It's possible she thinks"),
            (r"This means", "This could mean"),
            (r"You will", "You might")
        ]
        
        processed_text = text
        for pattern, replacement in replacements:
            # Simple replace doesn't handle context well, using RegEx sub for start of sentences
            processed_text = re.sub(pattern, replacement, processed_text, flags=re.IGNORECASE)
            
        return processed_text

    @staticmethod
    def detect_diagnostic_language(text: str) -> bool:
        patterns = [
            r"narcissist",
            r"bipolar",
            r"borderline",
            r"sociopath",
            r"gaslighting" # Context dependent, but often misused
        ]
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                return True
        return False
