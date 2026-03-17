import os
from huggingface_hub import InferenceClient

def generate_workout(name, age, goal, level, equipment, bmi):
    # Get HF Token from environment secrets
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found. Please add it to your Hugging Face Space Settings > Secrets."

    try:
        # Mistral-7B is often more stable and 'warmer' than Gemma on the free API
        # but we can try Gemma 1.1 if preferred. Let's try Gemma 1.1 first
        model_id = "google/gemma-1.1-7b-it" 
        client = InferenceClient(model=model_id, token=hf_token)
        
        prompt = f"""<start_of_turn>user
You are a professional fitness coach. Provide a detailed 5-day workout plan for:
- Name: {name}
- Age: {age}
- Goal: {goal}
- Level: {level}
- Equipment: {equipment}
- BMI: {bmi}

Structure: For each day, provide a "Day X: [Focus]" header, followed by a list of 3 exercises with sets, reps, and a tip.
Return ONLY the plan in Markdown format.<end_of_turn>
<start_of_turn>model
"""
        
        # wait_for_model=True is CRITICAL for free tier to prevent 'Model Loading' errors
        response = client.text_generation(
            prompt,
            max_new_tokens=1000,
            temperature=0.7,
            top_p=0.9,
            return_full_text=False,
            wait_for_model=True 
        )
            
        if not response:
            return "Error: The model returned an empty response. This might be a temporary API issue."
            
        return response
        
    except Exception as e:
        # Enhanced error reporting
        error_msg = str(e)
        if not error_msg:
            error_msg = f"Unknown Error (Type: {type(e).__name__}). This usually happens if the Hugging Face API is currently overloaded or the model is sleeping."
        return f"Error: {error_msg}" 
