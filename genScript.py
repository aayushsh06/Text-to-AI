from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GROQ_KEY')
client = Groq(api_key = api_key)

with open('storyType.txt', 'r') as file:
    lines = file.readlines()
story = ''.join(lines)

completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "user",
            "content": f"Generate a {story} story. Make the story less than 200 words. Only include the story in your response. Make the first line start with a dramatic hook that intrigues. Start with the action."
        },
    ],
    temperature=1,
    max_tokens=400,
    top_p=1,
    stream=True,
    stop=None,
)

script = []  
for chunk in completion:
    content = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content else ""
    if content: 
        script.append(content)


script = ''.join(script)

with open("inputText.txt", "w") as file:
    file.write(script)
