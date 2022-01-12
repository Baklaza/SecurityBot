import discord
import os
import random

from discord.ext import commands
from discord.ext.commands.errors import RoleNotFound
from discord.utils import get


intents = discord.Intents.all()
discord.member = True
discord.reaction = True

bot = commands.Bot("-", intents = intents)

@bot.command() 
async def security(ctx):

    emoji_id = os.environ.get("EMOJI_ID")
    sec = bot.get_emoji(int(emoji_id))
    
    emojis = ['🎓', sec, '💼', '😀', '😃', '😄', '😁', '😅', '😂', '😇', '😉', '😊', '😋', '😌', '😍']
    msg = await ctx.send(f'Select {sec} for verification:')

    for i in range(len(emojis)):
        random.shuffle(emojis)
        await msg.add_reaction(emojis[0])


@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, name = 'Unverified')
    await member.add_roles(role)


@bot.event
async def on_raw_reaction_add(payload):
    emoji_id = os.environ.get("EMOJI_ID")
    channel_id = os.environ.get("CHANNEL_ID")
    if payload.message_id == int(channel_id) and payload.emoji.id == int(emoji_id):
        role = get(payload.member.guild.roles, name = 'Unverified')
        await payload.member.remove_roles(role)


        role = get(payload.member.guild.roles, name = 'Verified')
        await payload.member.add_roles(role)

        role = get(payload.member.guild.roles, name = 'Community')
        await payload.member.add_roles(role)


        await payload.member.send('Thank you for passing the verification. Welcome to Crypto & Music!')

token = os.environ.get("BOT_TOKEN")
bot.run(str(token))
