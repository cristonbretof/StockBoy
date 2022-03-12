import os
from datetime import datetime as dt
from datetime import date
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks

from botcontroller import BotController
from src.algos import algos
from src.utils.discordparser import *


symbols_list = "hqu.to hsu.to heu.to hfu.to tqqq nail cure utsl retl spxl fas arkw hura.to hxu.to soxl"
sl_list = [-0.03, -0.02, -0.04, -0.025, -0.035, -0.055, -0.03, -0.04, -0.04, -0.03, -0.035, -0.03, -0.03, -0.015, -0.08]
RatingStars = "4/5 4/5 4/5 3/5 5/5 4/5 4/5 3/5 4/5 2/5 3/5 2/5 4/5 2/5 5/5 1/5"

def main():

    #intents = discord.Intents.all()
    #bot = commands.Bot(command_prefix='$', intents=intents)
    bot = commands.Bot(command_prefix='$')

    # Setup Bot Controller
    bc = BotController()

    @bot.event
    async def on_ready():
        print("SpeculBot up and running!")

    @bot.command(name='add', help=f"Add a bot to SpeculBot \n{format_add_bot}")
    async def add_bot(ctx, *args):
        content = await parse_add_bot_command(ctx, args)
        if content is None: return
        bc.add_speculbot(algo=content["algo"], 
                        name=content["name"],
                        symbols=" ".join(content["symbols"]),
                        stop_loss=content["stop_loss"])

        botname = content["name"]
        await ctx.send(f"Added {botname} to Bot list")

    @bot.command(name='remove', help="Remove a bot from SpeculBot \n$remove <name>")
    async def remove_bot(ctx, *args):
        content = await parse_remove_bot_command(ctx, args)
        if content is None: return
        bc.remove_speculbot(name=content["name"])

        botname = content["name"]
        await ctx.send(f"Removed {botname} from Bot list")
    
    @bot.command(name='list', help="List all bots in SpeculBot \n$list")
    async def list_bots(ctx, *args):
        list_of_bots = bc.list_all_bots()
        if len(list_of_bots) > 0:
            for i, bot in enumerate(list_of_bots):
                await ctx.send(f"[{i}] {bot}\n")
        else:
            await ctx.send("No bots currently running in SpeculBot")

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    # Start notification to Webhook
    notif_loop.start(bc=bc)

    try:
        # Start Discord Bot
        bot.run(TOKEN)

    except KeyboardInterrupt:
        bc.send_notification(name="BotController", content="HELP!")
        quit()


#boucle infinie
@tasks.loop(seconds = 1800) # repeat after every 1800 seconds
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
