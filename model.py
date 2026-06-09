import os
from openai import OpenAI

def generate_workout(name, age, goal, level, equipment, bmi):
    # Initialize Groq client
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a fitness coach. Generate a 5-day workout plan. Each day must include exactly 3 exercises with sets and reps. Keep it concise."
                },
                {
                    "role": "user",
                    "content": f"Age: {age}, Goal: {goal}, Level: {level}, Equipment: {equipment}. Provide 3 exercises per day with sets and reps. Add a short title for each day."
                }
            ],
            temperature=0.5,
            max_tokens=350
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Service Error: {str(e)}"