from openai import OpenAI
from dotenv import load_dotenv
import os
#import antigravity


load_dotenv()
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

path = input("Enter the path of the folder with the files you want to rename: ")
# file = input("Enter the path of the file you want to rename: ")
for filename in os.listdir(path):
  file = os.path.join(path, filename)
  f = open(file, "r")
  content = f.read()
  prompt = f'''The filename is {filename}. Summarize {content} and give the file a name according to the following points.  
1. the filename should be meaningful
2. have a maximum of 3 words
3. use underscores to separate out different words (no spaces)
4. do not change the extensions of the file or the file type and keep it the same as before
return a filename with extension only
do not provide a summary of anything or rewrite any code
'''
  f.close()

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

  newname = response.choices[0].message.content
  print(newname)
  newpath = os.path.join(path, newname)
  #os.rename(file, newpath)