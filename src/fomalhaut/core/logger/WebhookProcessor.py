from typing import Final as _Final
from typing import Optional as _Optional
from discord_webhook import DiscordWebhook as _Webhook

from ..assets.message import Message as _Message


class WebhookProcessor(_Webhook):
    def __init__(self, url: str, threaded: bool = False) -> None:
        super().__init__(url=url, rate_limit_retry=True)
        self.threaded: _Final[bool] = threaded

    def send(self, message: _Message, thread: _Optional[int] = None):  # TODO: Implement ThreadID
        self.set_content(message.content)
        self.add_embed(message.embed.serialize())
        self.add_file(message.file.fp, message.file.filename)
        self.execute()
        self.remove_embeds()
        self.remove_files()
