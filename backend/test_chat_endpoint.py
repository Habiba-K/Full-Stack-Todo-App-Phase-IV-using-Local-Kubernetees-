"""
Test Chat Endpoint Directly

This script tests the /api/chat endpoint to see what error is occurring.
"""
import asyncio
import requests
import json

def test_chat():
    print("=" * 70)
    print("TESTING CHAT ENDPOINT")
    print("=" * 70)

    # You need a valid JWT token
    # For testing, we'll try without auth first to see the error

    url = "http://localhost:8001/api/chat"

    payload = {
        "message": "Show me all my tasks"
    }

    headers = {
        "Content-Type": "application/json"
    }

    print(f"\nSending request to: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("\nNote: This will fail with 401 because we don't have a token")
    print("But it will show us if the endpoint is reachable\n")

    try:
        response = requests.post(url, json=payload, headers=headers)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 401:
            print("\n✓ Endpoint is reachable (401 = needs authentication)")
        elif response.status_code == 500:
            print("\n✗ Server error - check backend logs")
        else:
            print(f"\n? Unexpected status code: {response.status_code}")

    except Exception as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    test_chat()
