#Le code marche pas dans collab, mais marche très bien sous linux (AKA PopOS ou Raspberry PI OS par exemple)
import os
import json
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks

from src.speculbot import SpeculBot
import requests


class BotController:

    def __init__(self):
        self.bots = {}
        self.url = self.get_url()

    def get_url(self):
        with open(os.getcwd()+"/../bot_config.json", 'r')  as f:
            url = json.load(f)['url']
            return url

    def send_results(self):
        for name, bot in self.bots.items():
            results = bot.get_results()

            contents = ""
            self.send_notification(name=name, content=results)

    def send_notification(self, content: str, name: str):
        data = {
            "content" : content,
            "username" : name
        }

        result = requests.post(self.url, json=data)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            pass

    def add_speculbot(self, algo, symbol, name: str):
        self.bots[name] = SpeculBot(algo, symbol, name)
        self.bots[name].start()

    def remove_speculbot(self, name: str):
        self.bots[name].stop()
        self.bots[name].join()

    def shutdown(self):
        for bot in self.bots.values():
            bot.stop()
            bot.join()
