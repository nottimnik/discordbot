import discord
from discord.ext import commands

client = commands.Bot(command_prefix="!")

##Status:
@client.event
async def on_ready():
    print("The Bot is online!")
    await client.change_presence(activity=discord.Game(name="!help | some1.xyz"))

@client.command()
async def hello(ctx):
    await ctx.send("Hello!")



##Moderation Commands:
@client.command(aliases=["c"]) ##The Clear Command
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=1):
    amount = amount + 1
    await ctx.channel.purge(limit = amount)
    await ctx.send(f"Successfully deleted {amount-1} messages!")

@client.command(aliases=["k"]) ##The Kick Command
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *,reason = "None"):
    await member.send(f"You have been kicked. *Reason: {reason}*")
    await ctx.send(f"{member} has been kicked from the server! *Reason: {reason}*")
    await member.kick(reason=reason)

@client.command(aliases=["b"]) ##The Ban Command
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *,reason = "None"):
    await member.send(f"You have been banned. *Reason: {reason}*")
    await ctx.send(f"{member} has been banned from the server! *Reason: {reason}*")
    await member.ban(reason=reason)

@client.command(aliases=["ub"]) ##The unban command
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split("#")

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name,member_disc):

            await ctx.guild.unban(user)
            await ctx.send(member_name + " has been unbanned!")
            return
        
    ctx.send(member + " was not found.")

@client.command(aliases=["m"]) #The mute command
@commands.has_permissions(manage_messages = True)
async def mute(ctx, member: discord.Member, *, reason="None"):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    ##If the server doesn't have a Muted role, the bot will create one:
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        ##The Permissions of the mutedRole
        permissions = discord.Permissions()
        permissions.update(send_messages = False, speak = False) 

        ##Sets The Permissions of the mutedRole
        await mutedRole.edit(permissions = permissions)

    await member.add_roles(mutedRole)
    await ctx.send(f"{member} has been muted. *Reason: {reason}*")

@client.command(aliases = ["um"])
@commands.has_permissions(manage_messages = True)
async def unmute(ctx, member : discord.Member, *,reason="None"):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(mutedRole)
    await ctx.send (f"{member} has been unmuted.")

client.run("")