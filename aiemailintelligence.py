import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

to = st.text_input("Who do you want this message to?")
topic = st.text_input("What is the topic of the email?")
tone = st.selectbox("Tone", ["Casual", "Formal", "Assertive", "Friendly"])
sender = st.text_input("Who is this message from?")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
prompt = f'''
To: {to}
Topic: {topic}
From: {sender}
Make the email based on the {tone}. Include a proper greeting, a polite closing, and a clear body. In the greeting, address {to}, then sign off with {sender} at the end (do not explicitly mention "to:" and "from:"). Do not use asteriks (*) or hashtags (#) in the email. Do not explicitly mention "{topic}" in the email. Keep the email short.
'''

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
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

email = response.choices[0].message.content
msg = MIMEText(email)
msg["Subject"] = topic
msg["From"] = EMAIL_USER
msg["To"] = to

if st.button("Generate Email"):
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(EMAIL_USER, EMAIL_PASS)
  server.sendmail(EMAIL_USER, to, msg.as_string())
  st.write("Email sent!")