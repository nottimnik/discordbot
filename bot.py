import discord
from discord.ext import commands

client = commands.Bot(command_prefix="!")

#remove the default help command
client.remove_command("help")

##Status:
@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("----------")
    await client.change_presence(activity=discord.Game(name="!help | some1.xyz"))

@client.command()
async def hello(ctx):
    await ctx.send("Hello!")

##Custom Help Command:
@client.group(invoke_without_command = True)
async def help(ctx):
    em = discord.Embed(title = "SOME1 Help Commands")
    em.add_field(name = "⚒️ Moderation", value = "!help moderation")
    em.add_field(name = "Fun", value = "help fun")
    await ctx.send(embed = em)

@help.command()
async def moderation(ctx):
    em = discord.Embed(title = "⚒️ Moderation Commands")
    em.add_field(name = "!clear (optional amount)", value = "`Clears messages in a particular channel.`\n*Required Permission: Manage Messages*")
    em.add_field(name = "!mute [member] (optional reason)", value = "`Mutes a specific member.`\n*Required Permission: Manage Messages*", inline = False)
    em.add_field(name = "!unmute [member]", value = "`Unmutes a member.`\n*Required Permission: Manage Messages*", inline = False)
    em.add_field(name = "!kick [member] (optional reason)", value = "`Kicks a member from the server.`\n*Required Permission: Kick Members*", inline = False)
    em.add_field(name = "!ban [member] (optional reason)", value = "`Bans a member from the server.`\n*Required Permission: Ban Members*", inline = False)
    em.add_field(name = "!unban [member]", value = "`Unbans a member from a the server.`\n*Required Permission: Ban Members*", inline = False)
    em.add_field(name = "!addrole [member] [role]", value = "`Adds a role to a member.`\n*Required Permission: Manage Roles*", inline = False)
    em.add_field(name = "!delrole [member] [role]", value = "`Removes a role from a member.`\n*Required Permission: Manage Roles*", inline = False)
    await ctx.send(embed = em)


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

@client.command(aliases = ["um"]) #The unmute command
@commands.has_permissions(manage_messages = True)
async def unmute(ctx, member : discord.Member, *,reason="None"):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(mutedRole)
    await ctx.send (f"{member} has been unmuted.")

@client.command()
@commands.has_permissions(manage_roles = True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"Successfully given {role.mention} to {user.mention}")

@client.command()
@commands.has_permissions(manage_roles = True)
async def delrole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"Successfully remove {role.mention} from {user.mention}")



client.run("TOKEN")
