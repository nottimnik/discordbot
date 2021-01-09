import discord
import random
import wikipedia
import asyncio
import datetime
import json
from discord.ext import commands

#Custom Prefix for every server
def get_prefix(client, message):
    try:
        with open(r"database\prefixes.json", "r") as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]
    except:
        return "!"

client = commands.Bot(command_prefix= get_prefix)

#remove the default help command
client.remove_command("help")

@client.event #store the defaul prefix in the database
async def on_guild_join(guild):
    with open(r"database\prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "!"

    with open(r"database\prefixes.json", "w")as f:
        json.dump(prefixes, f, indent=4)

@client.event #deletes the prefix from the database if the bot leavea the server
async def on_guild_remove(guild):
    with open(r"database\prefixes.json", "r") as f:
        prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open(r"database\prefixes.json", "w")as f:
            json.dump(prefixes, f)

#Leveling System:
@client.event
async def on_message(message):
    if not message.author.bot:
        with open(r'database\level.json','r') as f:
            users = json.load(f)
        await update_data(users, message.author,message.guild)
        await add_experience(users, message.author, 4, message.guild)
        await level_up(users, message.author,message.channel, message.guild)

        with open(r'database\level.json','w') as f:
            json.dump(users, f)
    await client.process_commands(message)

async def update_data(users, user,server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1

async def add_experience(users, user, exp, server):
  users[str(user.guild.id)][str(user.id)]['experience'] += exp

async def level_up(users, user, channel, server):
  experience = users[str(user.guild.id)][str(user.id)]['experience']
  lvl_start = users[str(user.guild.id)][str(user.id)]['level']
  lvl_end = int(experience ** (1/4))
  if str(user.guild.id) != '757383943116030074':
    if lvl_start < lvl_end:
      await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
      users[str(user.guild.id)][str(user.id)]['level'] = lvl_end

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
    await ctx.send(f"Hello!")


#-----------------------------------------


##Custom Help Command:
@client.group(invoke_without_command = True)
async def help(ctx):
    em = discord.Embed(title = "SOME1 Help Commands")
    em.add_field(name = "⚒️ Moderation", value = "`!help moderation`")
    em.add_field(name = "⭐ Level System", value = "`!help levelsystem`")
    em.add_field(name = "😂 Fun", value = "`!help fun`")
    em.add_field(name = "💬 Social", value = "`!help social`")
    em.add_field(name = "📣 Polls", value = "`!help polls`")
    em.add_field(name = "🎉 Giveaway", value = "`!help giveaways`")
    em.add_field(name = "👑 Premium", value = "`!help premium`")
    em.add_field(name = "⚙ Other", value = "`!help other`")
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

@help.command()
async def fun(ctx):
    em = discord.Embed(title = "😂 Fun Commands")
    em.add_field(name = "!coinflip", value = "`Flips a coin.`", inline = False)
    em.add_field(name = "!wikipedia [topic]", value = "`Searches for a specific topic on wikipedia.`", inline = False)
    em.add_field(name = "!randomnumber (optional number 1) (optional number 2)", value = "`Generates a random number between the specified 2 numbers.`\n*if not specified it will just generate a random number*")
    await ctx.send(embed = em)

@help.command()
async def social(ctx):
    em = discord.Embed(title = "💬 Social Commands")
    em.add_field(name = "!hug [member]", value = "`Hug a member.`", inline = False)
    em.add_field(name = "!kiss [member]", value = "`Kiss a member.`", inline = False)
    await ctx.send(embed = em)

@help.command()
async def polls(ctx):
    em = discord.Embed(title = "📣 Polls Commands")
    em.add_field(name = "!poll [message]", value = "`Creates a poll with the introduced message.`")
    await ctx.send(embed = em)

@help.command()
async def giveaways(ctx):
    em = discord.Embed(title = "🎉 Giveaways Commands")
    em.add_field(name = "!giveaway", value = "`Creates a new giveaway.`")
    em.add_field(name = "!reroll [channel] [id of the giveaway]", value = "`Rerolls the winners of the giveaway.`")
    await ctx.send(embed = em)

@help.command()
async def other(ctx):
    em = discord.Embed(title = "⚙ Other Commands")
    em.add_field(name = "!prefix [new prefix]", value = "`Changes the prefix of the bot.`\n*Required Permission: Administrator*")
    em.add_field(name = "!developers", value = "The Developers behind SOME1.")
    await ctx.send(embed = em)

@help.command()
async def levelsystem(ctx):
    em = discord.Embed(title = "⭐ Level System's Commands")
    em.add_field(name = "!level or !rank", value = "`See your level and xp.`", inline = False)
    em.add_field(name = "!level [member] or !rank [member]", value = "`See the mentioned member's xp and level.`")

@help.command()
async def premium(ctx):
    em = discord.Embed(title = "👑 Premium", description = "The Premium Version of SOME1's is totally something different.")
    await ctx.send(embed = em)

#Some other commands:
@client.command() #Developer Command to see the developers of SOME1
async def developers(ctx):
    em = discord.Embed(title = "SOME1's Developers", description = "The team behind SOME1.")
    em.add_field(name = "Timnik#4158", value = "Main Developer", inline = False)
    em.add_field(name = "BossuJmek2k19#7072", value = "Made the Audio Bot", inline = False)
    await ctx.send(embed = em)

@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        em = discord.Embed(title = "We couldn't find that :/")
        await ctx.send(embed = em)

##Moderation Commands:
@client.command() ##The Clear Command
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=1):
    amount = amount + 1
    await ctx.channel.purge(limit = amount)
    await ctx.send(f"Successfully deleted {amount-1} messages!")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')

@client.command(aliases=["k"]) ##The Kick Command
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *,reason = "None"):
    await member.send(f"You have been kicked. *Reason: {reason}*")
    await ctx.send(f"{member} has been kicked from the server! *Reason: {reason}*")
    await member.kick(reason=reason)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the member you want to kick. Usage: `!kick [member] (optional reason)`')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')

