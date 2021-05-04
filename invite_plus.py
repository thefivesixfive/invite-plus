# fivesixfive automod
# version 0.0.0

# imports
from dotenv import load_dotenv
from os import getenv
from discord import utils, Embed
from discord.ext import commands

# fetch env vars
load_dotenv()
TOKEN = getenv('TOKEN')

# create client
bot = commands.Bot(command_prefix='invite+')

# log startup
@bot.event
async def on_ready():
    # TODO log output via SMS
    print(f'[+] {bot.user} online!')

#
# commands
#

# echo
@bot.command(name="echo")
async def echo(ctx, *args):
    # make sure there's channel args
    if len(args) < 2:
        await ctx.author.send("You haven't supplied a proper number of arguments! `.echo #general hello`")
        await ctx.delete()
        return
    # filter out #, get guild by id, grab channel by name
    channel = args[0].replace("#", "")
    channel = utils.get(ctx.guild.channels, name=channel)
    # if channel does not  exist, raise error, remove msg, and quit
    if channel == None:
        await ctx.author.send("That channel does not exist!")
        await ctx.delete()
        return
    # if channel does exist, send message
    else:
        # join the rest of the args together
        await channel.send(" ".join(args[1:]))
        return

# return organized invites, filter out
def gen_lb(raw_invites:list):
    # loop through raw_invite_list, remove duplicate invitees, total sum uses
    invites = {}
    for invite in raw_invites:
        # Add  value, otherwise, create
        try:
            invites[invite.inviter.name].uses += invite.uses
        except Exception as _:
            invites[invite.inviter.name] = invite
    # clean funky characters
    clean_invites = {}
    for username in invites:
        new_user = ''.join(char for char in username if char.isalnum())
        # replace
        clean_invites[new_user] = invites[username]
    # sort invites by uses, descending, returns keys in order
    key = sorted(clean_invites, reverse=True, key=lambda invite: clean_invites[invite].uses)
    print((clean_invites, key))  
    # return
    return (clean_invites, key)

# leaderboard
@bot.command(name="leaderboard")
async def leaderboard(ctx):
    # grab invites
    raw_invite_list = await ctx.guild.invites()
    # generate invite leaderboard
    invites, ranked_keys = gen_lb(raw_invite_list)
    # grab longest username
    user_col_size = 0
    for user in invites:
        if len(user) > user_col_size:
            user_col_size = len(user)
    # generate header
    col_padding = abs(user_col_size-8)
    leaderboard = f"Username{' '*col_padding} | Uses\n"
    # spacing line         
    leaderboard += f"--------{'-'*col_padding}-|-----\n"
    # generate leaderboard 
    for user in ranked_keys:
        # grab invite      
        invite = invites[user]
        # grab spacing inbetween name / uses
        col_padding = user_col_size - len(user)
        # generate line     
        leaderboard += f"{user}{' '*col_padding} | {invite.uses}\n"
    # send to discord via embed
    embed = Embed(title="", color=0x7289da)
    embed.add_field(name="Invite Leaderboard", value="```"+leaderboard+"```", inline=False)   
    await ctx.channel.send(embed=embed)


# execute bot
bot.run(TOKEN)