from datetime import datetime as _datetime
from typing import Final as _Final
from typing import Optional as _Optional
from typing import Union as _Union

from discord import Colour as _Colour
from discord import Embed as _Embed
from discord_webhook import DiscordEmbed as _WebhookEmbed


class Embed(_Embed):
    class Author:
        def __init__(
                self,
                text: _Optional[str] = None,
                url: _Optional[str] = None,
                icon: _Optional[str] = None,
        ):
            self.text: _Final[_Optional[str]] = text
            self.url: _Final[_Optional[str]] = url
            self.icon: _Final[_Optional[str]] = icon

        def append(self, embed: _Embed) -> _Embed:
            return embed.set_author(name=self.text, url=self.url, icon_url=self.icon)

    class Footer:
        def __init__(
                self,
                text: _Optional[str] = None,
                icon: _Optional[str] = None,
        ):
            self.text: _Final[_Optional[str]] = text
            self.icon: _Final[_Optional[str]] = icon

        def append(self, embed: _Embed) -> _Embed:
            return embed.set_footer(text=self.text, icon_url=self.icon)

    class Field:
        def __init__(
                self,
                title: _Optional[str] = None,
                content: _Optional[str] = None,
                inline: bool = False
        ):
            self.title: _Final[_Optional[str]] = title
            self.content: _Final[_Optional[str]] = content
            self.inline: _Final[bool] = inline

        def append(self, embed: _Embed) -> _Embed:
            return embed.add_field(name=self.title, value=self.content, inline=self.inline)

    def __init__(
            self,
            title: _Optional[str] = None,
            description: _Optional[str] = None,
            url: _Optional[str] = None,
            colour: _Optional[_Colour] = None,
            image: _Optional[_Union[str, bool]] = False,
            profile: _Optional[str] = None,
            timestamp: _datetime = _datetime.now(),
            author: _Optional[Author] = None,
            footer: _Optional[Footer] = None,
            fields: _Optional[list[Field]] = None
    ):
        super().__init__(
            colour=colour,
            title=title,
            url=url,
            description=description,
            timestamp=timestamp
        ).set_thumbnail(
            url=profile
        )

        if image is str:
            self.set_image(url=image)
        elif image is bool and image:
            self.set_image(url="attachment://attachment.png")

        if author is not None:
            author.append(self)

        if footer is not None:
            footer.append(self)

        if fields:
            for i in fields:
                i.append(self)

    def serialize(self) -> _WebhookEmbed:
        embed: _WebhookEmbed = _WebhookEmbed()

        embed.set_title(self.title)
        embed.set_description(self.description)
        embed.set_url(self.url)
        embed.set_color(self.colour.value)
        embed.set_image(self.image.url)
        embed.set_thumbnail(self.thumbnail.url)
        embed.set_timestamp(self.timestamp)
        embed.set_author(name=self.author.name, url=self.author.url, icon_url=self.author.icon_url)
        embed.set_footer(text=self.footer.text, icon_url=self.footer.icon_url)

        if self.fields:
            for i in self.fields:
                embed.add_embed_field(name=i.name, value=i.value, inline=i.inline)

        return embed
