class TrivialBaseline:
    """Predicts the majority/safest class (Other) and never escalates."""
    def predict(self, text):
        return {
            "intent": "Other", 
            "reply": "Thank you for reaching out.",
            "escalation_flag": "Auto-handled"
        }

class SimpleBaseline:
    """Uses intermediate hardcoded rules to route queries."""
    def predict(self, text):
        text_lower = text.lower()
        if "charge" in text_lower or "refund" in text_lower:
            intent = "Billing / Refund"
            flag = "Auto-handled"
        elif "court" in text_lower or "sue" in text_lower:
            intent = "Escalation Trigger"
            flag = "Escalate: simple keyword rule"
        elif "crash" in text_lower or "turn" in text_lower:
            intent = "Account Issue / Technical Support"
            flag = "Auto-handled"
        else:
            intent = "Other"
            flag = "Auto-handled"
            
        return {
            "intent": intent, 
            "reply": "Standard routed reply.",
            "escalation_flag": flag
        }