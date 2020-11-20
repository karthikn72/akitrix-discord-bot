import json
import os
import threading
import time
import urllib.error
import urllib.request

import discord
import pymysql
from PIL import Image, ImageEnhance
from discord.ext import commands

import AkitrixDB
import Image_Edit

'''Unique token for bot to connect with Discord API'''

TOKEN = 'YOUR API KEY'


def get_prefix(bot, message):
    with open('prefix.json', 'r') as f:
        guild_dict = json.load(f)
    if str(message.guild.id) in guild_dict.keys():
        return guild_dict[str(message.guild.id)]
    else:
        return ';'


intents = discord.Intents(messages=True, guilds=True, members=True, presences=True)
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

'''Writes current time to a text file every 10 minutes to track last running timestamp of bot'''


def update_time():
    threading.Timer(600.0, update_time).start()
    with open('BotRuntime.txt', 'w') as f:
        f.write(str(time.asctime()) + '\n')


update_time()

permissionlist = ['administrator', 'ban_members', 'kick_members',
                  'manage_channels', 'manage_guild', 'manage_messages',
                  'add_reactions', 'read_messages',
                  'send_messages', 'send_tts_messages',
                  'embed_links', 'attach_files', 'read_message_history', 'mention_everyone', 'external_emojis',
                  'connect', 'speak', 'mute_members', 'deafen_members', 'move_members',
                  'change_nickname', 'manage_nicknames', 'manage_roles', 'manage_webhooks', 'manage_emojis',
                  'bot_owner']

'''Throughout the project, 'ctx' is a discord.Context object which consists details on the guild and channel where a
command was invoked, and also the user that invoked it.'''


@bot.command(name="akiset")
async def set_prefix(ctx, prefix):
    with open('prefix.json', 'r') as json_file:
        guild_dict = json.load(json_file)

    guild_dict[str(ctx.guild.id)] = prefix

    with open('prefix.json', 'w') as json_file:
        json.dump(guild_dict, json_file, indent=4)
    await ctx.send("The prefix is now set to ``{0}``".format(prefix))


'''Lists permissions of specified user in chat'''


@bot.command(name="perms")
async def list_perms(ctx, *member):
    if len(member) == 1:
        member = ctx.guild.get_member(int(''.join(d for d in member[0] if d.isdigit())))
    else:
        member = ctx.message.author
    memberperms = []
    if member.guild_permissions.administrator:
        await ctx.send('This user is an administrator!')
    else:
        for x in permissionlist:
            if x == "bot_owner" and member.id in [432126465254096896]:
                memberperms.append(x)
            elif x == "bot_owner":
                pass
            else:
                check = getattr(member.guild_permissions, x)
                if check:
                    memberperms.append(x)
        memberperms_str = '\n'.join(memberperms)
        embed = discord.Embed(color=discord.Colour.gold(), title="{0}'s roles".format(member.name),
                              description=memberperms_str)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)


@bot.command(name="perm_check")
async def perm_check(ctx, member, required_perms):
    missing_perms = []
    for i in required_perms:
        if i == "bot_owner" and (ctx.author.id not in [432126465254096896]):
            missing_perms.append(i)
        elif i == "bot_owner":
            pass
        else:
            check = getattr(member.guild_permissions, i)
            if not check:
                missing_perms.append(i)
    if len(missing_perms) != len(required_perms):
        return True
    else:
        await ctx.send(
            f"You are missing one or more of the following permissions: `{','.join(i for i in missing_perms)}`")
        return False


@bot.command(name="yeet")
async def yeet(ctx, *, message):
    message = message.lower()
    message2 = list(message)
    for i in range(1, len(message2), 2):
        message2[i] = message2[i].upper()
    await ctx.send(''.join(message2))


