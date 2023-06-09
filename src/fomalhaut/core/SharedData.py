from os import getenv as _env
from json import loads as _parse
from json import dumps as _stringify
from json import JSONDecodeError as _ParseErr
from typing import Self as _Self
from requests import get as _request
from .logger.WebhookProcessor import WebhookProcessor as _Webhook


class SharedData:
    def __init__(self):
        response: str = ""
        try:
            response = _request(
                f"https://gist.githubusercontent.com/AlphaKR93/{_env('CONFIG_ID')}/raw"
            ).text
            content: dict = _parse(response)
        except _ParseErr:
            print(response)
            return

        self._content: dict = content
        self.processor: list[_Webhook] = []

        for i in self._content["logging"]:
            self.processor.append(_Webhook(f"https://discord.com/api/webhooks/{i['id']}/{i['token']}", i["threaded"]))

    def content(self) -> str:
        return _stringify(self._content)

    def config(self, name: str) -> dict:
        return self._content["botConfig"][name]

    def reload(self) -> _Self:
        self.__init__()
        return self
