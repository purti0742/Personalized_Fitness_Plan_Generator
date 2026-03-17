import os
import json
from huggingface_hub import InferenceClient

def generate_workout(name, age, goal, level, equipment, bmi):
    # Get HF Token from environment secrets
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found. Please add it to your Hugging Face Space Settings > Secrets."

    try:
        # Use a very popular and stable model: Mistral-7B-Instruct-v0.3
        # It's better supported on the free Inference API than Gemma 1.1
        model_id = "mistralai/Mistral-7B-Instruct-v0.3"
        client = InferenceClient(model=model_id, token=hf_token)
        
        prompt = f"<s>[INST] You are a professional fitness coach. Provide a detailed 5-day workout plan for:\n" \
                 f"- Name: {name}\n- Age: {age}\n- Goal: {goal}\n- Level: {level}\n" \
                 f"- Equipment: {equipment}\n- BMI: {bmi}\n\n" \
                 f"Structure: For each day, provide a 'Day X: [Focus]' header, followed by a list of 3 exercises with sets, reps, and a tip.\n" \
                 f"Return ONLY the plan in Markdown format. [/INST]"

        # Using direct post to be 100% sure about the parameters
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.9,
            },
            "options": {
                "wait_for_model": True,
                "use_cache": False
            }
        }
        
        response = client.post(json=payload)
        result = json.loads(response.decode("utf-8"))

        # The API returns a list with the generated text
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "Error: No text generated.")
        
        return str(result)
        
    except Exception as e:
        return f"Error: Could not generate plan: {str(e)}"
