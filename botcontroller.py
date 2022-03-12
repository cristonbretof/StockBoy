#Le code marche pas dans collab, mais marche très bien sous linux (AKA PopOS ou Raspberry PI OS par exemple)
import os
import json

from src.speculbot import SpeculBot
import requests


class BotController:

    def __init__(self):
        self.bots = {}
        self.url = self.get_url()

    def get_url(self):
        with open(os.getcwd()+"/../bot_config.json", 'r')  as f:
            url = []
            url_dict = json.load(f)
            nb_of_urls = len(url_dict)
            for i in range(nb_of_urls):
                if (i+1) > 1:
                    url.append(url_dict["url{}".format(i+1)])
                else:
                    url.append(url_dict["url"])
            return url

    def send_results(self):
        for name, bot in self.bots.items():
            content = ""
            results = bot.get_results()
            for r in results:
                if r.result == 1:
                    msg = (r.name, "BUY")
                elif r.result == 0:
                    msg = (r.name, "SELL")
                else:
                    continue

                stock_res = f"Stock: {msg[0]} Signal: {msg[1]}"
                content += stock_res + "\n"

            if content != "":
                self.send_notification(name=name, content=content)

    def send_notification(self, content: str, name: str):
        data = {
            "content" : content,
            "username" : name
        }

        for i in range(len(self.url)):
            result = requests.post(self.url[i], json=data)

            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                pass

        
    def add_speculbot(self, algo, symbols, name: str, stop_loss:list):
        self.bots[name] = SpeculBot(algo, symbols, name, stop_loss=stop_loss)
        self.bots[name].start()

    def remove_speculbot(self, name: str):
        self.bots.pop(name)
        self.bots[name].stop()
        self.bots[name].join()

    def list_all_bots(self):
        return self.bots.keys()
            

    def shutdown(self):
        for bot in self.bots.values():
            bot.stop()
            bot.join()
