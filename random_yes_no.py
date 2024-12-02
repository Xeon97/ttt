
# -*- coding: utf-8 -*-

# This is a custom module for Hikka Userbot
# Author: Your Name
# Description: Randomly answers "yes" or "no" to questions when "Рома" is mentioned in the chat.

import random
from .. import loader, utils

class RandomYesNoMod(loader.Module):
    """Randomly answers 'yes' or 'no' to questions in a specific chat."""
    strings = {"name": "RandomYesNo"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "target_chat", None, "Chat ID where the bot will respond."
        )

    async def setchatcmd(self, message):
        """Set the current chat as the target chat.
        Usage: .setchat
        """
        self.config["target_chat"] = message.chat_id
        await message.edit(f"<b>Target chat set to:</b> {message.chat_id}")

    async def watcher(self, message):
        """Watches for 'Рома' in messages and replies with 'да' or 'нет'."""
        target_chat = self.config["target_chat"]
        if target_chat is None or message.chat_id != target_chat:
            return

        if "Рома" in (message.raw_text or ""):
            answer = random.choice(["Да", "Нет"])
            await message.reply(answer)
