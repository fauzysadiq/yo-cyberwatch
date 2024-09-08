import requests
import dotenv
import os 


dotenv.load_dotenv(os.path.join('..', '.env'))
auth_key = os.environ['FLASK_API_AUTH_CODE']
chatbot_api_url = os.environ['CHATBOT_URL']  + "/chat" + '/' + auth_key

def get_history_schema(role, message):
    return {
        "role": role,
        "parts": [message]
    }

def test_chat_endpoint(message, history):

    payload = {
        "message": message,
        "history": history
    }

    response = requests.post(chatbot_api_url, json=payload)

    if response.status_code == 200:
        return 200, response.json()
    else:
        print("Error:", response.status_code, response.text)
        return 400, None

def main(dev_test:bool = False) -> None:
    '''
    dev_test : get one time response from the bot if its true
    '''

    print('''
    Enter 'END' to end the chat
    ''')
    while True:
        message = input('user : ')
        if message == 'END': break
        history = [get_history_schema('model', 'hi, how can i help you.')]
        status_code, response = test_chat_endpoint(message, history)

        if status_code == 200:
            bot_response = response['bot_response']
            history.append(get_history_schema('user', message))
            history.append(get_history_schema('model', bot_response))
            print('cyber ai : ' + bot_response)

        if dev_test:
            break


if __name__ == "__main__":
    main(False)