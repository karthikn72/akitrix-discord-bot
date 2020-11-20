import os
import urllib.error
import urllib.request

import discord
from discord.ext import commands
from googleapiclient.discovery import build


def remove_forbidden(file_name):
    forbidden_chars = '<>:"?/\\?*'
    for char in forbidden_chars:
        file_name = file_name.replace(char, "-")
    return file_name


class GooScraper(commands.Cog, name="GoogleScraper"):
    def __init__(self, bot):
        self.bot = bot
        self.valid_messages = {}  # {message:[urban/google, total num of items,index]}

    @commands.command(name="google")
    async def load_images(self, ctx, *query):
        api_key = "YOUR GOOGLE API KEY"
        search_engine_id = "YOUR GOOGLE CUSTOM SEARCH ENGINE ID"
        resource = build("customsearch", 'v1', developerKey=api_key).cse()

        query = (' '.join(query)).strip(' ')

        imagedesc = []
        imagelink = []

        result = resource.list(q=query, cx=search_engine_id, searchType='image').execute()

        filename = remove_forbidden(query + str(ctx.author.id) + ".txt")
        imagename = remove_forbidden(query + str(ctx.author.id) + ".jpg")

        filename = 'cogs/GoogleImageSearch/results/' + filename
        imagename = 'cogs/GoogleImageSearch/results/' + imagename

        try:
            for item in result['items']:
                imagedesc.append(item['title'])
                imagelink.append(item['link'])

            with open(filename, "w+") as f:
                for link in range(len(imagelink)):
                    image_url = imagelink[link]
                    f.write("{0}\n".format(image_url))

            with open(filename, "r") as f:
                result_embed = discord.Embed(colour=discord.Colour.dark_red(),
                                             title="{0}'s image result for: `{1}`".format(ctx.author.name, query))
                image_url = f.readline()
                try:
                    urllib.request.urlretrieve(image_url, imagename)
                    result_embed.set_image(url=image_url)
                except urllib.error.HTTPError:
                    result_embed.add_field(name="Error:", value="The image cannot be loaded please try again later!")
                message = await ctx.send(embed=result_embed)
        except KeyError:
            result_embed = discord.Embed(colour=discord.Colour.dark_red(),
                                         title="{0}'s image result for: `{1}`".format(ctx.author.name, query))
            result_embed.add_field(name="Error:", value="The image cannot be found!")
            message = await ctx.send(embed=result_embed)
        try:
            os.remove(filename)
            os.remove(imagename)
        except FileNotFoundError:
            pass


def setup(bot):
    bot.add_cog(GooScraper(bot))
    print("Google Cog added")
