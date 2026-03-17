import os
import requests
import json

def generate_workout(name, age, goal, level, equipment, bmi):
    # Get HF Token from environment secrets
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found. Please add it to your Hugging Face Space Settings > Secrets."

    # Using the new Hugging Face Router URL (v1/chat/completions is OpenAI-compatible)
    # This is the most modern and supported way to call HF models now
    api_url = "https://router.huggingface.co/hf-inference/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    # Model ID - Mistral-7B-Instruct-v0.3 is highly reliable
    model_id = "mistralai/Mistral-7B-Instruct-v0.3"

    messages = [
        {
            "role": "system",
            "content": "You are a professional fitness coach. Return ONLY the requested plan in Markdown format. Do not add conversational filler."
        },
        {
            "role": "user",
            "content": f"Provide a detailed 5-day workout plan for:\n"
                       f"- Name: {name}\n- Age: {age}\n- Goal: {goal}\n- Level: {level}\n"
                       f"- Equipment: {equipment}\n- BMI: {bmi}\n\n"
                       f"Structure: For each day, provide a 'Day X: [Focus]' header, followed by a list of 3 exercises with sets, reps, and a tip."
        }
    ]

    payload = {
        "model": model_id,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
        "stream": False
    }

    try:
        # Increase timeout as model loading can take time
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            # Navigate the OpenAI-style response format
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0].get("message", {}).get("content", "")
                if content:
                    return content
                else:
                    return "Error: Model returned an empty message."
            else:
                return f"Error: Unexpected response format: {json.dumps(result)}"
        else:
            # Better error parsing for the new router
            try:
                err_data = response.json()
                error_msg = err_data.get("error", {}).get("message", response.text)
            except:
                error_msg = response.text
            return f"Error: API status {response.status_code} - {error_msg}"
            
    except Exception as e:
        return f"Error: Failed to connect to Hugging Face Router: {str(e)}"
