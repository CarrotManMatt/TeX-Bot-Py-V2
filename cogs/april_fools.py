"""Contains cog classes for all april-fools features."""

import datetime
import logging
from typing import TYPE_CHECKING, override

from discord.ext import tasks

from config import settings
from utils import TeXBotBaseCog
from utils.error_capture_decorators import capture_guild_does_not_exist_error

if TYPE_CHECKING:
    from collections.abc import Sequence
    from logging import Logger
    from typing import Final

    from utils import TeXBot

__all__: "Sequence[str]" = ("AprilFoolsTaskCog",)

logger: "Final[Logger]" = logging.getLogger("TeX-Bot")


class AprilFoolsTaskCog(TeXBotBaseCog):
    """Cog class that defines the April Fools' Day tasks."""

    @override
    def __init__(self, bot: "TeXBot") -> None:
        """Start all task managers when this cog is initialised."""
        _ = self.send_morning_message.start()
        _ = self.send_evening_message.start()

        super().__init__(bot)

    @override
    def cog_unload(self) -> None:
        """
        End all running tasks whenever the tasks cog is unloaded.

        This may be run dynamically or when the bot closes.
        """
        self.send_morning_message.cancel()
        self.send_evening_message.cancel()

    @tasks.loop(time=datetime.time(9, 30, tzinfo=datetime.UTC))
    @capture_guild_does_not_exist_error
    async def send_morning_message(self) -> None:
        """One-off task to send a message in the evening."""
        self.bot.general_channel.send(settings["APRIL_FOOLS_MORNING_MESSAGE"])

    @tasks.loop(time=datetime.time(20, 15, tzinfo=datetime.UTC))
    @capture_guild_does_not_exist_error
    async def send_evening_message(self) -> None:
        """One-off task to send a message in the evening."""
        self.bot.general_channel.send(settings["APRIL_FOOLS_EVENING_MESSAGE"])
