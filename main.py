import disnake
from disnake.ext import commands

intents = disnake.Intents.default()
intents.reactions = True

bot = commands.InteractionBot(intents=intents)

MESSAGE_ID = 211111111111111111111
ROLE_ID = 1111111111111111111111
TOKEN = "None"
EMOJI_ID = None # set to none to trigger on any emoji

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload: disnake.RawReactionActionEvent):
    if EMOJI_ID != None and EMOJI_ID != payload.emoji.id:
        return
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    
    if payload.message_id == MESSAGE_ID:
        role = message.guild.get_role(ROLE_ID)
        if role == None:
            return
        member = await message.guild.get_or_fetch_member(payload.user_id)
        await member.add_roles(role, reason=f"Reacted on {message.id}")
        print("Given role to", member.id)

@bot.event
async def on_raw_reaction_remove(payload: disnake.RawReactionActionEvent):
    if EMOJI_ID != None and EMOJI_ID != payload.emoji.id:
        return
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    
    if payload.message_id == MESSAGE_ID:
        role = message.guild.get_role(ROLE_ID)
        if role == None:
            return
        member = await message.guild.get_or_fetch_member(payload.user_id)
        await member.remove_roles(role, reason=f"Unreact {message.id}")
        print("Revoked role from", member.id)

if __name__ == "__main__":
    if MESSAGE_ID == None or ROLE_ID == None or TOKEN == None or TOKEN == "TOKEN":
        print("Message id or role id or token not set")
        exit(0)
    bot.run(TOKEN)