@bot.listen()
async def on_member_join(member):
    channel = member.guild.system_channel
    filename = str(member.id)
    filepath = 'assets/Avatars/' + filename

    if "gif" in str(member.avatar_url):
        filepath += ".gif"
    else:
        filepath += "-process.jpg"
    with open(os.path.join(filepath), "wb+") as f:
        await member.avatar_url.save(filepath)
        if filepath[-3:] == "gif":
            new_filepath = filepath[:-3] + "-process.jpg"
            Image.open(filepath).convert('RGB').save(new_filepath)
            filepath = new_filepath
    final_image = Image_Edit.welcome_image(filepath, member.id)
    await channel.send(content="Hello there, {0.mention}".format(member), file=discord.File(final_image))
    os.remove(final_image)
    datamod = AkitrixDB.Database()
    datamod.initialize(member.guild.id, member.guild.name)
    datamod.add_member(member.id, member.name, str(member.avatar_url), 0, 10000, 1, 100)
    timer = bot.get_command("reset-timer")
    await timer.__call__(channel, member.id)
    datamod.terminate()


@bot.listen()
async def on_member_remove(member):
    channel = member.guild.system_channel
    await channel.send("Goodbye {0}...we'll miss you!".format(member.name))
    datamod = AkitrixDB.Database()
    datamod.initialize(member.guild.id, member.guild.name)
    datamod.remove_member(member.id)
    datamod.terminate()


@bot.command(name="cr")
async def newroleyay(ctx, *, newrole):
    check = await perm_check(ctx, ctx.author, ["manage_roles"])
    if check:
        guild = ctx.guild
        await guild.create_role(name=newrole)
        await ctx.send("New Role Created: ```{0}```".format(newrole))


@bot.command(name="ar")
async def add_role(ctx, member, *role):
    check = await perm_check(ctx, ctx.author, ["manage_roles"])
    if check:
        role = discord.utils.get(ctx.guild.roles, name=' '.join(role))
        if role is None:
            await ctx.send("This role is not available")
        member = ctx.guild.get_member(int(''.join(d for d in member if d.isdigit())))
        await member.add_roles(role)
        await ctx.send("`{0}` added to {1.mention}".format(role.name, member))


@bot.command(name="rr")
async def remove_role(ctx, member, *role):
    check = await perm_check(ctx, ctx.author, ["manage_roles"])
    if check:
        role = discord.utils.get(ctx.guild.roles, name=' '.join(role))
        if role is None:
            await ctx.send("This role is not available")
        member = ctx.guild.get_member(int(''.join(d for d in member if d.isdigit())))
        await member.remove_roles(role)
        await ctx.send("`{0}` removed from {1.mention}".format(role.name, member))


@bot.command(name="dr")
async def byerole(ctx, *, oldrole):
    check = await perm_check(ctx, ctx.author, ["manage_roles"])
    if check:
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=oldrole)
        if role is None:
            role = guild.get_role(int(oldrole))
        await role.delete()
        await ctx.send("R.I.P This role got deleted: ```{0}```".format(oldrole))


@bot.command(name="mention")
async def mentiontime(ctx, *, person):
    guild = ctx.guild
    member = discord.utils.get(guild.members, name=person)
    if member is None:
        member = guild.get_role(int(person))
    await ctx.send("{0} wants you now, {1.mention}".format(ctx.message.author.mention, member))


@bot.command(name="enlarge", aliases=['emojibig', 'emoteyeet'])
async def emojibig(ctx, *, emote):
    emoji_converter = commands.PartialEmojiConverter()
    emoji = await emoji_converter.convert(ctx, emote)
    emotestring = str(emote)
    colon1 = emotestring.find(':')
    colon2 = emotestring.rfind(':')
    filename = emotestring[colon1 + 1:colon2]
    filepath = 'assets/Emotes/' + filename
    if emotestring[1] == "a":
        filepath += ".gif"
    else:
        filepath += ".jpg"
    with open(os.path.join(filepath), "wb+") as f:
        await emoji.url.save(filepath)
        await ctx.send(file=discord.File(filepath))
    os.remove(filepath)


