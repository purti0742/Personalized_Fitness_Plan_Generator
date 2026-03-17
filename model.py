import os
import requests
import time

def generate_workout(name, age, goal, level, equipment, bmi):
    # Get HF Token from environment secrets
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found. Please add it to your Hugging Face Space Settings > Secrets."

    # Using Mistral-7B-Instruct-v0.3 - very stable on free tier
    model_id = "mistralai/Mistral-7B-Instruct-v0.3"
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {hf_token}"}

    prompt = f"<s>[INST] You are a professional fitness coach. Provide a detailed 5-day workout plan for:\n" \
             f"- Name: {name}\n- Age: {age}\n- Goal: {goal}\n- Level: {level}\n" \
             f"- Equipment: {equipment}\n- BMI: {bmi}\n\n" \
             f"Structure: For each day, provide a 'Day X: [Focus]' header, followed by a list of 3 exercises with sets, reps, and a tip.\n" \
             f"Return ONLY the plan in Markdown format. [/INST]"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
            "return_full_text": False
        },
        "options": {
            "wait_for_model": True
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=90)
        
        # Handle the response
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "Error: No text generated.")
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"]
            else:
                return f"Error: Unexpected response format: {result}"
        else:
            return f"Error: API returned status {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error: Failed to connect to Hugging Face: {str(e)}"
