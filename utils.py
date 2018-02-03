import requests
from local_settings import TELE_TOKEN, CRM_CHANNEL


def crm_update_message(text):

    send_message_template = (
        "https://api.telegram.org/bot{TOKEN}"
        "/sendMessage?chat_id={chat_id}&text={client_update}"
    )
    requests.get(send_message_template.format(**{
        "TOKEN": TELE_TOKEN,
        "chat_id": CRM_CHANNEL,
        "client_update": text,
    }))
