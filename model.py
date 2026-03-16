import google.generativeai as genai
import os

# Set up the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_workout(name, age, goal, level, equipment, bmi):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment. Please set it in Hugging Face Secrets."
    
    try:
        genai.configure(api_key=api_key)
        # Standard model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are a professional fitness coach. Provide a detailed 5-day workout plan for:
        - Name: {name}, Age: {age}, Goal: {goal}, Level: {level}, Equipment: {equipment}, BMI: {bmi}
        
        Structure: For each day, provide a "Day X: [Focus]" header, followed by a list of 3 exercises with sets, reps, and a tip.
        Return ONLY the plan in Markdown.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error: Could not generate plan with Gemini: {str(e)}" 