@bot.command(name="avatar", aliases=["av"])
async def display_avatar(ctx, *member):
    if len(member) == 1:
        member = ctx.guild.get_member(int(''.join(d for d in member[0] if d.isdigit())))
    else:
        member = ctx.message.author
    filename = ''.join(i for i in member.name if i.isalnum())
    filepath = 'assets/Avatars/' + filename
    if "gif" in str(member.avatar_url):
        filepath += ".gif"
    else:
        filepath += ".jpg"
    with open(os.path.join(filepath), "wb+") as f:
        await member.avatar_url.save(filepath)
        await ctx.send(file=discord.File(filepath))
    os.remove(filepath)


@bot.command(name="deepfry")
async def deepfry(ctx, *avatar):
    factor = 10
    if len(avatar) == 0 or (avatar[0].isnumeric() and len(avatar[0]) <= 4):
        messages = await ctx.history(limit=20).flatten()
        message_index = -1
        is_embed = False
        for message in range(0, len(messages)):
            if (len(messages[message].embeds) >= 1 and not isinstance(messages[message].embeds[0].image,
                                                                      type(discord.Embed.Empty))):
                is_embed = True
                message_index = message
                break
            elif len(messages[message].attachments) >= 1:
                message_index = message
                break
        if is_embed:
            image_url = messages[message_index].embeds[0].image.url
        else:
            image_url = messages[message_index].attachments[0].url
        dot = image_url.rfind('.')
        image_url2 = 'assets/DeepFry/' + str(ctx.author.id)
        if image_url[dot + 1:] == "gif":
            ext = ".gif"
        elif image_url[dot + 1:] == "png":
            ext = "-original.png"
        else:
            ext = "-original.jpg"
        image_url2 += ext
        if not is_embed:
            await messages[message_index].attachments[0].save(image_url2)
        else:
            urllib.request.urlretrieve(image_url, image_url2)
        if len(avatar) != 0 and avatar[0].isnumeric():
            factor = int(avatar[0])
    else:
        if avatar[0].isnumeric() and len(avatar[0]) > 4:
            member = ctx.guild.get_member(avatar[0])
        else:
            member = ctx.guild.get_member(int(''.join(d for d in avatar[0] if d.isdigit())))
        if avatar[-1].isnumeric() and len(avatar[-1]) <= 4:
            factor = int(avatar[-1])
        image_url = member.avatar_url
        image_url2 = 'assets/DeepFry/' + str(ctx.author.id)

        if "gif" in str(image_url):
            ext = ".gif"
        else:
            ext = "-original.jpg"
        image_url2 += ext
        with open(image_url2, "wb+") as f:
            await member.avatar_url.save(image_url2)
    if image_url2[-3:] == "gif":
        temp_image = image_url2[:-3] + "-original.jpg"
        Image.open(image_url2).convert('RGB').save(temp_image)
        image_url2 = temp_image
    img = Image.open(image_url2)
    converter = ImageEnhance.Color(img)
    img2 = converter.enhance(factor)
    img2.convert("RGB").save(image_url2)
    await ctx.send(file=discord.File(image_url2))
    os.remove(image_url2)

@bot.command(name="roles")
async def listroles(ctx):
    guild = ctx.guild
    list_roles = []
    for role in guild.roles:
        if len(role.members) == 0 or not role.members[0].bot:
            list_roles.append(str(role))
    list_roles_str = ', '.join(list_roles)
    embed = discord.Embed(color=discord.Colour.gold(), title="Roles in: `{0}`".format(guild.name),
                          description=f"```{list_roles_str}```")
    embed.set_thumbnail(url=guild.icon_url)
    await ctx.send(embed=embed)


@bot.command(name="report")
async def report(ctx, *report):
    i = await bot.application_info()
    owner = i.owner
    await owner.send(
        "**Server:** {0}\n**User:** {1}\n**Report:** {2}".format(ctx.guild.name, ctx.author.name, ' '.join(report)))


