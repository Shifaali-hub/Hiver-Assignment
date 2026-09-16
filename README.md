# Support Ticket Intent & Escalation Evaluator

This repository implements a dual-pipeline architecture to classify inbound customer support queries and trigger escalations. It includes a Primary Agent evaluator and a FastAPI-based Secondary Reviewer service. 

## 1. Setup & Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API Key (Optional: codebase will run safely without it via fallback logic)
export OPENAI_API_KEY="your-key-here"