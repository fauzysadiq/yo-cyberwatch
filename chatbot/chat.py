import os
import dotenv
import google.generativeai as genai
import asyncio

def get_history_schema(role, message):
    return {
        "role": role,
        "parts": [message]
    }

dotenv.load_dotenv(os.path.join('..', '.env'))
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
history = [get_history_schema('model', 'hi, how can i help you')]

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="You are an exceptionally skilled cybersecurity advisor..."
)

async def get_response(input_message):
    chat_session = model.start_chat(
        history=history
    )

    history.append(get_history_schema('user', input_message))
    bot_response = chat_session.send_message(input_message)
    print(bot_response.text)
    history.append(get_history_schema('model', bot_response.text))

if __name__ == "__main__":
    input_message = input('user : ')
    asyncio.run(get_response(input_message))
