import os
from huggingface_hub import InferenceClient

def generate_workout(name, age, goal, level, equipment, bmi):
    # Get HF Token from environment secrets
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found. Please add it to your Hugging Face Space Secrets."

    try:
        # Switching to the exact Gemma 7B model ID and using text_generation for better stability
        client = InferenceClient(model="google/gemma-7b-it", token=hf_token)
        
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
        
        # Using text_generation which is more robust for free Inference API
        response = client.text_generation(
            prompt,
            max_new_tokens=1000,
            temperature=0.7,
            top_p=0.9,
            return_full_text=False
        )
            
        return response
        
    except Exception as e:
        return f"Error: Could not generate plan with Gemma on Hugging Face: {str(e)}" 
