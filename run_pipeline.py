import argparse
import os
import sys
import json

# Force Python to recognize the current directory (Fixes Windows/OneDrive pathing issues)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from primary_agent import PrimaryAgent

def main():
    parser = argparse.ArgumentParser(description="Primary Support Agent Pipeline")
    parser.add_argument("--brand", default="AppleSupport")
    parser.add_argument("--sample", action="store_true", help="Run with sample data flag")
    args = parser.parse_args()
    
    print(f"Starting pipeline for {args.brand}...")
    
    # We now simply read the shipped static golden_200.json!
    if not os.path.exists("golden_200.json"):
        print("Error: golden_200.json not found! Ensure it is included in your directory.")
        sys.exit(1)
        
    with open("golden_200.json", "r") as f:
        data = json.load(f)
        
    agent = PrimaryAgent()
    
    # Process the first tweet to generate the payload for the Reviewer API
    output = agent.process_tweet(data[0])
    
    payload = {
        "tweet_id": data[0]["tweet_id"],
        "primary_output": output
    }
    
    with open("primary_eval.json", "w") as f:
        json.dump(payload, f, indent=4)
        
    print("Pipeline Step 1 Complete: Saved payload to primary_eval.json")

if __name__ == "__main__":
    main()