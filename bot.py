import time
import threading
import os
import json
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks

from botcontroller import BotController
from src.algos.algos import *


def main():

    # Permet au bot de détecter la présence
    #intents = discord.Intents.all()
    #bot = commands.Bot(command_prefix='$', intents=intents)
    bot = commands.Bot(command_prefix='$')

    @bot.event
    async def on_ready():
        print("bot up and running")

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # Setup Bot Controller
    bc = BotController()
    bc.add_speculbot(algo=macd, symbol="TQQQ", name="MACkDy")
    
    # Start notification to Webhook
    notif_loop.start(bc=bc)

    try:
        # Start Discord Bot
        bot.run(TOKEN)

    except KeyboardInterrupt:
        print(" <---- END OF PROGRAM")
        quit()


#boucle infinie
@tasks.loop(seconds = 300) # repeat after every 300 seconds
async def notif_loop(bc:BotController):
    bc.send_results()
    if len(threading.enumerate()) > 1:
        bc.send_notification()
        bc.shutdown()
        

if __name__ == "__main__":
    main()
