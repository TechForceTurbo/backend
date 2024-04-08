import os

import requests
from dotenv import load_dotenv
from thefuzz import fuzz

from chat.models import ChatMessage, ChatSession
from telegarm_bot.constants import keyword, prompt_text

load_dotenv()


TOKEN = os.getenv('TOKEN')
API_KEY = os.getenv('API_KEY')
CAT_ID = os.getenv('CAT_ID')


def response_logic(text: str, session: ChatSession, user_id: int, message_id: int, username: str):
    """Данная функция содержит логику ответа бота пользователю, а также занесение вопросов/ответов в базу данных."""

    send_typing_url = f"https://api.telegram.org/bot{TOKEN}/sendChatAction?chat_id={user_id}&action=typing"
    requests.get(send_typing_url)

    list_from_text = text.split()

    if any(fuzz.ratio(word, keyword) > 85 for word in list_from_text):
        text_response = "Позвать оператора ?"
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={user_id}&text={text_response}&reply_to_message_id={message_id}").json()
    elif text.lower() == 'да' and session.messages.last().message == "Позвать оператора ?":
        text_response = "Зову оператора, подождите...сейчас он с вами свяжется"
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={user_id}&text={text_response}&reply_to_message_id={message_id}").json()
        text_response = "Нужно подключиться к клиенту с юзернеймом @"
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=779035433&text={text_response}{username}").json()
    elif text.lower() == 'нет' and session.messages.last() == "Позвать оператора ?":
        text_response = "Тогда что вы хотели бы узнать?"
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={user_id}&text={text_response}&reply_to_message_id={message_id}").json()
    else:
        messages = session.messages.all().order_by('-id')[:10]
        messages = list(reversed(messages))

        url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
        headers = {
            'Authorization': f'Api-Key {API_KEY}',
            'x-folder-id': CAT_ID
        }
        prompt = {
            'role': 'system',
            'text': prompt_text
        }

        messages_to_json = []
        messages_to_json.append(prompt)

        for message in messages:
            messages_to_json.append({
                'role': 'user' if message.is_user_message else 'assistant',
                'text': message.message
            })
        messages_to_json.append({
            "role": "user",
            "text": text
        })

        json = {
            "modelUri": "gpt://b1g4meb5hbbja1t6h8lv/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "2000"
            },
            "messages": messages_to_json
        }
        response = requests.post(url, headers=headers, json=json)

        text_response = response.json()['result']['alternatives'][0]['message']['text']

        send_message_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={user_id}&text={text_response}&parse_mode=Markdown&reply_to_message_id={message_id}"
        requests.get(send_message_url)

    ChatMessage.objects.create(session=session, message=text)
    ChatMessage.objects.create(session=session, message=text_response, is_user_message=False)
