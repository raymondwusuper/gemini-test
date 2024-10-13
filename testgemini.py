import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

genai.configure(api_key="AIzaSyBTE2Oh74mhQcYR0KZPnn-7VsEqEmXFCwQ")

defaultSysInstructions= r"You are a personal therapist whose goal is to talk to a user suffering with mental health issues to diagnose their needs You will be diagnosing them after an intial conversation in which they respond to certain questions. Make sure not to overwhelm the user."
default_safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

default_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
#   "response_mime_type": "application/json",
  "response_mime_type": "text/plain"
}



'''
class Task(BaseModel):
    title: str
    xp_reward: int
    completed: bool = False
'''

def generate_content(user_input):
    response = chat_session.send_message(user_input)
    model_response = response.text
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})
    return model_response

prompt = []

default_instruction = f"You are a therapist, helping people who are dealing with the following:  \
                              {' '.join(prompt)} \
                              Generate outputs to questions by giving them a task list to improve their situation.\
                              Return these tasks as json following the pydantic model: class Task(BaseModel): title: str, \
                              xp_reward: int, completed: bool = False and do not return anything else besides the json. \
                              Do not overwhelm the user."

while True:
    uinput = input("You: ") #ADD CALL FROM WEBSITE
    if uinput == "stop": break
    prompt.append(uinput)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", 
                              safety_settings=default_safety_settings,
                              generation_config=default_config,
                              system_instruction=default_instruction)
chat_session = model.start_chat(history=[])
print(prompt)
print(generate_content(uinput))
