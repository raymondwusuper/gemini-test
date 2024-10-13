import google.generativeai as genai
from config import API_KEY
# from dotenv import load_dotenv
# load_dotenv()

# genai.configure(api_key="AIzaSyBTE2Oh74mhQcYR0KZPnn-7VsEqEmXFCwQ")
# Create the model
generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
#   "response_mime_type": "application/json",
  "response_mime_type": "text/plain"
}

safety_settings = [
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

systemInstruction = r"You are a personal therapist whose goal is to create daily tasks over the course of a month to improve a user's mental health. You will be diagnosing them after an intial conversation in which they respond to certain questions. Only create the tasks when prompted, otherwise act as a therapist. These tasks are going to be used in a web app where the patient earns xp for completing tasks and levels up. When prompted to return the tasks, return them in a json with the format {title:String, xp_reward: Int, completed: {type: Boolean, default: false}}."

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction=systemInstruction,)

chat_session = model.start_chat(history=[])

def generate_content(user_input):
    response = chat_session.send_message(user_input)
    model_response = response.text
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})
    return model_response

print("Bot: How are you today?")

while True:
    uinput = input("You: ") #ADD CALL FROM WEBSITE
    print(generate_content(uinput))
