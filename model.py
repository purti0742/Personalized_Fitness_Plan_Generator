import os
import requests
import time

def generate_workout(name, age, goal, level, equipment, bmi):
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found."

    # Switch to the standard Inference API endpoint for better compatibility
    API_URL = "https://router.huggingface.co/hf-inference/models/meta-llama/Llama-3.2-3B-Instruct"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    # Format the prompt clearly for the model
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a professional fitness coach. Return ONLY the plan in Markdown. No filler.<|eot_id|>
    <|start_header_id|>user<|end_header_id|>
    Create a 5-day workout for {name}. 
    Goal: {goal}, Level: {level}, Equipment: {equipment}, BMI: {bmi}. 
    Include Day headers and 3-4 exercises per day.<|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1000,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    for attempt in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                # The response format for this endpoint is usually a list of dicts
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', 'No text generated.')
                return str(result)
            
            elif response.status_code == 503: # Model loading
                time.sleep(20)
                continue
            else:
                return f"API Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Connection failed: {str(e)}"

    return "Model is taking too long to load. Please try again in a minute."