import json
import requests
import sys

def main():
    try:
        with open("primary_eval.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: primary_eval.json missing. Run 'python run_pipeline.py' first.")
        sys.exit(1)
        
    print("Sending payload to Secondary Reviewer (Port 8000)...")
    try:
        response = requests.post("http://localhost:8000/review", json=data["primary_output"])
        response.raise_for_status()
        report = response.json()
        
        with open("final_audit_report.json", "w") as f:
            json.dump(report, f, indent=4)
            
        print("Success! Generated final_audit_report.json:")
        print(json.dumps(report, indent=2))
    except Exception as e:
        print(f"Connection Error: {e}. Is reviewer_service.py running?")

if __name__ == "__main__":
    main()