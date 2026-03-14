import random


def generate_workout(name, age, goal, level, equipment, bmi_status):

    warmups = [
        "Jumping Jacks – 2 mins",
        "Arm Circles – 1 min",
        "High Knees – 1 min",
        "Light Jog – 3 mins"
    ]

    muscle_no_eq = [
        "Pushups – 4 x 12",
        "Squats – 4 x 15",
        "Plank – 3 x 45 sec",
        "Lunges – 3 x 12 each leg",
        "Mountain Climbers – 3 x 30 sec"
    ]

    muscle_dumbbells = [
        "Dumbbell Curl – 4 x 12",
        "Shoulder Press – 4 x 10",
        "Goblet Squats – 4 x 12",
        "Dumbbell Row – 4 x 10",
        "Chest Press – 4 x 10"
    ]

    muscle_gym = [
        "Bench Press – 5 x 5",
        "Deadlift – 5 x 5",
        "Lat Pulldown – 4 x 10",
        "Leg Press – 4 x 12",
        "Cable Fly – 4 x 12"
    ]

    fat_loss = [
        "Burpees – 4 x 15",
        "Skipping – 5 mins",
        "Mountain Climbers – 4 x 40 sec",
        "Jump Squats – 4 x 12",
        "Plank – 4 x 1 min"
    ]

    cardio = [
        "Running – 15 mins",
        "Cycling – 20 mins",
        "Jump Rope – 10 mins",
        "Stair Climb – 10 mins",
        "Shadow Boxing – 5 mins"
    ]

    plan = f"\n🔥 Hello {name}! Here is your AI Generated Workout Plan\n"
    plan += f"\n🎯 Goal: {goal}"
    plan += f"\n📊 Level: {level}"
    plan += f"\n🏋 Equipment: {equipment}"
    plan += f"\n💡 BMI Status: {bmi_status}\n"

    plan += "\n🟡 Warmup:\n"
    for w in random.sample(warmups,2):
        plan += f"• {w}\n"

    if goal == "Build Muscle":

        plan += "\n💪 Strength Training:\n"

        if equipment == "No Equipment":
            exercises = muscle_no_eq

        elif equipment == "Dumbbells":
            exercises = muscle_dumbbells

        else:
            exercises = muscle_gym

        count = 3 if level == "Beginner" else 4 if level == "Intermediate" else 5

        for ex in random.sample(exercises,count):
            plan += f"• {ex}\n"

    elif goal == "Lose Weight":

        plan += "\n🔥 Fat Burn Circuit:\n"

        for ex in random.sample(fat_loss,4):
            plan += f"• {ex}\n"

    else:

        plan += "\n❤️ Cardio Session:\n"

        for ex in random.sample(cardio,4):
            plan += f"• {ex}\n"

    if age > 40:
        plan += "\n⚠ Advice: Maintain moderate intensity due to age.\n"

    if bmi_status == "Overweight":
        plan += "⚠ Advice: Focus more on cardio & calorie deficit.\n"

    plan += "\n✅ Stay Consistent. Drink Water. Sleep Well.\n"

    return plan