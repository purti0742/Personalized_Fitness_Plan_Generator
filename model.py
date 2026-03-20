import os
import requests
import time

def generate_workout(name, age, goal, level, equipment, bmi):
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found in environment secrets."

    # Use the stable OpenAI-compatible router endpoint
    API_URL = "https://router.huggingface.co/hf-inference/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    # Use the 'messages' format - it's much more reliable with the new router
    payload = {
        "model": "meta-llama/Llama-3.2-3B-Instruct",
        "messages": [
            {
                "role": "system", 
                "content": "You are a professional fitness coach. Return ONLY the 5-day workout plan in Markdown format. Do not include introductory text or signatures."
            },
            {
                "role": "user", 
                "content": f"Name: {name}, Age: {age}, Goal: {goal}, Level: {level}, Equipment: {equipment}, BMI: {bmi}. Provide 3-4 exercises per day with sets and reps."
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    for attempt in range(3):
        try:
            # Increased timeout slightly for free tier reliability
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                # Accessing the chat completions response structure
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                return "Error: Unexpected response format from AI."
            
            # 503 means model is loading, 429 means rate limited
            elif response.status_code in [503, 429]:
                time.sleep(20)
                continue
            
            # If still getting 404/Not Found, it might be the model ID in the router
            else:
                return f"API Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Connection failed: {str(e)}"

    return "The AI coach is currently busy or loading. Please wait a moment and try again."