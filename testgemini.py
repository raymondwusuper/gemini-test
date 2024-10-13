import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

genai.configure(api_key="AIzaSyBTE2Oh74mhQcYR0KZPnn-7VsEqEmXFCwQ")

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

default_instruction = f"You are a personal therapist whose goal is to talk to a user suffering with mental health issues to \
                      diagnose their needs. You will be diagnosing them and assigning them both interactive and achievable tasks as \
                      well as slightly more difficult, proactive tasks for relatively more experience points. The following \
                      information illustrates how they feel right now:  \
                      {' '.join(prompt)} \
                      Generate outputs to questions by giving them a task list to improve their situation(s).\
                      Return these tasks as json following the pydantic model: class Task(BaseModel): title: str, \
                      xp_reward: int, completed: bool = False and do not return anything else besides the json. \
                      Generate an amount such that all of them can be completed in a day. Make sure the experience \
                      points are multiples of 5. These tasks should be specific to the situation of the user."
first = True
while True:
    uinput = input("Anything weighing on your mind? \n" if first else "Anything else? \n") #ADD CALL FROM WEBSITE
    first = False
    if uinput == "stop": break
    prompt.append(uinput)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", 
                              safety_settings=default_safety_settings,
                              generation_config=default_config,
                              system_instruction=default_instruction)
chat_session = model.start_chat(history=[])
print(generate_content(uinput))
