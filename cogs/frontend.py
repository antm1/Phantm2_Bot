from discord.ext import commands
import discord
import json

class Frontend(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def update_crypto(self):
        with open('crypto.json', 'r') as file_in:
            self.crypto = json.load(file_in)

    @commands.command(
        name='a',
        description='[!a btc or !a btc resources] Provides a summary of fundamentals of a ticker you select (use any available ticker in place of btc in !a btc) (to expand specific section just add it to the command such as !a btc resources)',
        aliases= ['analyze', 'analysis'],
    )
    async def embed_command(self, ctx):

        msg = ctx.message.content

        # Extracting the text sent by the user
        # ctx.invoked_with gives the alias used
        # ctx.prefix gives the prefix used while invoking the command
        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        text = msg[len(prefix_used) + len(alias_used):]

        # Next, we check if the user actually passed some text
        if text == '':
            # User didn't specify the text

            await ctx.send(content='You need to specify the text!')

            pass
        else:
            # User specified the text.
            self.update_crypto()
            tickers = list(self.crypto)
            inputs = text.split()
            if inputs[0] in tickers:
                title = inputs[0]

                if len(inputs) == 1:
                    desc = '**' + str(self.crypto[inputs[0]][0]["name"]) + '** fundamental analysis summary'

                    embed = discord.Embed(
                        title=title,
                        description=desc,
                        color=0xA9A9A9
                    )
                    embed.add_field(name='CoinMarketCap', value= self.crypto[inputs[0]][0]["cmc"], inline=False)
                    keypoints = self.crypto[inputs[0]][0]["keyPoints"]
                    c = 0
                    keys = ''
                    while c < 3 and c < len(keypoints):
                        keys += str(c+1) +'. ' +keypoints[c] +'\n'
                        c += 1
                    embed.add_field(name='Key Points', value=keys, inline=False)

                    resources = self.crypto[inputs[0]][0]["resources"]
                    d = 0
                    res = ''
                    while d < 3 and d <len(resources):
                        res += str(d + 1) + '. ' + resources[d] + '\n'
                        d += 1
                    embed.add_field(name='Resources', value=res, inline=False)

                    await ctx.send(embed=embed)

                elif len(inputs)>=2:
                    section = inputs[1]
                    if inputs[1] == 'key' and inputs[2] == 'points' or inputs[1] == 'keypoints':
                        inputs[1] = 'keyPoints'
                        section = 'key points'
                    if inputs[1] == 'coinmarketcap' or inputs[1] == 'coin' and inputs[2] == 'market' and inputs[3] == 'cap':
                        inputs[1] = 'cmc'
                        section = 'CoinMarketCap'
                    label = title +' ' +str(section)
                    e = 0
                    fill = ''
                    sections = self.crypto[inputs[0]][0][inputs[1]]
                    if str(type(sections)) == "<class 'list'>":
                        while e < len(sections):
                            fill += str(e + 1) + '. ' + str(sections[e]) + '\n'
                            e += 1
                    else:
                        fill = sections

                    embed = discord.Embed(
                        title=label,
                        description=fill,
                        color=0xA9A9A9
                    )

                    await ctx.send(embed=embed)


            else:
                await ctx.send(content= "we don't have that available yet, the current list of available tickers is " +str(tickers))

            pass

        return

def setup(bot):
    bot.add_cog(Frontend(bot))
        # Adds the Basic commands to the bot
        # Note: The "setup" function has to be there in every cog file
