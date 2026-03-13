import requests
import os

# Use a model like Llama 3 or Mistral
API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-9b-it"
# On Hugging Face Spaces, set HF_TOKEN in Settings > Secrets
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKENN')}"}

def generate_workout(name, age, goal, level, equipment, bmi):
    # This highly structured prompt forces the model to follow a specific format
    prompt = f"""
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a professional fitness coach. Provide a detailed 5-day workout plan.
    Structure: For each day, provide a "Day X: [Focus]" header, followed by a list of 3 exercises with specific sets, reps, and a brief tip for each.
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    User Profile:
    - Name: {name}
    - Age: {age}
    - Goal: {goal}
    - Level: {level}
    - Equipment: {equipment}
    - BMI: {bmi}
    Task: Generate the 5-day structured plan. Return ONLY the plan in Markdown.
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
    
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "return_full_text": False,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload)

        # Check if the request actually worked before parsing JSON
        if response.status_code == 401:
            return "API Error: Invalid Token. Check your Secret name and value."
        elif response.status_code == 404:
            return "API Error: Model not found or URL is incorrect."
        elif response.status_code != 200:
            return f"API Error: {response.status_code} - {response.text[:100]}"

        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', "No text generated.")
        
        return "AI is busy, please try again."
        
    except Exception as e:
        return f"Could not generate plan: {str(e)}"