@bot.command(name="fulldb")
async def add_db(ctx):
    check = await perm_check(ctx, ctx.author, ["bot_owner"])
    if check:
        try:
            members = ctx.guild.members
            datamod = AkitrixDB.Database()
            datamod.initialize(ctx.guild.id, ctx.guild.name)
            inmembers = []
            for i in range(len(members)):
                member = members[i]
                added = datamod.add_member(member.id, member.name, str(member.avatar_url), 0, 10000, 1, 100)
                if added:
                    inmembers.append(member)
            datamod.terminate()
            await ctx.send("The members are added to the database!")
            if len(inmembers) != 0:
                await ctx.send("Some new members have been added! Would you like to view them...?")

                def check(message):
                    return message.author == ctx.author

                response = await bot.wait_for('message', check=check)
                if response.content == "y":
                    embed = discord.Embed(color=discord.Colour.dark_blue(), title="Newly added members:")
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.add_field(name="Members", value=str([i.mention for i in inmembers]), inline=False)
                    await ctx.send(embed=embed)
        except pymysql.err.OperationalError:
            await ctx.send("The server is having issues...")


@bot.command(name="setcred")
async def set_credits(ctx, *people):
    check = await perm_check(ctx, ctx.author, ["administrator", "bot_owner"])
    if check:
        if people[0] == "all":
            members = [i for i in ctx.guild.members]
        elif people[0] == "allindb":
            members = "all"
        else:
            members = [ctx.guild.get_member(int(''.join(d for d in people[0] if d.isdigit())))]
        amount = 1000
        if people[-1].isdigit():
            amount = int(people[-1])
        datamod = AkitrixDB.Database()
        datamod.initialize(0, 'Main')
        if members != "all":
            for member in members:
                datamod.reset_credits(member.id, amount)

        else:
            datamod.reset_all_credits(amount)
        datamod.terminate()
        if len(members) > 1:
            await ctx.send("Everyone's credits has been set to {0}".format(amount))
        else:
            await ctx.send("{0}'s credits has been set to {1}".format(members[0].name, amount))


@bot.command(name="resetxp")
async def resetxp(ctx, *people):
    check = await perm_check(ctx, ctx.author, ["administrator"])
    if check:
        if people[0] == "all":
            members = [i for i in ctx.guild.members]
        else:
            members = [ctx.guild.get_member(int(''.join(d for d in people[0] if d.isdigit())))]
        datamod = AkitrixDB.Database()
        datamod.initialize(0, 'Main')
        for member in members:
            datamod.reset_xp(member.id)
        datamod.terminate()
        if len(members) > 1:
            await ctx.send("Everyone's XP has been reset")
        else:
            await ctx.send("{0}'s XP has been reset".format(members[0].name))


# @bot.event
# async def on_message(message):
#     await bot.process_commands(message)
#     # xp_gain = len(message.content) // (random.randint(3, 7))
#     if len(message.embeds)!=0:
#         for embed in message.embeds:
#             print(embed.to_dict())
#     datamod = AkitrixDB.Database()
#     datamod.initialize('Main')
#     datamod.update_xp(message.author.id, xp_gain)


@bot.event
async def on_user_update(before, after):
    datamod = AkitrixDB.Database()
    datamod.initialize(0, 'Main')
    if before.avatar != after.avatar:
        datamod.update_pfp(after.id, after.avatar_url)
    if before.name != after.name:
        datamod.update_name(after.id, after.name)
    datamod.terminate()


@bot.event
async def on_guild_update(before, after):
    if before.name != after.name:
        datamod = AkitrixDB.Database()
        datamod.initialize(before.id, after.name)
        datamod.terminate()


