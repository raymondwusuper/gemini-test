import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

genai.configure(api_key="AIzaSyBTE2Oh74mhQcYR0KZPnn-7VsEqEmXFCwQ")


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

while True:
    uinput = input("You: ") #ADD CALL FROM WEBSITE
    if uinput == "I'm finished.": break
    prompt.append(uinput)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", 
                              system_instruction="You are a therapist, helping people who are dealing with the following: "
                              ' '.join(prompt) + 
                              "Generate outputs to questions by giving them a task list to improve their situation.\
                              Return these tasks as json following the pydantic model: class Task(BaseModel): title: str, \
                              xp_reward: int, completed: bool = False and do not return anything else besides the json.")
chat_session = model.start_chat(history=[])
print(generate_content(uinput))
