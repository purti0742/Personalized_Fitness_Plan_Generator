import os
import requests
import time

def generate_workout(name, age, goal, level, equipment, bmi):
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found in environment secrets. Please add it to your Space settings."

    # Stable router endpoint for Llama-3.2
    API_URL = "https://router.huggingface.co/hf-inference/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3.2-3B-Instruct",
        "messages": [
            {
                "role": "system", 
                "content": "You are a professional fitness coach. Return ONLY the 5-day workout plan in Markdown format with clear headings. Include exercises, sets, and reps. Do not include introductory text."
            },
            {
                "role": "user", 
                "content": f"User: {name}, Age: {age}, Goal: {goal}, Level: {level}, Equipment: {equipment}, BMI: {bmi}. Create a detailed 5-day plan."
            }
        ],
        "max_tokens": 1200,
        "temperature": 0.7
    }

    # Robust retry logic for Hugging Face free tier
    for attempt in range(4):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                return "Error: Unexpected AI response format."
            elif response.status_code == 503:
                # Model is loading
                time.sleep(25)
                continue
            elif response.status_code == 429:
                # Rate limited
                time.sleep(15)
                continue
            else:
                return f"AI Error: {response.status_code} - {response.text}"
        except Exception as e:
            if attempt == 3:
                return f"Connection failed after multiple retries: {str(e)}"
            time.sleep(5)
            continue
    return "The AI coach is taking a break. Please try again in 30 seconds."
