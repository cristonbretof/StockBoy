from discord.ext import commands
from discord.ext import tasks

from src.algos import algos

# Help message formats
format_add_bot = "$add <algo> -n <name> <symbols> --sl [stop loss]"
format_remove_bot = "$remove <name>"

async def parse_add_bot_command(ctx, args: list) -> dict:
    content = {}
    if not args:
        await ctx.send(f"SpeculBot requires these arguments (stop loss is optional) \n{format_add_bot}")
        return None
    elif len(args) < 4:
        await ctx.send(f"SpeculBot requires at least 3 arguments (algo/name/symbols) \n{format_add_bot}")
        return None
    else:
        # Guaranties we have at least the 3 arguments we need
        try:
            # Get algorithm from its name, if it exists
            content["algo"] = getattr(algos, args[0])
        except AttributeError:
            await ctx.send(f"First argument <algo> must contain a valid algorithm to run")
            return None
        
        if not args[1] == "-n":
            await ctx.send(f"Second argument <name> must be preceded by '-n' tag")
            return None
        content["name"] = args[2]
        
        sl_index = 0
        for i, arg in enumerate(args[3:]):
            if arg == "--sl":
                sl_index = i
        
        if not sl_index:
            content["symbols"] = args[3:]
            content["stop_loss"] = []
        else:
            content["symbols"] = args[3:sl_index-1]
            content["stop_loss"] = args[sl_index+1:]
        return content


async def parse_remove_bot_command(ctx, args: list) -> dict:
    content = {}
    if not args:
        await ctx.send(f"Bot requires only one argument \n{format_remove_bot}")
    else:
        if len(args) == 1:
            content["name"] = args[0]
            return content
        else:
            await ctx.send(f"Bot requires only one argument \n{format_remove_bot}")