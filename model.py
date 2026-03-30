import os
import requests

def generate_workout(name, age, goal, level, equipment, bmi):
    # 1. Pull the URL you saved in Hugging Face Secrets
    NGROK_URL = os.getenv("NGROK_URL") 
    
    if not NGROK_URL:
        return "Error: NGROK_URL not found in Hugging Face Secrets. Please add it in Settings."

    # 2. Point to the local LM Studio server endpoint
    # We use /v1/chat/completions to match LM Studio's OpenAI-style API
    API_URL = f"{NGROK_URL.rstrip('/')}/v1/chat/completions"
    
    # 3. CRITICAL: Add the ngrok-skip header for the free tier
    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true" 
    }

    # 4. Create the request for your local Llama model
    payload = {
        "model": "llama-3.2-3b-instruct", 
        "messages": [
            {
                "role": "system", 
                "content": "You are a professional fitness coach. Return ONLY a 5-day workout plan in Markdown format. Do not include introductory text."
            },
            {
                "role": "user", 
                "content": f"Name: {name}, Age: {age}, Goal: {goal}, Level: {level}, Equipment: {equipment}, BMI: {bmi}. Provide 3-4 exercises per day with sets and reps."
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    try:
        # 5. Send the request to your home computer
        # Timeout is set high (180s) because local CPUs can take longer than cloud GPUs
        response = requests.post(API_URL, headers=headers, json=payload, timeout=180)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            return "Error: Received an empty response from your local AI."
        else:
            return f"Server Error ({response.status_code}): Ensure LM Studio and ngrok are both running on your PC."
            
    except requests.exceptions.Timeout:
        return "The request timed out. Your computer is taking too long to process the plan."
    except Exception as e:
        return f"Connection Failed: Is your CMD window still open with ngrok? Error: {str(e)}"