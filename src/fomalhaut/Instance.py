import discord as _discord
from typing import Type as _Type
from typing import Final as _Final
from typing import Optional as _Optional
from typing import Callable as _Callable
from multiprocessing import Queue

from .core.logger import Logger as _Logger
from .core.assets.message import Embed as _Embed
from .core.SharedData import SharedData as _SharedData


class Instance(_discord.Client):
    class Task:
        def __init__(
                self,
                task: _Callable
        ):
            self.task: _Final[_Callable] = task
            self.status: bool = True

        def failure(self) -> None:
            self.status = False

    def update_queue(self) -> None:
        def validate(content: dict, key: str, expected: _Type, needs: _Optional[list] = None) -> None:
            if type(content.get(key)) != expected:
                raise ValueError(f"Invalid {key} type: expected {expected}, got {type(content.get(key))}")

            if needs and content[key] not in needs:
                raise ValueError(f"Invalid {key} value: expected {needs}, got {content[key]}")

        self._shared = self._queue.get()
        config: dict = self._shared.config(self._name)

        try:
            validate(config, "basicConfig", dict)

            validate(config["basicConfig"], "token", str)
            validate(config["basicConfig"], "status", str, ["online", "offline", "idle", "dnd"])
            validate(config["basicConfig"], "activity", dict)

            validate(config["basicConfig"]["activity"], "type", str,
                     ["playing", "streaming", "listening", "watching", "competing"])
            validate(config["basicConfig"]["activity"], "content", str)
            self._config = config
        except Exception as e:
            self._logger.exception(e, "validateConfig", None, additional_information=[
                _Embed.Field("Configuration content", self._shared.content())
            ]).throw(self._shared.processor)

    def __init__(
            self,
            q: Queue,
            name: str,
            loop_timeout: int = 5
    ):
        self._shared: _Optional[_SharedData] = None
        self._config: _Optional[dict] = None

        self._name: _Final[str] = name
        self._queue: _Final[Queue] = q
        self._logger: _Final[_Logger] = _Logger(name)

        self._logger.log("인스턴스를 초기화 하는중...")

        "Initialize SharedData"
        try:
            self.update_queue()
        except Exception as e:
            self._logger.exception(e, "initialize", None).throw(self._shared.processor)
            return

        "Initialize Instance"
        try:
            super().__init__(intents=_discord.Intents.all())

            self._footer: _Optional[_Embed.Footer] = None

            self._tasks: list[Instance.Task] = []
            self._loop_timeout: _Final[int] = loop_timeout

            self._tree: _Final[_discord.app_commands.CommandTree] = _discord.app_commands.CommandTree(self)
        except Exception as e:
            self._logger.exception(e, "initialize", None).throw(self._shared.processor)
            return

        self._logger.log("인스턴스를 성공적으로 초기화 했습니다.")

    def create_task(self, task: _Callable) -> None:
        self._tasks.append(self.Task(task))
