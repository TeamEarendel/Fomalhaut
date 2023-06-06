from typing import Optional as _Optional, Union as _Union, Final as _Final

import discord as _dc

from .Embed import Embed


class Message:
    def __init__(self, content: str, embed: _Optional[Embed], file: _Optional[_Union[_dc.File, str]]):
        if type(file) == str:
            raise NotImplementedError("not implemented yet")
        self.content: _Final[str] = content
        self.embed: _Final[_Optional[Embed]] = embed
        self.file: _Final[_Optional[_dc.File]] = file
