# -*- coding: utf-8 -*-
# meta developer: @chepuxmodules

# from .Hikka.hikka import loader, utils
from telethon import types
from .. import __version__, loader, utils, validators
from ..types import Config, ConfigValue
import openai
import requests


@loader.tds
class ChepuxGPTMod(loader.Module):
    """Задавайте вопросы chatgpt by @y9chebupelka (modded by @a1ezkfame xd)"""
    strings = {"name": "ChepuxGPT"}

    def __init__(self):
        self.config = Config(
            ConfigValue(
                option="OPENAI_API_KEY",
                default="None",
                value=self.db.get("chepuxgpt", "OPENAI_API_KEY", "None"),
                validator=validators.String(),
                doc="Ваш API ключ для OpenAI"
            ),
            ConfigValue(
                option="MODEL",
                default="gpt-3.5-turbo",
                value=self.db.get("chepuxgpt", "MODEL", "gpt-3.5-turbo"),
                validator=validators.String(),
                doc="Название модели для генерации ответов"
            )
        )
            

    async def gptcmd(self, message):
        """Используйте .gpt <вопрос> или ответьте на сообщение"""
        
        if self.config["OPENAI_API_KEY"] is None:
            await utils.answer(message, "<b>❗️ Вы не указали API ключ для OpenAI в конфиге модуля.</b>")
            return
        api_key = self.config["OPENAI_API_KEY"]
        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "❗️ <b>Вы не задали вопрос.</b>")
                return

        prompt = [{"role": "user", "content": question}]

        await message.edit("🧐 <b>Генерирую ответ...</b>")
        try:
            client = openai.AsyncOpenAI(api_key=api_key)
            response = await client.chat.completions.create(
                model=self.config["MODEL"],
                messages=prompt
            )
            answer = response.choices[0].message.content
            await utils.answer(message, f"❓ <b>Вопрос:</b> {question}\n<b><emoji document_id=5325583039848260951>🤓</emoji> Ответ:</b> {answer}")
        except Exception as e:
            await utils.answer(message, f"❗️ <b>Произошла ошибка:</b> {e}")
