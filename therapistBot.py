import google.generativeai as genai
from config import API_KEY

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

class TherapistBot:
    def __init__(self, history= None, system_instruction= defaultSysInstructions, safety_settings= default_safety_settings, generation_config = default_config):
        if history is None:
            history = []
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            safety_settings=safety_settings,
            generation_config=generation_config,
            system_instruction=system_instruction
        )
        self.chat_session = self.model.start_chat(history=history)
    
    def generate_content(self, user_input, update_history= True):
        response = self.chat_session.send_message(user_input)
        model_response = response.text
        if update_history:
            self.chat_session.history.append({"role": "user", "parts": [user_input]})
            self.chat_session.history.append({"role": "model", "parts": [model_response]})
        return model_response

    def run_convo_sample(self, bot_intro_message):
        print("Enter . to stop quit chatting")
        print("Bot: " + bot_intro_message)
        while True: 
            user_input = input("You: ")
            if user_input == ".":
                print(self.generate_content("Say goodbye to the user and thank them for sharing", False))
                break
            print(self.generate_content(user_input))

    def generate_tasks(self):
        prompt = r"Generate a list of daily tasks that a user can complete to improve their mental health based on their diagnosis. These tasks will be used in a web app where the patient earns xp for completing tasks daily and levels up. Return the tasks in a json with the format {title:String, xp_reward: Int, completed: {type: Boolean, default: false}} and say nothing else"
        return self.generate_content(prompt)
    
if __name__ == "__main__":
    bot1 = TherapistBot()
    bot1.run_convo_sample("How are you doing today?")
    print(bot1.generate_tasks())