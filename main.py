import os
import discord
import random
import aiofiles
import youtube_dl
from keep_alive import keep_alive

from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = ";_;", intents = intents)

@client.event
async def on_connect():
	for file in ["reaction_roles.txt"]:
		async with aiofiles.open(file, mode = "a") as temp:
			pass
	async with aiofiles.open("reaction_roles.txt", mode = "r") as file:
		lines = await file.readlines()
		for line in lines:
			data = line.split(" ")
			client.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))
		
	print("Bot is ready!")

#help 
client.remove_command("help")
@client.group(invoke_without_command = True)
async def help(ctx):
	em = discord.Embed(title = "Help", description = "Use ;_;help <command> for help with a certain command", color = ctx.author.color)
	em.add_field(name = "Moderation", value = "clear, kick, ban, unban, whois, set_reaction, avatar")
	em.add_field(name = "Fun", value = "ditsu, randomnumber, coinflip, cr, eightball")
	await ctx.send(embed = em)

#Fun
#ditsu
@help.command()
async def ditsu(ctx):
	em = discord.Embed(title = "ditsu", description = "Prints a very true statement", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;ditsu")
	await ctx.send(embed = em)

@client.command()
async def ditsu(ctx):
	await ctx.send("ditsu is supreme!")

#randomnumber
@help.command()
async def randomnumber(ctx):
	em = discord.Embed(title = "randomnumber", description = "generates a random number between the specified numbers", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;randomnumber <num1> <num2>")
	await ctx.send(embed = em)

@client.command()
async def randomnumber(ctx, num1, num2):
	embed = discord.Embed(title = "random number generator", description = (random.randint(int(num1), int(num2))), color = ctx.author.color)
	await ctx.send(embed = embed)

#coinflip
@help.command()
async def coinflip(ctx):
	em = discord.Embed(title = "coinflip", description = "flips a coin to get heads or tails", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;coinflip")
	await ctx.send(embed = em)

@client.command()
async def coinflip(ctx):
    coinflip = ["Heads", "Tails"]
    await ctx.send(f"{random.choice(coinflip)}") 

#cool rate
@help.command()
async def cr(ctx):
	em = discord.Embed(title = "cool rate", description = "generates a percent to see how cool you are :sunglasses:", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;cr")
	await ctx.send(embed = em)

@client.command()
async def cr(ctx):
	embed = discord.Embed(title = "cool rate :sunglasses:", description = f"your not cool lol", color = ctx.author.color)
	await ctx.send(embed = embed)
	
@client.command()
async def coolrate(ctx):
	embed = discord.Embed(title = "cool rate :sunglasses:", description = f"You are {(random.randint(1, 101))}% cool", color = ctx.author.color)
	await ctx.send(embed = embed)

#8ball
@help.command()
async def eightball(ctx):
	em = discord.Embed(title = "eightball", description = "Gives a answer to your questions", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;eightball")
	await ctx.send(embed = em)

@client.command()
async def eightball(ctx):
	eightball = ["Yes."]
	await ctx.send(f"{random.choice(eightball)}") 

#Moderation
#clear
@help.command()
async def clear(ctx):
	em = discord.Embed(title = "clear", description = "clears the specified amount of messages", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;clear <amount>")
	await ctx.send(embed = em)

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 0):
	await ctx.message.delete()
	await ctx.channel.purge(limit = amount)
	if amount == 1:
		await ctx.send(f"Cleared {amount} message")
	else:
		await ctx.send(f"Cleared {amount} messages")

#kick
@help.command()
async def kick(ctx):
	em = discord.Embed(title = "kick", description = "kicks the specified user", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;kick <user> [reason]")
	await ctx.send(embed = em)

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = "No reason provided"):
	await ctx.send(member.name + " has been kicked because of: " + reason)
	await member.kick(reason = reason)

#ban
@help.command()
async def ban(ctx):
	em = discord.Embed(title = "ban", description = "bans the specified user", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;ban <user> [reason]")
	await ctx.send(embed = em)

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = "No reason provided"):
	await ctx.send(member.name + " has been banned because of: " + reason)
	await member.ban(reason = reason)

#unban
@help.command()
async def unban(ctx):
	em = discord.Embed(title = "unban", description = "unbans the specified user", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;unban <user>")
	await ctx.send(embed = em)

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_disc = member.split("#")
	for banned_entry in banned_users:
		user = banned_entry.user
		if(user.name, user.discriminator) == (member_name, member_disc):
			await ctx.guild.unban(user)
			await ctx.send(member_name + " has been unbanned")
			return
	await ctx.send(member + " was not found")

#whois
@help.command()
async def whois(ctx):
	em = discord.Embed(title = "whois", description = "gives details about the specified user", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;whois <user>")
	await ctx.send(embed = em)
																					
@client.command()
@commands.has_permissions(kick_members = True)
async def whois(ctx, member : discord.Member):
	embed = discord.Embed(title = member.name, description = member.mention, color = discord.Colour.blue())
	embed.add_field(name = "ID", value = member.id, inline = True)
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
	await ctx.send(embed = embed)

#reaction roles
@help.command()
async def set_reaction(ctx):
	em = discord.Embed(title = "set reaction", description = "sets up reaction roles for a message", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;set_reaction <role (must be one word)> <message id> <emoji>")
	await ctx.send(embed = em)

client.reaction_roles = []

@client.event
async def on_raw_reaction_add(payload):
	for role_id, msg_id, emoji in client.reaction_roles:
		if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
			await payload.member.add_roles(client.get_guild(payload.guild_id).get_role(role_id))

@client.event
async def on_raw_reaction_remove(payload):
	for role_id, msg_id, emoji in client.reaction_roles:
		if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
			guild = client.get_guild(payload.guild_id)
			await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))

@client.command()
@commands.has_permissions(manage_roles = True)
async def set_reaction(ctx, role: discord.Role = None, msg: discord.Message = None, emoji = None):
	if emoji.isdigit():
		try:
			emoji = client.get_emoji(emoji).name
		except:
			emoji = None
	if role != None and msg != None and emoji != None:
		await msg.add_reaction(emoji)
		client.reaction_roles.append((role.id, msg.id, str(emoji.encode("utf-8"))))
		
		async with aiofiles.open("reaction_roles.txt", mode = "a") as file:
			emoji_utf = emoji.encode("utf-8")
			await file.write(f"{role.id} {msg.id} {emoji_utf}\n")
		await ctx.channel.send("Reaction has been set.")
	else:
		await ctx.send("Invalid arguements.")

#avatar
@help.command()
async def avatar(ctx):
	em = discord.Embed(title = "avatar", description = "displays the specified users avatar.", color = ctx.author.color)
	em.add_field(name = "**Syntax**", value = ";_;avatar <user>")
	await ctx.send(embed = em)

@client.command()
async def avatar(ctx, *,  member : discord.Member = None):
  await ctx.send(member.avatar_url)
	
#errors
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("MissingPermissions")
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("MissingRequiredArguments")
	elif isinstance(error, commands.CommandNotFound):
		await ctx.send("CommandNotFound")
	elif isinstance(error, commands.MemberNotFound):
		await ctx.send("MemberNotFound")
	# elif isinstance(error, commands.CommandInvokeError):
	# 	await ctx.send("Error")
	else:
		raise error

#testing or commands that need help / organization
@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! In {round(client.latency * 300)}ms')

@client.command()
async def doubles(ctx, player1, player2, player3, player4):
	doublesPlayers = [player1, player2, player3, player4]
	team1player1 = (f"{random.choice(doublesPlayers)}")
	doublesPlayers.remove(team1player1)
	team1player2 = (f"{random.choice(doublesPlayers)}")
	doublesPlayers.remove(team1player2)
	team1 = []
	team1.append(team1player1)
	team1.append(team1player2)
	await ctx.send(f"{team1} vs {doublesPlayers}")

@client.command()
async def threes(ctx, player1, player2, player3, player4, player5, player6):
	threesPlayers = [player1, player2, player3, player4, player5, player6]
	team1player1 = (f"{random.choice(threesPlayers)}")
	threesPlayers.remove(team1player1)
	team1player2 = (f"{random.choice(threesPlayers)}")
	threesPlayers.remove(team1player2)
	team1player3 = (f"{random.choice(threesPlayers)}")
	threesPlayers.remove(team1player3)
	team1 = []
	team1.append(team1player1)
	team1.append(team1player2)
	team1.append(team1player3)
	await ctx.send(f"{team1} vs {threesPlayers}")

@client.command()
async def moo0dy(ctx):
	await ctx.send("moo0dy is ok sometimes but sometimes he sucks so bad")

@client.command()
async def zelats(ctx):
	await ctx.send("zelats kb is inconsistant bruv")

@client.command()
async def andy(ctx):
	await ctx.send("andy sucks")

@client.command()
async def a(ctx):
	await ctx.send("--userphone")

@client.command()
async def johnson(ctx):
	await ctx.send("johnson is 70 average")

@client.command()
async def justin(ctx):
	await ctx.send("justin time for deez nuts")

@client.command()
async def james(ctx):
	await ctx.send("@everyone")

@client.command()
async def abishan(ctx):
	await ctx.send("peach")

@client.command()
async def kajanan(ctx):
	task_loop.start() # important to start the loop

@tasks.loop(seconds=2)
async def task_loop():
	await ctx.send("@ditsu") 

@client.command()
async def dhanish(ctx):
	await ctx.send("3 CLASSES WTF")

@client.command()
async def michealli(ctx):
	await ctx.send("bruh micheal actual opp")


@client.command()
async def hotrate(ctx):
	rand = random.randint(1, 4)
	if rand == 1:
		embed = discord.Embed(title = "hot rate :sunglasses:", description = f"your not hot lol (1% to happen tho!)", color = ctx.author.color)
	elif rand == 101:
		embed = discord.Embed(title = "hot rate :sunglasses:", description = f"You are {rand}% hot, you melt everyone here lol", color = ctx.author.color)
	else:
		embed = discord.Embed(title = "hot rate :sunglasses:", description = f"You are {rand}% hot", color = ctx.author.color)
	await ctx.send(embed = embed)







keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)