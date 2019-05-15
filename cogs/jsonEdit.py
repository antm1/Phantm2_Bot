from discord.ext import commands
import json

# New - The Cog class must extend the commands.Cog class
class JsonEdit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def update_crypto(self):
        with open('crypto.json', 'r') as file_in:
            self.crypto = json.load(file_in)

    def update_file(self):
        with open('crypto.json', 'w') as file_out:
            json.dump(self.crypto, file_out, indent=2, sort_keys=True)


    def is_admin():
        def predicate(ctx):
            with open('config.json', 'r') as file_in:
                adminlist = json.load(file_in)
            for a in adminlist['admin_ids']:
                if int(a) == ctx.message.author.id:
                    return ctx.message.author.id == int(a)

        return commands.check(predicate)

    # Define a new command
    @commands.command(
        name='edit',
        description='The edit command',
        aliases=['e']
    )
    @is_admin()
    async def edit_command(self, ctx):
        # Define a check function that validates the message received by the bot
        def check(ms):
            # Look for the message sent in the same channel where the command was used
            # As well as by the user who used the command.
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        # First ask the user for the ticker
        await ctx.send(content='What is the ticker of the crypto info you want to edit?')

        # Wait for a response and get the ticker
        try:
            msg = await self.bot.wait_for('message', timeout = 30, check=check)
            if msg:
                ticker = msg.content
                # Confirms that the ticker was received.
                await ctx.send(content='You have selected **' + ticker + '** to edit.')
                self.update_crypto()
                if ticker in self.crypto:
                    await ctx.send(content='Which part of **' + ticker + '** do you want to to edit?')
                    rawcontents = self.crypto[ticker][0]
                    parts = ''
                    for p in rawcontents:
                        parts += p + ' '
                    await ctx.send(content=parts)
                    try:
                        section = await self.bot.wait_for('message', timeout=30, check=check)
                        if str(section.content) in rawcontents:
                            sec = str(section.content)
                            await ctx.send(content='You have selected **' + ticker + ' ' + sec + '** to edit.')
                            if str(type(self.crypto[ticker][0][sec])) == "<class 'str'>":
                                await ctx.send(content='The contents of which are\n-\n')
                                await ctx.send(content= self.crypto[ticker][0][sec])
                                await ctx.send(content='-\nWhat would you like to replace it with?')
                                try:
                                    newinput = await self.bot.wait_for('message', timeout=180, check=check)
                                    if newinput.content.startswith('!'):
                                        await ctx.send(content='You have entered a command, editing cancelled')
                                    else:
                                        self.crypto[ticker][0][sec] = newinput.content
                                        self.update_file()
                                        await ctx.send(content='**' + ticker + ' ' + sec + '** has been updated!')
                                except:
                                    await ctx.send(
                                        content='Edited content needs to be posted within 3 minutes in order to prevent bad edits, please start over!')
                            elif str(type(self.crypto[ticker][0][sec])) == "<class 'list'>":
                                seccontents = self.crypto[ticker][0][sec]
                                amount = len(seccontents)
                                await ctx.send(
                                    content= 'Which has **' + str(amount) + '** sections in it, please choose the one you want to edit.'
                                )
                                try:
                                    subsection = await self.bot.wait_for('message', timeout=30, check=check)
                                    subsec = int(subsection.content)
                                    if int(subsec) <= int(amount) and int(subsec) > 0:
                                        await ctx.send(content='You have selected section **' + str(subsec) + ' ** of **' + ticker + ' ' + sec + '** to edit.\nOf which the contents are\n-')
                                        await ctx.send(content= self.crypto[ticker][0][sec][int(subsec) - 1])
                                        await ctx.send(content='-\nWhat would you like to replace it with?')
                                        try:
                                            newcontent = await self.bot.wait_for('message', timeout=180, check=check)
                                            if newcontent.content.startswith('!'):
                                                await ctx.send(content='You have entered a command, editing cancelled')
                                            else:
                                                self.crypto[ticker][0][sec][int(subsec) - 1] = newcontent.content
                                                self.update_file()
                                                await ctx.send(content='Section **' + str(subsec) + ' ** of **' + ticker + ' ' + sec + '** has been updated!')
                                        except:
                                            await ctx.send(content='Edited content needs to be posted within 3 minutes in order to prevent bad edits, please start over!')
                                    else:
                                        await ctx.send(content= "Your selection didn't fall into the appropriate range, please start the process again!")
                                except:
                                    await ctx.send(
                                        content='You need to specify the an appropriate section on your first try within 30 seconds, please start the process again!')
                        else:
                            await ctx.send(content= "You didn't select a proper part of " +ticker +" to edit, please start the process again!")
                            return
                    except:
                        await ctx.send(content='You need to specify the part within 30 seconds, please start the process again!')

                else:
                    await ctx.send(content="It looks like we don't have that ticker yet or it doesn't have anything written in it yet.")

                pass


        except:
            # User didn't specify the ticker

            await ctx.send(content='You need to specify the ticker within 30 seconds, please try the command again!')

            pass

        return


def setup(bot):
    bot.add_cog(JsonEdit(bot))
    # Adds the JsonEdit commands to the bot
    # Note: The "setup" function has to be there in every cog file
