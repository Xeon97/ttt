
# -*- coding: utf-8 -*-
# meta developer: @YourTelegramUsername
# meta banner: https://via.placeholder.com/600x200.png?text=RPG+Game+Module

import random
from telethon import events

players = {}
items = {
    "sword": {"price": 50, "power": 10},
    "shield": {"price": 30, "defense": 5},
}

@loader.tds
class RPGGameMod(loader.Module):
    """RPG Game Module"""

    strings = {"name": "RPGGame"}

    async def profilecmd(self, message):
        """Показать ваш профиль игрока"""
        user_id = message.sender_id
        if user_id not in players:
            players[user_id] = {"level": 1, "exp": 0, "gold": 100, "items": []}
        profile = players[user_id]
        response = (
            f"🎮 Профиль игрока:\n"
            f"👤 Игрок: {message.sender.first_name}\n"
            f"⭐ Уровень: {profile['level']}\n"
            f"⚡ Опыт: {profile['exp']}\n"
            f"💰 Золото: {profile['gold']}\n"
            f"🎒 Предметы: {', '.join(profile['items']) or 'нет'}"
        )
        await message.reply(response)

    async def questcmd(self, message):
        """Начать новый квест"""
        question = random.choice([
            {"q": "Я без рук и без ног, но всех обнимаю. Что я?", "a": "кровать"},
            {"q": "Что всегда идёт, но никогда не приходит?", "a": "время"},
        ])
        await message.reply(f"🎲 Новый квест!\nЗагадка: {question['q']}")

        @self.client.on(events.NewMessage)
        async def check_answer(inner_event):
            if inner_event.text.lower() == question['a']:
                winner = inner_event.sender.first_name
                await inner_event.reply(f"🎉 {winner} правильно ответил на загадку!")
                players[inner_event.sender_id]["gold"] += 10
                self.client.remove_event_handler(check_answer)

    async def shopcmd(self, message):
        """Открыть магазин"""
        shop_items = "\n".join([f"{name} - {data['price']} золота" for name, data in items.items()])
        await message.reply(f"🛒 Магазин:\n{shop_items}\n\nДля покупки используйте .buy <предмет>")

    async def buycmd(self, message):
        """Купить предмет из магазина: .buy <item>"""
        item_name = message.text.split(" ", 1)[1].lower()
        user_id = message.sender_id
        if item_name not in items:
            await message.reply("❌ Предмет не найден!")
            return
        if players[user_id]["gold"] >= items[item_name]["price"]:
            players[user_id]["gold"] -= items[item_name]["price"]
            players[user_id]["items"].append(item_name)
            await message.reply(f"🎉 Вы купили {item_name}!")
        else:
            await message.reply("❌ У вас недостаточно золота!")
