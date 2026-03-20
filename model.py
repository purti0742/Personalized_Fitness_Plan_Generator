import os
import requests
import json
import time

def generate_workout(name, age, goal, level, equipment, bmi):
    # Get HF Token from environment secrets
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found. Please add it to your Hugging Face Space Settings > Secrets."

    # Using the most stable Serverless Inference endpoint (OpenAI-compatible)
    # This path is the new standard that replaces the old 410-Gone endpoint
    api_url = "https://api-inference.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    # Model ID - Llama-3.2-3B-Instruct is extremely reliable and 'warm' on the free tier
    model_id = "meta-llama/Llama-3.2-3B-Instruct"

    messages = [
        {"role": "system", "content": "You are a professional fitness coach. Return ONLY the plan in Markdown. No filler."},
        {"role": "user", "content": f"Create a 5-day workout for {name}. Goal: {goal}, Level: {level}, Equipment: {equipment}, BMI: {bmi}. Include Day headers and 3-4 exercises per day."}
    ]

    payload = {
        "model": model_id,
        "messages": messages,
        "max_tokens": 1200,
        "temperature": 0.5,
        "stream": False
    }

    try:
        # We try up to 3 times if the model is loading
        for attempt in range(3):
            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                return f"Error: No content in response: {result}"
            
            # If model is loading, wait and retry
            elif response.status_code == 503:
                time.sleep(15)
                continue
            else:
                break
        
        return f"Error: API returned status {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error: Connection failed: {str(e)}"
