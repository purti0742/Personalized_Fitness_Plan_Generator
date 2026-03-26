import os
import requests
import time

def generate_workout(name, age, goal, level, equipment, bmi, food_pref="None", region="None"):
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found in environment secrets."

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
                "content": f"You are a professional fitness and nutrition coach. Return a 5-day workout plan AND basic meal tips in Markdown format. Personalize the meal tips based on the user's food preference ({food_pref}) and region ({region}). Do not include introductory text."
            },
            {
                "role": "user", 
                "content": f"User: {name}, Age: {age}, Goal: {goal}, Level: {level}, Equipment: {equipment}, BMI: {bmi}. Region: {region}, Dietary Pref: {food_pref}. Create a detailed holistic plan."
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.7
    }

    for attempt in range(4):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                return "Error: Unexpected AI response format."
            elif response.status_code in [503, 429]:
                time.sleep(25)
                continue
            else:
                return f"AI Error: {response.status_code} - {response.text}"
        except Exception as e:
            if attempt == 3: return f"Connection failed: {str(e)}"
            time.sleep(5)
            continue
    return "The AI coach is busy. Please try again later."
