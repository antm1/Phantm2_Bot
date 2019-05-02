import json

from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config.json') as file_in:
            self.config = json.load(file_in)

    def update_config(self):
        with open('config.json', 'r') as file_in:
            self.config = json.load(file_in)

    def update_file(self):
        with open('config.json', 'w') as file_out:
            json.dump(self.config, file_out, indent=2, sort_keys=True)


    def is_admin():
        def predicate(ctx):
            with open('config.json', 'r') as file_in:
                adminlist = json.load(file_in)
            for a in adminlist['admin_ids']:
                if int(a) == ctx.message.author.id:
                    return ctx.message.author.id == int(a)

        return commands.check(predicate)

    def is_mod():
        def predicate(ctx):
            with open('config.json', 'r') as file_in:
                modlist = json.load(file_in)
            for m in modlist['mod_ids']:
                if int(m) == ctx.message.author.id:
                    return ctx.message.author.id == int(m)
            with open('config.json', 'r') as file_in:
                adminlist = json.load(file_in)
            for a in adminlist['admin_ids']:
                if int(a) == ctx.message.author.id:
                    return ctx.message.author.id == int(a)

        return commands.check(predicate)

    @commands.command(
        name="addadmin",
        aliases=['giveadmin','aadmin', 'promoadmin', 'padmin', 'promoteadmin'],
        pass_context=True,
        hidden=True,
        usage = '<text>'
    )
    @commands.is_owner()
    async def add_admin(self, ctx, *new_admin):
        self.update_config()
        try:
            member = ctx.message.mentions[0].id
        except IndexError:
            member = new_admin
        self.config['admin_ids'].append(str(member))
        self.update_file()
        added_admin = [members.mention for members in self.bot.get_all_members() if members.id == member][0]
        await ctx.send(content = "{} has been added as an admin! :smile:".format(added_admin))

    @commands.command(
        name="removeadmin",
        aliases=['radmin', 'deladmin', 'kickadmin', 'deadmin'],
        pass_context=True,
        hidden=True,
        usage = '<text>'
    )
    @commands.is_owner()
    async def remove_admin(self, ctx, *admin):
        self.update_config()
        try:
            member = ctx.message.mentions[0].id
            print(member)
        except IndexError:
            member = new_admin
        self.config['admin_ids'].remove(str(member))
        self.update_file()
        removed_admin = [members.mention for members in self.bot.get_all_members() if members.id == member][0]
        await ctx.send(content="{} has been removed as an admin".format(removed_admin))

    @commands.command(
        name="addmod",
        aliases=['givemod','amod', 'promomod', 'pmod', 'promotemod'],
        pass_context=True,
        hidden=True,
        usage = '<text>'
    )
    @is_admin()
    async def add_mod(self, ctx, *new_mod):
        print('add admin function was tripped succesfully')
        self.update_config()
        try:
            member = ctx.message.mentions[0].id
        except IndexError:
            member = new_mod
        self.config['mod_ids'].append(str(member))
        self.update_file()
        added_mod = [members.mention for members in self.bot.get_all_members() if members.id == member][0]
        await ctx.send(content = "{} has been added as an mod! :smile:".format(added_mod))

    @commands.command(
        name="removemod",
        aliases=['rmod', 'delmod', 'kickmod', 'demod'],
        pass_context=True,
        hidden=True,
        usage = '<text>'
    )
    @is_admin()
    async def remove_mod(self, ctx, *mod):
        self.update_config()
        try:
            member = ctx.message.mentions[0].id
        except IndexError:
            member = new_mod
        self.config['mod_ids'].remove(str(member))
        self.update_file()
        removed_mod = [members.mention for members in self.bot.get_all_members() if members.id == member][0]
        await ctx.send(content="{} has been removed as a mod".format(removed_mod))

    @commands.command(
        name="reload",
        aliases=['reloadcog','cogload', 'rcog', 'reloadcogs', 'rcogs', 'cogsload'],
        pass_context=True,
        hidden=True,
        usage = '<text>'
    )
    @is_admin()
    async def reload_cog(self, ctx):

        # Next we get the message with the command in it.
        msg = ctx.message.content

        # Extracting the text sent by the user
        # ctx.invoked_with gives the alias used
        # ctx.prefix gives the prefix used while invoking the command
        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        text = msg[len(prefix_used) + len(alias_used):]

        # Next, we check if the user actually passed some text
        if text == '':
            # User didn't specify the cog

            await ctx.send(content='You need to specify the cog(s) you want to reload!')

            pass
        else:
            # User specified the cog.

            file_string = (f"{text}")
            reload_list = file_string.split()
            for x in reload_list:
                try:
                    self.bot.reload_extension('cogs.' +str(x))
                    await ctx.send(content='The cog ' + str(x) + ' was reloaded successfully')

                except:
                    await ctx.send(content='The cog ' + str(x) + ' was spelled wrong or does not exist or has an error in it')
                #print(x)

            pass

        return


def setup(bot):
    bot.add_cog(Admin(bot))
