# fivesixfive automod
# version 0.0.0

# imports
from dotenv import load_dotenv
from os import getenv
from discord import utils
from discord.ext import commands

# fetch env vars
load_dotenv()
TOKEN = getenv('TOKEN')

# create client
bot = commands.Bot(command_prefix='+')

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

# return organized invites
def grab_invites(invites:list):
    pass

# leaderboard
@bot.command(name="leaderboard", aliases=["lb", "leader"])
async def leaderboard(ctx):
    # grab invites
    raw_invite_list = await ctx.guild.invites()
    # loop through raw_invite_list, remove duplicate invitees, total sum uses
    invite_list = {}
    for invite in raw_invite_list:
        # Add  value, otherwise, create
        try:
            invite_list[invite.inviter.name] += invite.uses
        except Exception as _:
            invite_list[invite.inviter.name] = invite.uses
    # sort invites by uses, descending
    invite_list = sorted(invite_list, reverse=True, key=lambda invite:invite["uses"])
    # grab longest username
    user_col_size = 0
    for key in invite_list.keys():
        if len(key) > user_col_size:
            user_col_size = len(key)
    # generate header
    leaderboard = f"Username{' '*abs(user_col_size-8)}    Invites \n"
    # spacing line
    leaderboard += f"{''*len(leaderboard)}"
    # generate leaderboard
    lb_unsorted = {}
    for key in invite_list.keys():
        # get whitespace to align name column
        user_col_diff = user_col_size-len(key)
        # generate leaderboard row
        row = f"{key}{' '*user_col_diff}    {invite_list[key]}\n"
        # add row to dict to be sorted
        lb_unsorted[invite_list[key]]=row
    # sort leaderboard
    lb_sorted_key = sorted(lb_unsorted, reverse=True)
    # add sorted to leaderboard
    for key in lb_sorted_key:
        leaderboard+=lb_unsorted[key]
    # send to discord
    await ctx.channel.send("```"+leaderboard+"```")


# execute bot
bot.run(TOKEN)