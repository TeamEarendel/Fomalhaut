from os import path as _sysio
from os import mkdir as _mkdir
from datetime import datetime as _datetime
from traceback import format_exception as _exc
from typing import Final as _Final
from typing import Optional as _Optional
from typing import Self as _Self
from typing import TextIO as _TextIO

from discord import Colour as _Colour
from discord import File as _File

from .WebhookProcessor import WebhookProcessor as _Processor
from ..assets.message import Embed as _Embed
from ..assets.message import Message as _Message


class Logger:
    def __init__(
            self,
            name: str
    ) -> None:
        self._name: _Final[str] = name
        log: _TextIO

        if not _sysio.exists(f"log/{name}"):
            _mkdir(f"log/{name}")

        open(f"log/{name}/{_datetime.now().strftime('%y%m%d-%H_%M')}.log", 'x').close()
        log = open(f"log/{name}/{_datetime.now().strftime('%y%m%d-%H_%M')}.log", 'w')

        self._log_file: _Final[_TextIO] = log
        self._cache: _Optional[_Message] = None

    def log(self, content: str) -> None:
        print(f"[{self._name}] {content}")
        self._log_file.write(f"[{_datetime.now().strftime('%p %I:%M:%S')}] {content}\n")

    def exception(
            self,
            exception: Exception,
            location: str,
            footer: _Optional[_Embed.Footer],
            ignored: bool = False,
            additional_information: _Optional[list[_Embed.Field]] = None
    ) -> _Self:
        traceback: str = "".join(_exc(exception))

        content: str = (
            f"""!!! 예외 발생을 감지했습니다 !!!
            
            위치: {location}
            예외 타입: {str(type(exception))}
            무시 여부: {ignored}
            
            ########## Exception ##########
            {exception}
            
            ########## Traceback ##########
            {traceback}"""
        )
        self.log(content)

        file: _Optional[_File] = None
        if len(traceback) > 1023:
            with open(f"fatal/{self._name}/{_datetime.now().strftime('%y%m%d-%H_%M_%S')}.log", 'w') as io:
                io.write(traceback)
                io.close()
            traceback = "첨부 로그 파일을 참조하십시오"

        embed: _Final[_Embed] = _Embed(
            title="예외 발생을 감지했습니다",
            colour=(_Colour.yellow() if ignored else _Colour.red()),
            footer=footer,
            description=f"""
                - 발생 위치: `{location}`
                - 예외 타입: `{str(type(exception))}`
                - 무시 여부: `{ignored}`
                """,
            fields=[
                _Embed.Field(
                    title="Exception", content=f"```\n{exception}\n```"
                ),
                _Embed.Field(
                    title="Traceback", content=f"```\n{traceback}\n```"
                )
            ]
        )

        if additional_information:
            for i in additional_information:
                i.append(embed)

        self._cache = _Message(
            content=content,
            embed=embed,
            file=file
        )
        return self

    def get_cache(self) -> _Optional[_Message]:
        cache: _Optional[_Message] = self._cache
        self._cache = None
        return cache

    def throw(self, processor: list[_Processor], thread: _Optional[dict] = None) -> None:  # TODO: Implement ThreadID
        for i in processor:
            i.send(self.get_cache())
