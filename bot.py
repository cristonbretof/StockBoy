import os
from datetime import datetime as dt
from datetime import date
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks

from botcontroller import BotController
from src.algos.algos import *


symbols_list = "hqu.to hsu.to heu.to hfu.to tqqq nail cure utsl retl spxl fas arkw hura.to hxu.to soxl "
sl_list = [-0.03, -0.02, -0.04, -0.025, -0.035, -0.055, -0.03, -0.04, -0.04, -0.03, -0.035, -0.03, -0.03, -0.015, -0.08]
RatingStars = "4/5 4/5 4/5 3/5 5/5 4/5 4/5 3/5 4/5 2/5 3/5 2/5 4/5 2/5 5/5 1/5" 



def main():

    # Permet au bot de détecter la présence
    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        print("Bot up and running")

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # Setup Bot Controller
    bc = BotController()
    bc.add_speculbot(algo=macd, symbols=symbols_list, name="MACkDy", stop_loss=sl_list)
    
    # Start notification to Webhook
    notif_loop.start(bc=bc)

    try:
        # Start Discord Bot
        bot.run(TOKEN)

    except KeyboardInterrupt:
        bc.send_notification(name="BotController", content="HELP!")
        quit()


#boucle infinie
@tasks.loop(seconds = 10) # repeat after every 1800 seconds
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
