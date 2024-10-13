import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

genai.configure(api_key="AIzaSyBTE2Oh74mhQcYR0KZPnn-7VsEqEmXFCwQ")
model = genai.GenerativeModel(model_name="gemini-1.5-flash", 
                              system_instruction="You are a therapist, helping people who are mentally ill. \
                              Generate outputs to questions by giving them a task list to improve their situation.\
                              Return these tasks as json with the task name, how much xp should be rewarded from \
                              completing the task based on task difficulty, and a completion status set to false. \
                              Do not return anything else besides the json.")
chat_session = model.start_chat(history=[])

class Task(BaseModel):
    title: str
    xp_reward: int
    completed: bool = False

def generate_content(user_input):
    response = chat_session.send_message(user_input)
    model_response = response.text
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})
    return model_response

while True:
    uinput = input("You: ") #ADD CALL FROM WEBSITE
    print(generate_content(uinput))
