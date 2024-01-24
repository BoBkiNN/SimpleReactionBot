import disnake
from disnake.ext import commands

intents = disnake.Intents.default()
intents.reactions = True
bot = commands.InteractionBot(intents=intents)

########### CONFIG ###########

MESSAGE_ID = 0
TOKEN = "TOKEN"
EMOJI_TO_ROLE = {
    
}

## Example EMOJI_TO_ROLE:
# EMOJI_TO_ROLE = {
#    "💀": 1199390475912761424
# }

######### CONFIG END #########

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload: disnake.RawReactionActionEvent):
    rid = EMOJI_TO_ROLE.get(str(payload.emoji))
    if rid == None or payload.message_id != MESSAGE_ID:
        return
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    role = message.guild.get_role(rid)
    if role == None:
        return
    member = await message.guild.get_or_fetch_member(payload.user_id)
    await member.add_roles(role, reason=f"Reacted on {message.id}")
    print(f"Given role {rid} to", member.id)

@bot.event
async def on_raw_reaction_remove(payload: disnake.RawReactionActionEvent):
    rid = EMOJI_TO_ROLE.get(str(payload.emoji))
    if rid == None or payload.message_id != MESSAGE_ID:
        return
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    role = message.guild.get_role(rid)
    if role == None:
        return
    member = await message.guild.get_or_fetch_member(payload.user_id)
    await member.remove_roles(role, reason=f"Unreact {message.id}")
    print(f"Revoked role {rid} from", member.id)

if __name__ == "__main__":
    if MESSAGE_ID == None or MESSAGE_ID == 0 or len(EMOJI_TO_ROLE) == 0 or TOKEN == None or TOKEN == "TOKEN":
        print("Message id or EMOJI_TO_ROLE map or token not set")
        exit(0)
    bot.run(TOKEN)
