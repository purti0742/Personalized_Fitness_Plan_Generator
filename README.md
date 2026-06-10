# FitPlan AI: AI-Powered Fitness Application

FitPlan AI is an intelligent fitness platform that generates personalized workout plans based on individual user metrics and goals. Built using **Streamlit**, *Python*, and *MongoDB*, this application leverages generative AI to provide dynamic, context-aware fitness guidance.

## 🚀 Key Features

* *Personalized AI Workouts*: Generates custom fitness plans using the Llama 3.3 model via the Groq API.
* *User Authentication*: Secure account management using JWT (JSON Web Tokens) and bcrypt for password hashing.
* *Data Visualization*: Real-time tracking of fitness progress, weight trends, and health metrics (BMI) using Pandas and Streamlit.
* *Secure Architecture*: Built with environment-variable-based secrets management to ensure API security and data privacy.

## 🛠️ Tech Stack

* *Frontend/UI*: Streamlit
* *Backend*: Python
* *Database*: MongoDB Atlas
* *AI Integration*: Groq API (Llama 3.3)
* *Authentication*: JWT, bcrypt

## ⚙️ Installation & Setup

1. **Clone the repository:**
git clone https://github.com/purti0742/Personalized_Fitness_Plan_Generator.git
cd Personalized_Fitness_Plan_Generator


2. **Install dependencies:**
   pip install -r requirements.txt

3. **Configure Environment Variables:**
Create a `.env` file in the root directory and add your credentials:

MONGODB_URI=your_mongodb_connection_string
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key_for_jwt


4. **Run the application:**
streamlit run app.py

## 🔐 Security Note

This project uses environment variables to manage sensitive keys. **Never** commit your `.env` file to version control. This repository includes a `.gitignore` to ensure your credentials remain private.
