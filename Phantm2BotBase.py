from discord.ext import commands

def get_prefix(client, message):

    prefixes = ['!', '!!']    # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix

    if not message.guild:
        prefixes = ['!']   # Only allow '==' as a prefix when in DMs, this is optional

    # Allow users to @mention the bot instead of using a prefix when using a command. Also optional
    # Do `return prefixes` if u don't want to allow mentions instead of prefix.
    return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(                         # Create a new bot
    command_prefix=get_prefix,              # Set the prefix
    description='Lets do bot stuff',        # Set a description for the bot
    owner_id=YOUR DISCORD ID NUMBER HERE,   # Your unique User ID
    case_insensitive=True                   # Make the commands case insensitive
)

# case_insensitive=True is used as the commands are case sensitive by default

cogs = ['cogs.basic','cogs.embed', 'cogs.jsonEdit', 'cogs.admin']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    bot.remove_command('help')
    # Removes the help command
    # Make sure to do this before loading the cogs
    for cog in cogs:
        bot.load_extension(cog)
    return


#the bot.event section is to catch error thrown by failure of @commands.is_owner() and @commands.check(function)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You have no power here!")
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send ("Calm down there hotshot, try again in " +str(int(error.retry_after)) +" seconds!")
        return
# Finally, login the bot
bot.run('YOUR TOKEN HERE', bot=True, reconnect=True)
