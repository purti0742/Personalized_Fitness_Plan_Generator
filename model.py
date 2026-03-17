import os
from huggingface_hub import InferenceClient

def generate_workout(name, age, goal, level, equipment, bmi):
    # Get HF Token from environment secrets
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    if not hf_token:
        return "Error: HUGGINGFACE_TOKEN not found. Please add it to your Hugging Face Space Secrets."

    try:
        # Using Gemma 2 9B IT (newer and more capable version of Gemma)
        # or can use "google/gemma-7b-it" if explicitly preferred
        client = InferenceClient("google/gemma-2-9b-it", token=hf_token)
        
        prompt = f"""
        <start_of_turn>user
        You are a professional fitness coach. Provide a detailed 5-day workout plan for:
        - Name: {name}
        - Age: {age}
        - Goal: {goal}
        - Level: {level}
        - Equipment: {equipment}
        - BMI: {bmi}
        
        Structure: For each day, provide a "Day X: [Focus]" header, followed by a list of 3 exercises with sets, reps, and a tip.
        Return ONLY the plan in Markdown format.
        <end_of_turn>
        <start_of_turn>model
        """
        
        response = ""
        for message in client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            stream=True,
        ):
            response += message.choices[0].delta.content or ""
            
        return response
        
    except Exception as e:
        return f"Error: Could not generate plan with Gemma on Hugging Face: {str(e)}" 
