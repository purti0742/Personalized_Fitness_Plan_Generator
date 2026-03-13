import requests
import os

# Use a model like Llama 3 or Mistral
API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-9b-it"
# On Hugging Face Spaces, set HF_TOKEN in Settings > Secrets
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKENN')}"}

def generate_workout(name, age, goal, level, equipment, bmi):
    # Pro Tip: Add "Return only the workout plan" to the prompt
    prompt = f"User: {name}, Age: {age}, Goal: {goal}, Level: {level}, Equipment: {equipment}, BMI: {bmi}. Provide a professional 5-day workout plan with 3 exercises per day. Return ONLY the plan, no extra conversational text."
    
    try:
        response = requests.post(API_URL, headers=headers, json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 500, "return_full_text": False} # This ensures you don't get the prompt back
        })
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', "No text generated.")
        return "AI is busy or error occurred."
    except Exception as e:
        return f"Error: {str(e)}"
