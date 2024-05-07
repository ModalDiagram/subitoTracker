import requests
import os
import json

class Telegram_bot:
    chat_id = ""
    token = ""

    def __init__(self):
        main_dir = os.path.dirname(__file__)
        with open(os.path.join(main_dir, "../secrets.json"), "r") as secrets_file:
            secrets = json.load(secrets_file)
        self.chat_id = secrets.get("chat_id")
        self.token = secrets.get("token")


    def send_offers(self, offers):
        """
        Mando un messaggio col bot se trovo un'offerta e -a è specificato
        :param msg: messaggio da mandare
        """
        for offer in offers:
            request_url = "https://api.telegram.org/bot" + self.token + "/sendMessage?chat_id=" + self.chat_id + "&text=" + str(offer)
            requests.get(request_url)
