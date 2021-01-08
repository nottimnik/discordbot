sers)

    await channel.send(f"Congratulations! {winner.mention} won {prize}!")

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


