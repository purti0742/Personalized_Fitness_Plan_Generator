def generate_workout(name, age, goal, level, equipment, bmi):
    # 1. Update the URL to the new Chat Completions router
    API_URL = "https://router.huggingface.co/hf-inference/v1/chat/completions"
    
    # 2. Reformat the prompt into a 'messages' list
    messages = [
        {"role": "system", "content": "You are a professional fitness coach. Provide a detailed 5-day workout plan. Return ONLY the plan in Markdown."},
        {"role": "user", "content": f"Create a plan for: {name}, Age: {age}, Goal: {goal}, Level: {level}, Equipment: {equipment}, BMI: {bmi}"}
    ]
    
    # 3. Update payload to match Chat Completion requirements
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct", # Or another model ID
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            return f"API Error: {response.status_code} - {response.text}"

        result = response.json()
        
        # 4. Update the extraction path for the response
        return result['choices'][0]['message']['content']
        
    except Exception as e:
        return f"Could not generate plan: {str(e)}"