@client.command(aliases=["b"]) ##The Ban Command
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *,reason = "None"):
    await member.send(f"You have been banned. *Reason: {reason}*")
    await ctx.send(f"{member} has been banned from the server! *Reason: {reason}*")
    await member.ban(reason=reason)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the member you want to ban. Usage: `!ban [member] (optional reason)`')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')

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

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the member you want to unban. Usage: `!unban [member]`')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')

@client.command() #The mute command
@commands.has_permissions(manage_messages = True)
async def mute(ctx, member: discord.Member, *, reason="None"):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    ##If the server doesn't have a Muted role, the bot will create one:
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        ##The Permissions of the mutedRole
        permissions = discord.Permissions()
        permissions.update(send_messages = False, speak = True) 

        ##Sets The Permissions of the mutedRole
        await mutedRole.edit(permissions = permissions)

    await member.add_roles(mutedRole)
    await ctx.send(f"{member} has been muted. *Reason: {reason}*")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the member you want to mute. Usage: `!mute [member] (optional reason)`')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')

@client.command(aliases = ["um"]) #The unmute command
@commands.has_permissions(manage_messages = True)
async def unmute(ctx, member : discord.Member, *,reason="None"):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(mutedRole)
    await ctx.send (f"{member} has been unmuted.")

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the player you want to unmute. Usage: `!unmute [member]`')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')

@client.command()
@commands.has_permissions(manage_roles = True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"Successfully given {role.mention} to {user.mention}")

@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the player and the role you want to add to. Usage: `!addrole [member] [role]`')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')

@client.command()
@commands.has_permissions(manage_roles = True)
async def delrole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"Successfully remove {role.mention} from {user.mention}")

@delrole.error
async def delrole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the player and the role you want to remove from. Usage: `!delrole [member] [role]`')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')


#Fun Commands:
@client.command()
async def coinflip(ctx):
    choices = ["Bead", "Tail"]
    await ctx.send(":coin: The coin fliped: **" + random.choice(choices) +"**")

@client.command()
async def randomnumber(ctx, n1 = 0, n2 = 1000000000):
    await ctx.send("Your random number is " + str(random.randint(n1, n2)))

@client.command() #Command that users can use to search articles on wikipedia
async def wiki(ctx, *,topic = "wikipedia"):
    try:
        page = wikipedia.page(wikipedia.suggest(topic))
        if(len(page.summary)>2000): #if the summary of the page is bigger than 2000 characters, the summary will be resized to 2000 characters.
            em = discord.Embed(title = ":globe_with_meridians: " + str(topic) + " | Summary", description = str(str('%.2000s') % str(page.summary)))
            em.set_footer(text=page.url)
        else:
            em = discord.Embed(title = str(topic), description = page.summary)
            em.set_footer(text="Source: " + page.url)
        await ctx.send(embed = em)
    except: #if the wikipedia API return a error(didn't find a article or there are too many articles) the author will be announced
        await ctx.send(":globe_with_meridians: There are too many/none topics with this keyword on wikipedia. Please be more specific.")

