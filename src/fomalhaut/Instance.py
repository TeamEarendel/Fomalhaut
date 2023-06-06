import discord as _discord
from typing import Final as _Final

from .core.logger import Logger as _Logger
from .core.SharedData import SharedData as _SharedData


class Instance(_discord.Client):
    class Activity:
        def __init__(
                self,
                status: str,
                activity: str,
                content: str
        ):
            self.status: _Final[_discord.Status] = _discord.Status(status)
            self.content: _Final[str] = content
            actype: _discord.ActivityType

            match activity:
                case "playing":
                    actype = _discord.ActivityType.playing
                case "listening":
                    actype = _discord.ActivityType.listening
                case "watching":
                    actype = _discord.ActivityType.watching
                case _:
                    raise ValueError("Invalid Activity Type")

            self.activity: _Final[_discord.ActivityType] = actype

    def __init__(
            self,
            shared: _SharedData,
            name: str,
            activity: Activity,
            loop_timeout: int = 5
    ):
        self.logger: _Final[_Logger] = _Logger(name, shared.processor)
        self.logger.log("인스턴스를 초기화 하는중...")
        try:
            super().__init__(intents=_discord.Intents.all())

            self._name: _Final[str] = name
            self._shared: _Final[_SharedData] = shared.reload()

        except Exception as e:
            self.logger.exception(e, "initialize", None).throw()
            return
