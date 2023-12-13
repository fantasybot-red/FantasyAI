import discord
import dotenv
import os
import asyncio
from discord import app_commands
from chatgpt import ChatGPT
from discord.ext import tasks

dotenv.load_dotenv()

intents = discord.Intents.all()
bot = discord.Client(intents=intents)
bot.tree = discord.app_commands.CommandTree(bot)
gpt = ChatGPT()

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    
    if bot.user in message.mentions:
            if message.clean_content:
                list_m = []
                async with message.channel.typing():
                    mess_dict = {
                            "role": "user",
                            "content": message.content,
                            "name": message.author.id
                        }
                    list_m.append(mess_dict)
                    async for mess in message.channel.history(limit=50, before=message):
                        if mess.author.bot and mess.author != bot.user:
                            continue
                        if not mess.content:
                            continue
                        mess_dict = {
                            "role": "assistant",
                            "content": mess.content
                        }
                        if not mess.author.bot:
                            mess_dict["role"] = "user"
                            mess_dict["name"] = mess.author.id
                        list_m.append(mess_dict)
                    list_m.reverse()
                    print(list_m)
                    out_gpt = await gpt.create_new_chat(list_m)
                await message.reply(out_gpt)
        
        
        


@tasks.loop(seconds=10)
async def status_c():
    await bot.change_presence(activity=discord.Game(name="@ me and ask"))
    await asyncio.sleep(10)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} Guilds"))
    await asyncio.sleep(10)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{len(bot.users)} Users"))
    await asyncio.sleep(10)

@bot.event
async def on_ready():
    await bot.tree.sync()
    try:
        status_c.start()
        print("status task was created")
    except BaseException:
        pass
    print(f"Login As {bot.user}")


bot.run(os.getenv("token"))