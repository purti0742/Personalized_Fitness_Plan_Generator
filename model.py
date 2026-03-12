import requests
import os

# Use a model like Llama 3 or Mistral
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
# On Hugging Face Spaces, set HF_TOKEN in Settings > Secrets
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKENN')}"}

def generate_workout(name, age, goal, level, equipment, bmi):
    prompt = f"""
    User: {name}, Age: {age}, Goal: {goal}, Fitness Level: {level}, Equipment: {equipment}, BMI: {bmi}.
    Task: Provide a professional 5-day workout plan. 
    Format: List 3 exercises per day with sets and reps. Keep it short and motivating.
    """
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        result = response.json()
        # Handle different response formats from HF models
        if isinstance(result, list):
            return result[0]['generated_text']
        return result.get('generated_text', "AI is busy, please try again.")
    except Exception as e:
        return f"Could not generate plan: {str(e)}"