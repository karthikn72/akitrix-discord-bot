import asyncio
import json
import urllib.parse
import urllib.request

import discord
from discord.ext import commands


class UrbScraper(commands.Cog, name="UrbanScraper"):
    def __init__(self, bot):
        self.bot = bot
        self.data_dict = {}  # {query:[definition, example]}
        self.valid_messages = {}  # {message:[api, query, index]}

    @commands.command(name="urban")
    async def urban(self, ctx, *query):
        query = urllib.parse.quote((' '.join(query)).strip(' '))
        url = 'http://api.urbandictionary.com/v0/define?term=%s' % (query)
        query = urllib.parse.unquote(query)
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        size = len(data['list'])
        self.data_dict[query] = []

        for i in range(size):
            definition = str(data['list'][i]['definition'])
            example = data['list'][i]['example']
            if len(definition) < 1024 and len(example) < 1024:
                self.data_dict[query].append([definition, example])

        await self.display(["urban", query], ctx)

    async def display(self, message, ctx):
        query = message[1]
        try:
            definition = self.data_dict[query][0][0]
            example = self.data_dict[query][1][1]

            result_embed = discord.Embed(colour=discord.Colour.dark_red(), title=query)
            result_embed.add_field(name="Definition:", value=definition, inline=False)
            result_embed.add_field(name="Example:", value=example)
            result_embed.set_thumbnail(url="https://arablit.files.wordpress.com/2015/04/ud-logo.jpg")

            sent_message = await ctx.send(embed=result_embed)
            await sent_message.add_reaction('02spinleft:678613956327112704')
            await sent_message.add_reaction('02spinright:678613956025384972')
            self.valid_messages[sent_message.id] = [message[0], message[1], 0]
            await self.update_messages(sent_message.id)
        except IndexError:
            await ctx.send("The word `{0}` cannot be found in the dictionary!".format(query))

    async def scroll(self, message_increment, *ctx):
        # message = [api, query, index]
        message_id = message_increment[0]
        editing_msg = await ctx[0].fetch_message(message_id)
        api = self.valid_messages[message_id][0]
        query = self.valid_messages[message_id][1]
        index = self.valid_messages[message_id][2]
        increment = message_increment[1]

        if api == "urban":
            try:
                size = len(self.data_dict[query])
                index += increment
                if index >= size:
                    index = 0
                elif index < 0:
                    index = size - 1

                definition = self.data_dict[query][index][0]
                example = self.data_dict[query][index][1]

                result_embed = discord.Embed(colour=discord.Colour.dark_red(), title=query)
                result_embed.add_field(name="Definition:", value=definition, inline=False)
                result_embed.add_field(name="Example:", value=example)
                result_embed.set_thumbnail(url="https://arablit.files.wordpress.com/2015/04/ud-logo.jpg")

                try:
                    await editing_msg.edit(embed=result_embed)
                    self.valid_messages[message_id][2] = index
                except discord.errors.HTTPException:
                    index += increment
                    if index >= size:
                        index = 0
                    elif index < 0:
                        index = size - 1
            except IndexError:
                await ctx[0].send("The word `{0}` cannot be found in the dictionary!".format(query))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id in self.valid_messages and reaction.count > 1:
            if reaction.emoji.id == 678613956025384972:
                await self.scroll([reaction.message.id, 1], reaction.message.channel)
            elif reaction.emoji.id == 678613956327112704:
                await self.scroll([reaction.message.id, -1], reaction.message.channel)

    async def update_messages(self, message_id):
        await asyncio.sleep(300)
        del self.data_dict[self.valid_messages[message_id][1]]
        del self.valid_messages[message_id]


def setup(bot):
    bot.add_cog(UrbScraper(bot))
    print("Urban Cog added")
