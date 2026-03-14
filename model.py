import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_workout(name, age, goal, level, equipment, bmi):

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are an expert certified fitness trainer.

Create a SAFE, structured, beginner-friendly 5-day workout plan.

Client Details:
Name: {name}
Age: {age}
Goal: {goal}
Fitness Level: {level}
Equipment Available: {equipment}
BMI: {bmi}

Instructions:
- Each day must have:
  Warmup (2 exercises)
  Main Workout (3 exercises with sets & reps)
  Cooldown (1 exercise)
  One coaching tip

- Keep workouts realistic and progressive.
- Add safety advice if BMI is high or age > 40.
- Return ONLY markdown workout plan.
"""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.6,
                "max_output_tokens": 800
            }
        )

        if response and response.text:
            return response.text
        else:
            return "⚠️ AI could not generate workout. Try again."

    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"