import cairosvg as cpng
import discord.ext
import os, random
from discord import Option
from discord import Embed
from discord import default_permissions

#Sets the intents for the bot
intents = discord.Intents.all()
intents.message_content = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    #Prints the bots username and ping when started
    print(f'Logged in as {bot.user}')
    print(f'{round(bot.latency * 1000)} ms')


@bot.slash_command(description="Sends a flag")
async def flag(ctx):
    #Formats the string to match the guess
    flag = random.choice(os.listdir("Flags/"))
    flag = flag.strip(" ")
    flag = flag[:-4]
    flag = flag.lower()

    # Writes the current flag in the txt file
    with open("FlagInfo.txt", "w") as flagInfo:
        flagInfo.write(flag)

    #Converts the .svg file into a .png and
    cpng.svg2png(url=f"Flags/{flag}.svg", write_to=f"Pngs/NoCheating.png")
    file = discord.File(f"Pngs/NoCheating.png", filename=f"NoCheating.png")


    #Removes all files from the /Pngs directory
    os.system('rm Pngs/*')
    await ctx.respond(file=file)
    await ctx.send("> ## Submit answer with the 'Flag: ' or 'flag: ' keyword.")

def guessConvert(message):
    #Converts the message content into a format to match the current flag
    guess = message
    guess = guess[5:]
    guess = guess.replace(" ","")
    guess = guess.lower()
    return (guess)

@bot.event
async def on_message(message):
    global completed
    if message.content.startswith('Flag:') or message.content.startswith('flag:') and message.author.id != bot.user.id:

        with open("FlagInfo.txt", "r") as flagInfo:
            flag = flagInfo.readline()

        guess = guessConvert(message.content)
        print(f"Guess: {guess}")

        if guess == flag:
            await message.channel.send("Correct")
            completed = True
        else:
            await message.channel.send("Incorrect")


bot.run('Your Token Here')
