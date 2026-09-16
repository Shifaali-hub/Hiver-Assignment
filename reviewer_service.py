from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import re

app = FastAPI(title="Hiver Reviewer API Service")

class ReviewPayload(BaseModel):
    intent_prediction: str
    generated_reply: str
    escalation_flag: str

@app.post("/review")
async def review_primary_output(payload: ReviewPayload):
    discrepancies = 0
    notes = []
    
    # 1. Intent taxonomy validation
    valid_intents = ["Account Issue / Technical Support", "Billing / Refund", "Escalation Trigger", "Other"]
    if payload.intent_prediction not in valid_intents:
        discrepancies += 1
        notes.append(f"Invalid intent mapping: {payload.intent_prediction}")
        
    # 2. Escalation Regex Compliance
    if not re.match(r"^(Auto-handled|Escalate: .*)$", payload.escalation_flag):
        discrepancies += 1
        notes.append("Escalation flag failed strict regex format.")
        
    # 3. Grounding length check 
    if len(payload.generated_reply.strip()) < 10:
        discrepancies += 1
        notes.append("Generated reply lacks sufficient grounding text.")
        
    # 4. Professionalism Guardrail (Checking for AI hallucination phrases)
    forbidden_phrases = ["as an ai", "i don't know", "guarantee"]
    if any(phrase in payload.generated_reply.lower() for phrase in forbidden_phrases):
        discrepancies += 1
        notes.append("Reply triggered hallucination/professionalism guardrails.")
        
    return {
        "audit_status": "APPROVED" if discrepancies == 0 else "REQUIRES_REVISION",
        "discrepancies_found": discrepancies,
        "reviewer_notes": "; ".join(notes) if notes else "All integrity checks passed."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)