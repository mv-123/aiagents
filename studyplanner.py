from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def studyplanner(topic, number_of_days, grade):
    prompt = f'''Create a daywise study plan targeting {topic} for {number_of_days} days for someone in grade {grade}.
    Make the plan realistic.'''

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
        {
            "role": "user",
            "content": prompt
        }
        ],
        temperature=2,
        max_completion_tokens=2048,
        top_p=1,
        stream=False,
        stop=None
    )
    print(response.choices[0].message.content)

def practicetest(topic, grade):
    prompt = f'''Create a 10 question multiple choice practice test regarding {topic} for grade {grade} students. Explain the answers at the end.'''
    
    response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
            {
                "role": "user",
                "content": prompt
            }
            ],
            temperature=2,
            max_completion_tokens=2048,
            top_p=1,
            stream=False,
            stop=None
        )
    print(response.choices[0].message.content)

topic = input("Enter your main studying points: ")
number_of_days = input("How many days would you like to study? ")
grade = input("What grade are you in? ")

studyplanner(topic, number_of_days, grade)
practicetest(topic, grade)



