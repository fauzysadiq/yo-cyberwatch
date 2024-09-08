from flask import Flask, request, jsonify
import os
import dotenv
import google.generativeai as genai

app = Flask(__name__)
dotenv.load_dotenv(os.path.join('..', '.env'))
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
auth_key = os.environ['FLASK_API_AUTH_CODE']
system_prompt = '''You are an exceptionally skilled cybersecurity advisor, possessing in-depth knowledge and expertise in all aspects of cybersecurity. Your role is to provide comprehensive and accurate answers to any queries related to cybersecurity, including but not limited to threat analysis, risk management, incident response, security protocols, encryption, network security, and compliance.

You are expected to:

- Your name is cyberwatch ai.
- Offer Expert Guidance: Provide detailed and actionable advice on protecting systems, networks, and data from cyber threats.
- Diagnose Issues: Analyze and troubleshoot security issues or breaches with precision, recommending effective solutions.
- Stay Current: Reference the latest cybersecurity trends, vulnerabilities, and best practices.
- Educate and Inform: Explain complex concepts in a clear and understandable manner, catering to both technical and non-technical users.
- Be Proactive: Anticipate potential security challenges and suggest preventive measures to avoid future issues.
- Always aim for clarity, accuracy, and thoroughness in your responses, and ensure that the advice you provide is relevant to the specific context of each query.'''

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
    system_instruction=system_prompt
)


async def get_response(input_message, history):
    try:
        chat_session = model.start_chat(
            history=history
        )
        
        bot_response = chat_session.send_message(input_message)
        return bot_response.text
    except genai.types.generation_types.StopCandidateException as e:
        print(f"Safety exception: {e}")
        return "Sorry, the content of your message was flagged as potentially unsafe."

@app.route(f'/chat/{auth_key}', methods=['POST'])
async def chat():
    data = request.get_json()
    
    input_message = data.get("message")
    history = data.get("history")

    bot_response = await get_response(input_message, history)
    
    return jsonify({"bot_response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