@bot.command(name="profile")
async def profile(ctx, *member):
    try:
        if len(member) == 0:
            member_id = ctx.message.author.id
        elif isinstance(member[0], int):
            member_id = member[0]
        elif not member[0].isdigit():
            member_id = ctx.guild.get_member(int(''.join(d for d in member[0] if d.isdigit()))).id
        else:
            member_id = member[0]
        datamod = AkitrixDB.Database()
        datamod.initialize(ctx.guild.id, ctx.guild.name)
        facts = datamod.fetch_profile(member_id)
        datamod.terminate()
        name, avatar, isbot, creds, level, XP = facts[1], facts[2], facts[3], facts[4], facts[5], facts[6]
        embed = discord.Embed(color=discord.Colour.dark_blue(), title="{0}'s profile".format(name))
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="User ID:", value=member_id, inline=False)
        embed.add_field(name="Level:", value=level)
        embed.add_field(name="XP:", value=XP)
        embed.add_field(name="Credits:", value=creds)
        await ctx.send(embed=embed)
    except pymysql.err.OperationalError:
        await ctx.send("The server is having issues....")


@bot.command(name="gprofile")
async def game_profile(ctx, *member):
    if len(member) == 0:
        member_id = ctx.message.author.id
    elif isinstance(member[0], int):
        member_id = member[0]
    elif not member[0].isdigit():
        member_id = ctx.guild.get_member(int(''.join(d for d in member[0] if d.isdigit()))).id
    else:
        member_id = member[0]
    datamod = AkitrixDB.Database()
    datamod.initialize(ctx.guild.id, ctx.guild.name)
    facts = datamod.fetch_gameprofile(member_id)
    datamod.terminate()
    [potion, armor, weapon, name, avatar, weapon_level, armor_level] = facts
    embed = discord.Embed(color=discord.Colour.dark_blue(), title="{0}'s Player profile".format(name))
    embed.set_thumbnail(url=avatar)
    embed.add_field(name="Weapon:", value=weapon, inline=False)
    embed.add_field(name="Weapon Level:", value=weapon_level)
    if armor == "None":
        embed.add_field(name="Armor:", value="You don't have an armor yet!")
    else:
        embed.add_field(name="Armor:", value=armor)
        embed.add_field(name="Armor Level:", value=armor_level)
    if potion == "None":
        embed.add_field(name="Potion:", value="You don't have a potion yet!")
    else:
        embed.add_field(name="Potion:", value=potion)
    await ctx.send(embed=embed)


@bot.command(name="allprofile")
async def all_profile(ctx, *member):
    check = await perm_check(ctx, ctx.author, ["bot_owner"])
    if check:
        for member in ctx.guild.members:
            await profile(ctx, member.id)


@bot.command(name="play")
async def load_game(ctx):
    bot.load_extension('cogs.DiscordGame')
    await ctx.send("Game Cog Loaded!")


# except commands.ExtensionFailed:
#     # print(f'Failed to load extension {name}.', file=sys.stderr)
#     traceback.print_exc()
# for file in os.listdir("cogs"):
#     if file.endswith(".py"):
#         name = file[:-3]
#         try:
#             bot.load_extension(f"cogs.{name}")
#         except commands.ExtensionFailed:
#             # print(f'Failed to load extension {name}.', file=sys.stderr)
#             traceback.# print_exc()

@bot.command(name="spam")
async def spam(ctx, *text):
    text = list(text)
    try:
        repeat = int(text[-1])
        text = text[:-1]
    except ValueError:
        repeat = 10
    for i in range(repeat):
        await ctx.send(' '.join(text))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        wrong_com = str(error)[str(error).find('"') + 1:str(error).rfind('"')]
        await ctx.send("`{0}` is not a valid command!".format(wrong_com))
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("Incorrect syntax, `{0}`! Please try again!".format(ctx.author.name))
    else:
        print(type(error))
        print(error)
        await ctx.send(f"```{error}```")


@bot.event
async def on_ready():
    bot.load_extension('cogs.UrbanDictionary.urban_dict')
    bot.load_extension('cogs.GoogleImageSearch.GoogleImages')
    bot.load_extension('cogs.AdventureGame.DiscordGame')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)

