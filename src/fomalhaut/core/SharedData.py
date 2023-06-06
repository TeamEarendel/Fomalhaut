from os import getenv as _env
from typing import Self as _Self
from requests import get as _request
from .logger.WebhookProcessor import WebhookProcessor as _Webhook


class SharedData:
    def __init__(self):
        self._content: dict = _request(
            "https://raw.githubusercontent.com/AlphaKR93/config/main/fomalhaut.json?token=" + _env("CONFIG_TOKEN")
        ).json()
        self.processor: list[_Webhook] = []

        for i in self._content["logging"]:
            self.processor.append(_Webhook(f"https://discord.com/api/webhooks/{i['id']}/{i['token']}", i["threaded"]))

    def config(self) -> dict:
        return self._content

    def reload(self) -> _Self:
        self.__init__()
        return self