@wiki.error
async def wiki_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the topic you want to search for. Usage: `!wiki [topic]`')

#Social Commands:
@client.command()
async def hug(ctx, member: discord.Member):
    ##Links of gifs that the bot will send
    gifs = ["https://gifimage.net/wp-content/uploads/2017/09/anime-comfort-hug-gif-14.gif",
    "https://78.media.tumblr.com/18fdf4adcb5ad89f5469a91e860f80ba/tumblr_oltayyHynP1sy5k7wo1_500.gif",
    "https://media.tenor.co/images/42922e87b3ec288b11f59ba7f3cc6393/raw",
    "https://i.imgur.com/iI3o7t0.gif",
    "https://pa1.narvii.com/5722/d741ae3145e17efa00e262e3a2ead6f16e3f1289_hq.gif",
    "https://thumbs.gfycat.com/AchingKlutzyJohndory-max-1mb.gif",
    "https://thumbs.gfycat.com/SilkyAmbitiousHarvestmen-max-1mb.gif"
    ]
    em = discord.Embed(title = f"{member} you received a hug :hugging:")
    em.set_image(url=str(random.choice(gifs)))
    await ctx.send(embed = em)

@hug.error
async def hug_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the member you want to hug. Usage: `!hug [member]`')

@client.command()
async def kiss(ctx, member : discord.Member):
    await ctx.send(f"{member.mention} someone gave you a kiss :kissing_heart:")

@kiss.error
async def kiss_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the member you want to kiss. Usage: `!kiss [member]`')

#Polls Commands:
@client.command()
@commands.has_permissions(administrator = True)
async def poll(ctx,*,message):
    try:
        em = discord.Embed(title = ":mega:  POLL", description =f"{message}")
        msg = await ctx.send(embed=em)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
    except:
        await ctx.send("Invalid Syntax! Please use the correct version: **`!poll [message]`**")

@poll.error
async def poll_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')

#Giveaway Commands:
def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" :3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

@client.command()
@commands.has_permissions(administrator = True)
async def giveaway(ctx):
    await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

    questions = ["Which channel should it be hosted in?",
    "What should be the duration of the giveaway? (s|m|h|d)",
    "What is the prize of the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for("message", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You didn\'t answer in time, please be quicker next time!")
            return
        else:
            answers.append(msg.content)
    
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return
    
    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
        return 
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time!")
        return

    prize = answers[2]
     
    await ctx.send(f"The Giveaway wille be in {channel.mention} and will last {answers[1]} seconds!")

    em = discord.Embed(title = "Giveaway!", description = f"{prize}")
    em.add_field(name = "Hosted by:", value = ctx.author.mention)
    em.set_footer(text= f"Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = em)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(time)

    new_msg = await channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! {winner.mention} won {prize}!")

@giveaway.error
async def giveaway_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')

@client.command()
@commands.has_permissions(administrator = True)
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
    try: 
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was entered incorrectly.")
        return

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! The new winner is {winner.mention}!")

@reroll.error
async def reroll_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')

@client.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx, prefix):
    with open(r"database\prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open(r"database\prefixes.json", "w")as f:
        json.dump(prefixes, f)   
    await ctx.send(f"The new prefix is `{prefix}`.")

@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permssion to use that command :/')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify what the new prefix will be. Usage: `!prefix [new prefix]`")

##Level/Rank Command:
@client.command(aliases = ['rank','lvl'])
async def level(ctx,member: discord.Member = None):

    if not member:
        user = ctx.message.author
        with open(r'database\level.json','r') as f:
            users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(user.id)]['level']
        exp = users[str(ctx.guild.id)][str(user.id)]['experience']

        embed = discord.Embed(title = 'Level {}'.format(lvl), description = f"{exp} XP " ,color = discord.Color.green())
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
    else:
      with open(r'database\level.json','r') as f:
          users = json.load(f)
      lvl = users[str(ctx.guild.id)][str(member.id)]['level']
      exp = users[str(ctx.guild.id)][str(member.id)]['experience']
      embed = discord.Embed(title = 'Level {}'.format(lvl), description = f"You have {exp} XP" ,color = discord.Color.green())
      embed.set_author(name = member, icon_url = member.avatar_url)

      await ctx.send(embed = embed)

@level.error
async def level_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        em = discord.Embed(title="This member doesn't have a profile :(", color = 15158332)
        await ctx.send(embed = em)

client.run("TOKEN")