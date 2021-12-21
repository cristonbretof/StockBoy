import os
from datetime import datetime as dt
from datetime import date
from dotenv import load_dotenv
from discord.ext import commands
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
        print("Bot up and running")

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # Setup Bot Controller
    bc = BotController()
    bc.add_speculbot(algo=macd, symbols="hqu.to hsu.to heu.to hfu.to tqqq nail cure utsl retl spxl", name="MACkDy", stop_loss=-0.04)
    
    # Start notification to Webhook
    notif_loop.start(bc=bc)

    try:
        # Start Discord Bot
        bot.run(TOKEN)

    except KeyboardInterrupt:
        bc.send_notification(name="BotController", content="HELP!")
        quit()


#boucle infinie
@tasks.loop(seconds = 600) # repeat after every 600 seconds
async def notif_loop(bc:BotController):
    now = dt.now()
    open_t = now.replace(hour=9, minute=31, second=2)
    close_t = now.replace(hour=16, minute=0, second=0)

    ## For time of day
    if now >= open_t and now <= close_t:
        ## For day  of the week
        if date.today().isoweekday() >= 1 and date.today().isoweekday() <= 5:
            bc.send_results()

if __name__ == "__main__":
    main()
