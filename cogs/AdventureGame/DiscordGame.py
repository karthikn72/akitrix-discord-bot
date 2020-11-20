import asyncio
import datetime
import random
import time

import discord
import pymysql
from discord.ext import commands

import AkitrixDB


class EndGame(Exception):
    pass


class Player:

    def __init__(self, user_id):
        datamod = AkitrixDB.Database()
        datamod.initialize(0, 'Main')
        facts = datamod.fetch_gameprofile(user_id)

        self.valid_messages = []

        self.low_multiplier = 1.07
        self.high_multiplier = 1.1
        [self.potion, self.armor, self.weapon, self.name, self.avatar, self.weapon_level, self.armor_level] = facts
        facts2 = datamod.fetch_profile(user_id)
        self.gold, self.level, self.XP = facts2[4], facts2[5], facts2[6]
        self.potion_hp = 0
        self.potion_damage = 0

        self.health = int(1000 * (self.low_multiplier ** self.level))

        datamod.execute(
            "SELECT `Damage ({0})` FROM `Weapons` WHERE `Weapons`.`Name` = '{1}'".format(self.weapon_level,
                                                                                         self.weapon))
        base_dmg = datamod.cur.fetchone()
        self.WeaponDmg = base_dmg[0]

        self.dead = False
        datamod.terminate()


class Player_Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def initialize(self, ctx, user):
        try:

            player_hash = ''.join([chr(97 + int(i)) for i in str(user.id)])
            self.players[user.id] = Player(user.id)
            self.players[user.id].name = user.name

        except pymysql.err.OperationalError:
            await ctx.send(
                "Due to technical difficulties the game has aborted! Your timer shall now be reset, and you will be able to restart the game!")
            await ctx.send("Apologies for the inconvenience....")
            await self.timer_reset(ctx, ctx.author.id)
            return

    async def game_profile(self, ctx):
        embed = discord.Embed(color=discord.Colour.blue(),
                              title="`{0}`'s profile".format(self.players[ctx.author.id].name))
        embed.set_thumbnail(url=self.players[ctx.author.id].avatar)
        embed.add_field(name="Gold:", value=self.players[ctx.author.id].gold)
        embed.add_field(name="Armor:", value=self.players[ctx.author.id].armor)
        embed.add_field(name="Armor Level:", value=self.players[ctx.author.id].armor_level)
        embed.add_field(name="Health:", value=self.players[ctx.author.id].health)
        # embed.add_field(name="Morale: `{0}`",value=self.players[ctx.author.id].morale))
        embed.add_field(name="Weapon:", value=self.players[ctx.author.id].weapon)
        embed.add_field(name="Weapon Level:", value=self.players[ctx.author.id].weapon_level)
        embed.add_field(name="Weapon Damage:", value=self.players[ctx.author.id].WeaponDmg)
        embed.add_field(name="Level:", value=self.players[ctx.author.id].level)
        embed.add_field(name="Potion:", value=self.players[ctx.author.id].potion)
        embed.set_footer(text='Type "quit" to exit the game at any prompt')
        await ctx.send(embed=embed)

    async def user_in(self, ctx, input_msg, valid_inputs):
        try:
            await ctx.send(input_msg)

            def check(message):
                return message.author == ctx.author

            valid_inputs.append("quit")
            out_msg = await self.bot.wait_for('message', check=check, timeout=90.0)
            while out_msg.content.lower() not in valid_inputs:
                await ctx.send(input_msg)
                out_msg = await self.bot.wait_for('message', check=check, timeout=90.0)
            if out_msg.content.lower() == "quit":
                raise EndGame
            return out_msg.content.lower()
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond!")
            raise EndGame

    async def check_player(self, ctx):
        try:
            datamod = AkitrixDB.Database()
            datamod.initialize(ctx.guild.id, ctx.guild.name)
            SQL = "SELECT `Time` FROM `UserItems` WHERE `UID`={0}".format(ctx.author.id)
            datamod.execute(SQL)
            time_stamp = datamod.cur.fetchone()[0]
            datamod.terminate()
            epoch_seconds = time_stamp.timestamp()
            current_time = datetime.datetime.now().timestamp()
            time_diff = current_time - epoch_seconds
            return time_diff >= 14400, time_diff
        except pymysql.err.OperationalError:
            await self.timer_reset(ctx, ctx.author.id)
            return

    @commands.command(name="reset-timer")
    async def timer_reset(self, ctx, *member):
        check = True
        if check:
            if len(member) == 0:
                member_id = ctx.message.author.id
            elif isinstance(member[0], int):
                member_id = member[0]
            elif not member[0].isdigit():
                member_id = ctx.guild.get_member(int(''.join(d for d in member[0] if d.isdigit()))).id
            else:
                member_id = member[0]
            try:
                current_time = datetime.datetime.now().timestamp()
                change_time = datetime.timedelta(seconds=14400)
                new_time = datetime.datetime.now() - datetime.timedelta(seconds=14400)
                update_time = datetime.datetime.fromtimestamp(new_time.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
                datamod = AkitrixDB.Database()
                datamod.initialize(ctx.guild.id, ctx.guild.name)
                SQL = "UPDATE `UserItems` SET `Time`='{0}' WHERE `UID`={1}".format(update_time, member_id)
                datamod.execute(SQL)
                datamod.terminate()
                await ctx.send(f"{ctx.guild.get_member(member_id).name}'s timer has now been reset!")
            except pymysql.err.OperationalError:
                await ctx.send(
                    "Due to technical difficulties the game has aborted! Your timer shall now be reset, and you will be able to restart the game!")
                await ctx.send("Apologies for the inconvenience....")
                # await self.timer_reset(ctx, member_id)
                return

    async def play_game(self, ctx):
        playable, time_diff = await self.check_player(ctx)
        if playable:
            await self.initialize(ctx, ctx.author)
            await self.game_profile(ctx)
            try:

                confirm = await self.user_in(ctx,
                                             "You currently have `{0}` XP, this will be your levelling system, do you understand? `Y/N` ".format(
                                                 self.players[ctx.author.id].XP),
                                             ["yes", "yeah", "y", "no", "nah", "n"])
                if confirm in ["yes", "yeah", "y"]:
                    await ctx.send("You may continue with your adventure!")
                else:
                    await ctx.send("We're going to continue anyway")
                await ctx.send("While walking through the woods something jumps out of the bushes!")
                name, monster_xp, monster_health = await self.monster_spawn(ctx, [0.5 ** i for i in range(3)])
                await self.choice(ctx, name, monster_xp, monster_health)
                await self.game_profile(ctx)
                await ctx.send("You notice there is a village up ahead...")
                village = await self.user_in(ctx, "Do you want to go to the village? `Y/N`",
                                             ["yes", "yeah", "y", "no", "nah", "n"])
                if village in ["yes", "yeah", "y"]:
                    shop = "y"
                    shops = [1, 2, 3]
                    self.players[ctx.author.id].shops_visited = [0] * len(shops)
                    while shop in ["yes", "yeah", "y"]:
                        shoptype = await self.user_in(ctx,
                                                      "Would you like to go to:\n`1`) Potion Store\n`2`) Blacksmiths (Armory)\n`3`) Forge (Weaponry)\n`4`) Exit\n",
                                                      [str(i + 1) for i in range(len(shops) + 1)])
                        if shoptype == "4":
                            break
                        elif self.players[ctx.author.id].shops_visited[int(shoptype) - 1] != 1:
                            await self.open_shop(shoptype, ctx)
                            self.players[ctx.author.id].shops_visited[int(shoptype) - 1] = 1
                            await self.game_profile(ctx)
                        else:
                            await ctx.send("This shop has already been visited!")
                        shop = await self.user_in(ctx, "Do you want to go to another store? `Y/N`",
                                                  ["yes", "yeah", "y", "no", "nah", "n"])
                await ctx.send("You decide to continue traveling through the woods")
                await ctx.send("While in the woods you begin to here a rustling noise")
                monster_chance = random.randint(1, 100)
                if monster_chance >= 2:
                    name, monster_xp, monster_health = await self.monster_spawn(ctx, [i for i in range(1, 11)])
                    await self.choice(ctx, name, monster_xp, monster_health)
                    await self.game_profile(ctx)
                else:
                    await ctx.send("You check the bush and find a magic pile of money along with a silver key")
                    gold_gain = 10 * random.randint(5, 50)
                    self.players[ctx.author.id].gold += gold_gain
                    await ctx.send(
                        "You found `{0}` gold inside the bag, you now have `{1}` pieces".format(gold_gain, self.players[
                            ctx.author.id].gold))
                await ctx.send("What's this? You notice a small cave nearby!")
                cave = await self.user_in(ctx, "Do you want to enter the cave? `Y/N`",
                                          ["yes", "yeah", "y", "no", "nah", "n"])
                if cave in ["yes", "yeah", "y"]:
                    await ctx.send("You enter the cave")
                    await ctx.send("Out pops another monster!")
                    name, monster_xp, monster_health = await self.monster_spawn(ctx, [i for i in range(11, 21)])
                    choice = await self.user_in(ctx, "Do you want to `fight` or `run`?", ["run", "fight"])
                    if choice == "run":
                        await self.escape(ctx)
                        await ctx.send("You ran away from the `{0}` and escaped the cave!".format(name))
                        await ctx.send("You continue to follow the trail")
                    elif choice == "fight":
                        await self.fight(ctx, name, monster_xp, monster_health)
                        await ctx.send(
                            "After defeating the `{0}` you search the cave and find some treasure!".format(name))
                        gold_gain = 10 * random.randint(10, 45)
                        self.players[ctx.author.id].gold += gold_gain
                        await ctx.send("You found `{0}` gold!".format(gold_gain))
                        await ctx.send("You exit the cave and continue on the trail")
                    await self.game_profile(ctx)
                else:
                    await ctx.send("You continue on the trail and ignore the cave!")
                await ctx.send(
                    "While following the trail you find two routes to take, one up a dangerous cliff, and the other is a more safe path")
                cliffpath = await self.user_in(ctx, "Which one would you like to take? `Cliff` or `Path`",
                                               ["cliff", "path"])
                if cliffpath == "path":
                    monster_chance = random.randint(1, 100)
                    if monster_chance >= 45:
                        await ctx.send(
                            "You choose to go the safe route, but while following the path...")
                        name, monster_xp, monster_health = await self.monster_spawn(ctx, [i for i in range(17, 23)])
                        await self.choice(ctx, name, monster_xp, monster_health)
                elif cliffpath == "cliff":
                    climb = random.randint(1, 10)
                    while climb <= 5:
                        await ctx.send("You attempted to climb the cliff but fell!")
                        climb += 1
                        healthloss = int(((random.randint(1, 5)) / 100) * self.players[ctx.author.id].health)
                        self.players[ctx.author.id].health -= healthloss
                        await ctx.send("You lost `{0}` health from the fall!".format(healthloss))

                        if self.players[ctx.author.id].health <= 0:
                            self.players[ctx.author.id].health = 0
                            self.players[ctx.author.id].dead = True
                            await ctx.send("Wow you died from the fall...")
                            raise EndGame
                    await self.game_profile(ctx)
                    await ctx.send("You successfully climbed the cliff!")
                    await ctx.send(
                        "When you reach the top of the cliff you see a small village (this will be your last time to shop)")
                    village = await self.user_in(ctx, "Do you want to go to the village? `Y/N`",
                                                 ["yes", "yeah", "y", "no", "nah", "n"])
                    if village in ["yes", "yeah", "y"]:
                        shop = "y"
                        shops = [1, 2, 3]
                        self.players[ctx.author.id].shops_visited = [0] * len(shops)
                        while shop in ["yes", "yeah", "y"]:
                            shoptype = await self.user_in(ctx,
                                                          "Would you like to go to:\n`1`) Potion Store\n`2`) Blacksmiths (Armory)\n`3`) Forge (Weaponry)\n`4`) Exit\n",
                                                          [str(i + 1) for i in range(len(shops) + 1)])
                            if shoptype == "4":
                                break
                            elif self.players[ctx.author.id].shops_visited[int(shoptype) - 1] != 1:
                                await self.open_shop(shoptype, ctx)
                                self.players[ctx.author.id].shops_visited[int(shoptype) - 1] = 1
                                await self.game_profile(ctx)
                            else:
                                await ctx.send("This shop has already been visited!")
                            shop = await self.user_in(ctx, "Do you want to go to another store? `Y/N`",
                                                      ["yes", "yeah", "y", "no", "nah", "n"])
                    else:
                        await ctx.send("You decide not to go into the village and continue following the path")
                await ctx.send("A dark shadow looms over you...")
                await ctx.send("You walk over to approach it...")
                await ctx.send("IT'S THE FINAL BOSS!")
                name, monster_xp, monster_health = await self.monster_spawn(ctx, [22, 23, 24, 25, 30])
                await self.choice(ctx, name, monster_xp, monster_health)
                await ctx.send("You continue to follow the path and finally reach the top of the mountain")
                raise EndGame
            except EndGame:
                await ctx.send("The game has ended")
                await ctx.send("Here are your final stats:")
                if self.players[ctx.author.id].health < 0:
                    self.players[ctx.author.id].health = 0
                await self.game_profile(ctx)
                datamod = AkitrixDB.Database()
                datamod.initialize(ctx.guild.id, ctx.guild.name)
                SQL = "UPDATE `UserItems` SET `WID`=(SELECT `WID` FROM `Weapons` WHERE `Name`='{0}')," \
                      "`Weapon Level`='{1}'," \
                      "`PID`=(SELECT `IID` FROM `Items` WHERE `Item Name` = '{2}')," \
                      "`AID`=(SELECT `IID` FROM `Items` WHERE `Item Name` = '{3}')," \
                      "`Armor Level` = {4}," \
                      "`Time` = CURRENT_TIMESTAMP WHERE `UID`={5}".format(self.players[ctx.author.id].weapon,
                                                                          self.players[ctx.author.id].weapon_level,
                                                                          self.players[ctx.author.id].potion,
                                                                          self.players[ctx.author.id].armor,
                                                                          self.players[ctx.author.id].armor_level,
                                                                          ctx.author.id)
                datamod.execute(SQL)
                SQL = "UPDATE `Main` SET `Credits`={0},`Level`={1},`XP`={2} WHERE `UID` = {3}".format(
                    self.players[ctx.author.id].gold,
                    self.players[ctx.author.id].level,
                    self.players[ctx.author.id].XP,
                    ctx.author.id)
                datamod.execute(SQL)
                datamod.terminate()
                del self.players[ctx.author.id]
                return
        else:
            remaining = str(datetime.timedelta(seconds=(14400 - time_diff))).split(":")
            await ctx.send("You have `{0} hours and {1} minutes to play`!".format(remaining[0], remaining[1]))

    async def monster_spawn(self, ctx, levels):
        monster_level = random.choice(levels)
        datamod = AkitrixDB.Database()
        datamod.initialize(ctx.guild.id, ctx.guild.name)
        SQL = "SELECT `Size`,`Name`,`XP` FROM `Monsters` WHERE `Challenge`={0} ORDER BY RAND() LIMIT 1".format(
            monster_level)
        datamod.execute(SQL)
        (size, name, monster_xp) = datamod.cur.fetchone()
        datamod.terminate()
        monster_xp *= int(self.players[ctx.author.id].high_multiplier ** self.players[ctx.author.id].level)
        monster_health = int(1.5 * monster_xp)
        name = size + " " + name
        embed = discord.Embed(color=discord.Colour.dark_red(), title="Oh no! A monster has appeared!",
                              description="Monster Stats:")
        embed.set_thumbnail(url=self.players[ctx.author.id].avatar)
        embed.add_field(name="Name:", value=name)
        embed.add_field(name="Health:", value=str(monster_health))
        await ctx.send(embed=embed)
        return name, monster_xp, monster_health

    async def choice(self, ctx, name, monster_xp, monster_health):
        choice = await self.user_in(ctx, "Do you want to `fight` or `run`?", ["run", "fight"])
        if choice == "run":
            await self.escape(ctx)
        elif choice == "fight":
            await self.fight(ctx, name, monster_xp, monster_health)

    async def open_shop(self, shoptype, ctx):
        datamod = AkitrixDB.Database()
        datamod.initialize(0, 'Main')
        colours = ["White", "Yellow", "Red", "Blue", "Green", "Teal", "Turquoise", "Cyan"]
        if shoptype == "1":
            SQL = "SELECT `Item Name`,`Cost`,`HP`,`Damage` FROM `Items` WHERE `Item Name` LIKE 'Potion of %'"
            datamod.execute(SQL)
            await ctx.send(
                "You walk into the potion shop and notice there's a few items that catch your interest")
            description = ""
            counter = 0
            potions = datamod.cur.fetchall()
            for name, cost, hp, damage in potions:
                counter += 1
                hp *= int(self.players[ctx.author.id].low_multiplier ** self.players[ctx.author.id].level)
                damage *= int(self.players[ctx.author.id].low_multiplier ** self.players[ctx.author.id].level)
                cost *= int(self.players[ctx.author.id].low_multiplier ** self.players[ctx.author.id].level)
                description += "{0}) **{1}** | Cost: `{2}` | Health: `{3}` HP | Damage: `{4}`\n".format(counter, name,
                                                                                                        cost, hp,
                                                                                                        damage)
            embed = discord.Embed(colour=discord.Colour.blue(), title="Welcome to Granny Luna's Brewery!",
                                  description=description)
            await ctx.send(embed=embed)
            buy = await self.user_in(ctx, "Would you like to buy one? `Y/N`", ["yes", "yeah", "y", "no", "nah", "n"])
            if buy in ["yes", "yeah", "y"]:
                potion = await self.user_in(ctx, "Which potion would you like? Enter the number:",
                                            [str(i) for i in range(1, len(potions) + 1)])
                name, cost, hp, damage = potions[int(potion) - 1]
                hp *= int(self.players[ctx.author.id].low_multiplier ** self.players[ctx.author.id].level)
                damage *= int(self.players[ctx.author.id].low_multiplier ** self.players[ctx.author.id].level)
                cost *= int(self.players[ctx.author.id].low_multiplier ** self.players[ctx.author.id].level)
                await ctx.send(
                    "You walk up to the shop owner and point at the small `{0}` flask".format(random.choice(colours)))
                await ctx.send("The shop owner gives a disgruntled look and tries to take `{0}` gold".format(cost))
                if self.players[ctx.author.id].gold >= cost:
                    self.players[ctx.author.id].gold -= cost
                    if self.players[ctx.author.id].gold <= 0:
                        self.players[ctx.author.id].gold = 0
                    await ctx.send(
                        " The shop keeper takes `{0}` gold from you and hands you the potion".format(cost))
                    await ctx.send("You now have `{0}` gold pieces".format(self.players[ctx.author.id].gold))
                    self.players[ctx.author.id].potion = name
                    self.players[ctx.author.id].potion_hp = hp
                    self.players[ctx.author.id].potion_damage = damage
                    await ctx.send("You now have a `{0}` potion".format(self.players[ctx.author.id].potion))
                    await ctx.send("Be careful you can only have one potion at a time")
                    await ctx.send("You exit the shop")
                else:
                    await ctx.send(
                        "You only have `{0}` gold! The owner is mad and kicks you out of the store!".format(
                            self.players[ctx.author.id].gold))
            else:
                await ctx.send("The shop owner doesn't understand you and points you towards the exit")
        elif shoptype == "2":
            SQL = "SELECT `Item Name`,`Cost`,`HP` FROM `Items` WHERE `Item Name` LIKE '% Armor'"
            datamod.execute(SQL)
            await ctx.send(
                "You walk into the armory and notice there's a few items that catch your interest")
            description = ""
            counter = 0
            armors = datamod.cur.fetchall()
            for name, cost, hp in armors:
                counter += 1
                hp *= int(self.players[ctx.author.id].low_multiplier ** (self.players[ctx.author.id].armor_level + 1))
                cost *= int(self.players[ctx.author.id].low_multiplier ** (self.players[ctx.author.id].armor_level + 1))
                description += "`{0}`) **{1}** | Cost: `{2}` | Health: `{3}` HP\n".format(counter, name, cost, hp)
            embed = discord.Embed(colour=discord.Colour.blue(), title="Welcome to Blackmet's Armory!",
                                  description=description)
            await ctx.send(embed=embed)
            buy = await self.user_in(ctx, "Would you like to buy one? `Y/N`", ["yes", "yeah", "y", "no", "nah", "n"])
            if buy in ["yes", "yeah", "y"]:
                armor = await self.user_in(ctx, "Which armor would you like? Enter the number:",
                                           [str(i) for i in range(1, len(armors) + 1)])
                name, cost, hp = armors[int(armor) - 1]
                hp *= int(self.players[ctx.author.id].low_multiplier ** (self.players[ctx.author.id].armor_level + 1))
                cost *= int(self.players[ctx.author.id].low_multiplier ** (self.players[ctx.author.id].armor_level + 1))
                await ctx.send("You walk up to the shop owner and point at the `{0}`".format(name))
                await ctx.send("The shop owner gives a disgruntled look and tries to take `{0}` gold".format(cost))
                if self.players[ctx.author.id].gold >= cost:
                    self.players[ctx.author.id].gold -= cost
                    if self.players[ctx.author.id].gold <= 0:
                        self.players[ctx.author.id].gold = 0
                    await ctx.send(
                        " The shop keeper takes `{0}` gold from you and fits the armor on you".format(cost))
                    await ctx.send("You now have `{0}` gold pieces".format(self.players[ctx.author.id].gold))
                    if name == self.players[ctx.author.id].armor:
                        self.players[ctx.author.id].armor_level += 1
                    else:
                        self.players[ctx.author.id].armor_level = 1
                        self.players[ctx.author.id].armor = name
                    self.players[ctx.author.id].health += hp
                    await ctx.send("You now have a `{0}`".format(self.players[ctx.author.id].armor))
                    await ctx.send("You exit the shop")
                else:
                    await ctx.send(
                        "You only have `{0}` gold! The owner is mad and kicks you out of the store!".format(
                            self.players[ctx.author.id].gold))
            else:
                await ctx.send("The shop owner doesn't understand you and points you towards the exit")
        elif shoptype == "3":
            SQL = "SELECT `Name`,`Cost`,`Damage (S)` FROM `Weapons`"
            datamod.execute(SQL)
            await ctx.send(
                "You walk into the armory and notice there's a few items that catch your interest")
            description = ""
            counter = 0
            weapons = list(datamod.cur.fetchall())

            def check(reaction, user):
                return reaction.emoji.id in [678613956025384972, 678613956327112704, 680474277195153484]

            descriptions = []

            for name, cost, damage in weapons:
                weapons[counter] = [name, cost, damage]
                counter += 1
                current_len = len(description)
                level = "Small"
                if name == self.players[ctx.author.id].weapon and self.players[ctx.author.id].weapon_level == "M":
                    description += "`{0}`) **{1}** | Already Owned\n".format(counter, name)
                elif name == self.players[ctx.author.id].weapon and self.players[ctx.author.id].weapon_level == "S":
                    SQL = "SELECT `Damage (M)` FROM `Weapons` WHERE `Name` = '{0}'".format(name)
                    datamod.execute(SQL)
                    damage = datamod.cur.fetchone()[0]
                    weapons[counter - 1][2] = damage
                    level = "Medium"
                    cost *= 2
                    weapons[counter - 1][1] = cost
                    description += "`{0}`) **{1}** | Level: `{2}` | Cost: `{3}` | Damage: `{4}`\n".format(counter,
                                                                                                          name,
                                                                                                          level, cost,
                                                                                                          damage)
                else:
                    description += "`{0}`) **{1}** | Level: `{2}` | Cost: `{3}` | Damage: `{4}`\n".format(counter,
                                                                                                          name,
                                                                                                          level, cost,
                                                                                                          damage)
                new_len = len(description)
                if new_len >= 2048:
                    descriptions.append(description[:current_len])
                    description = ""
                    if name == self.players[ctx.author.id].weapon and self.players[ctx.author.id].weapon_level == "M":
                        description += "`{0}`) **{1}** | Already Owned\n".format(counter, name)
                    elif name == self.players[ctx.author.id].weapon and self.players[ctx.author.id].weapon_level == "S":
                        SQL = "SELECT `Damage (M)` FROM `Weapons` WHERE `Name` = '{0}'".format(name)
                        datamod.execute(SQL)
                        damage = datamod.cur.fetchone()[0]
                        weapons[counter - 1][2] = damage
                        level = "Medium"
                        cost *= 2
                        weapons[counter - 1][1] = cost
                        description += "`{0}`) **{1}** | Level: `{2}` | Cost: `{3}` | Damage: `{4}`\n".format(counter,
                                                                                                              name,
                                                                                                              level,
                                                                                                              cost,
                                                                                                              damage)
                    else:
                        description += "`{0}`) **{1}** | Level: `{2}` | Cost: `{3}` | Damage: `{4}`\n".format(counter,
                                                                                                              name,
                                                                                                              level,
                                                                                                              cost,
                                                                                                              damage)
            index = 0
            descriptions.append(description)
            if len(descriptions) == 0:
                embed = discord.Embed(colour=discord.Colour.blue(), title="Welcome to the Inferno Forge!",
                                      description=descriptions[index])
                sent_message = await ctx.send(embed=embed)
            else:
                embed = discord.Embed(colour=discord.Colour.blue(), title="Welcome to the Inferno Forge!",
                                      description=descriptions[index])
                embed.set_footer(
                    text="Page `{0}`/`{1}`...React with the emotes to scroll".format(index + 1, len(descriptions)))
                sent_message = await ctx.send(embed=embed)
                await sent_message.add_reaction('02spinleft:678613956327112704')
                await sent_message.add_reaction('surprised:680474277195153484')
                await sent_message.add_reaction('02spinright:678613956025384972')
                try:
                    async def scroll(description_list, desc_index, increment):
                        desc_index += increment
                        if desc_index >= len(description_list):
                            desc_index = 0
                        elif desc_index < 0:
                            desc_index = len(description_list) - 1
                        embed = discord.Embed(colour=discord.Colour.blue(), title="Welcome to the Inferno Forge!",
                                              description=description_list[desc_index])
                        embed.set_footer(
                            text="Page `{0}`/`{1}`...React with the emotes to scroll".format(desc_index + 1,
                                                                                             len(descriptions)))
                        await sent_message.edit(embed=embed)
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                        if reaction.emoji.id == 678613956327112704:
                            await scroll(description_list, desc_index, -1)
                        elif reaction.emoji.id == 678613956025384972:
                            await scroll(description_list, desc_index, 1)
                        elif reaction.emoji.id == 680474277195153484:
                            raise asyncio.TimeoutError

                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    if reaction.emoji.id == 678613956327112704:
                        await scroll(descriptions, index, -1)
                    elif reaction.emoji.id == 678613956025384972:
                        await scroll(descriptions, index, 1)
                    elif reaction.emoji.id == 680474277195153484:
                        raise asyncio.TimeoutError
                except asyncio.TimeoutError:
                    pass
            buy = await self.user_in(ctx, "Would you like to buy one? `Y/N`", ["yes", "yeah", "y", "no", "nah", "n"])
            if buy in ["yes", "yeah", "y"]:
                weapon = await self.user_in(ctx, "Which weapon would you like? Enter the number:",
                                            [str(i) for i in range(1, len(weapons))])
                name, cost, damage = weapons[int(weapon) - 1]
                await ctx.send("You walk up to the shop owner and point at the `{0}`".format(name))
                await ctx.send("The shop owner gives a disgruntled look and tries to take `{0}` gold".format(cost))
                if self.players[ctx.author.id].gold >= cost:
                    self.players[ctx.author.id].gold -= cost
                    if self.players[ctx.author.id].gold <= 0:
                        self.players[ctx.author.id].gold = 0
                    await ctx.send(
                        " The shop keeper takes `{0}` gold from you and equips you with the `{1}`".format(cost, name))
                    await ctx.send("You now have `{0}` gold pieces".format(self.players[ctx.author.id].gold))
                    if name == self.players[ctx.author.id].weapon:
                        self.players[ctx.author.id].WeaponDmg = damage
                        self.players[ctx.author.id].weapon_level = "M"
                    else:
                        self.players[ctx.author.id].weapon = name
                        self.players[ctx.author.id].WeaponDmg = damage
                        self.players[ctx.author.id].weapon_level = "S"
                    await ctx.send("You exit the shop")
                else:
                    await ctx.send(
                        "You only have `{0}` gold! The owner is mad and kicks you out of the store!".format(
                            self.players[ctx.author.id].gold))
            else:
                await ctx.send("The shop owner doesn't understand you and points you towards the exit")
        datamod.terminate()

    async def escape(self, ctx):
        goldloss = random.randint(1, 20)
        healthloss = random.randint(1, 5)
        # self.points -= 10
        # self.morale -= 10
        await ctx.send("You attempt to run away!")
        runchance = random.randint(1, 5)
        if runchance <= 5:
            self.players[ctx.author.id].health -= healthloss
            if self.players[ctx.author.id].health <= 0:
                self.players[ctx.author.id].health = 0
                await ctx.send("While running, you fell into a bed of spikes!")
                raise EndGame
            self.players[ctx.author.id].gold -= goldloss
            if self.players[ctx.author.id].gold <= 0:
                self.players[ctx.author.id].gold = 0
            await ctx.send(
                "You lost `{0}` health and `{1}` gold while trying to run away!".format(healthloss, goldloss))
        else:
            await ctx.send("You were able to escape without losing anything!")

    async def fight(self, ctx, name, monster_xp, monster_health):
        if self.players[ctx.author.id].potion != "None":
            await self.potiondrink(ctx)
        embed = discord.Embed(color=discord.Colour.dark_orange(), title="Battle Time!",
                              description="You vs `{0}`:".format(name))
        embed.set_thumbnail(url=self.players[ctx.author.id].avatar)
        embed.add_field(name="You", value="`{0}` HP | `{1}` XP".format(self.players[ctx.author.id].health,
                                                                       self.players[ctx.author.id].XP))
        embed.add_field(name=f"{name}", value="`{0}` HP | `{1}` XP".format(monster_health, monster_xp))
        sent_message = await ctx.send(embed=embed)
        time.sleep(5)
        while monster_health > 0:
            # monster attack
            monster_chance = random.randint(1, 10)
            monster_damage = int((random.randint(1, 25) / 100) * monster_xp)
            embed = discord.Embed(color=discord.Colour.dark_orange(), title="Battle Time!",
                                  description="You vs `{0}`:".format(name))
            embed.set_thumbnail(url=self.players[ctx.author.id].avatar)
            if monster_chance >= 3:
                embed.add_field(name="Monster's Attack:",
                                value="The monster hits you for `{0}` damage!".format(monster_damage))
                self.players[ctx.author.id].health -= monster_damage
                if self.players[ctx.author.id].health > 0:
                    embed.add_field(name="You now have:", value="`{0}` HP".format(self.players[ctx.author.id].health))
                else:
                    embed.add_field(name="You now have:", value="0 HP")
                    await sent_message.edit(embed=embed)
                    death_embed = discord.Embed(color=discord.Colour.dark_red(), title="Defeat!")
                    death_embed.set_thumbnail(url=self.players[ctx.author.id].avatar)
                    death_embed.add_field(name="R.I.P", value="You died from the monster's attack...")
                    await ctx.send(embed=death_embed)
                    self.players[ctx.author.id].dead = True
                    raise EndGame
            else:
                embed.add_field(name="Monster's Attack:",
                                value="The monster attempts to attack but misses!")
            await sent_message.edit(embed=embed)
            time.sleep(3)
            player_embed = discord.Embed(color=discord.Colour.dark_orange(), title="Battle Time!",
                                         description="You vs `{0}`:".format(name))
            player_embed.set_thumbnail(url=self.players[ctx.author.id].avatar)
            player_chance = random.randint(1, 10)
            if player_chance >= 2:
                player_damage = int((random.randint(75, 100) / 100) * self.players[ctx.author.id].WeaponDmg)
                monster_health -= player_damage
                player_embed.add_field(name="You now attempt to attack the monster!",
                                       value="You hit the monster with `{0}` points of damage!".format(player_damage))
                if monster_health > 0:
                    player_embed.add_field(name="Monster's Health:", value="`{0}` HP".format(monster_health))
                else:
                    player_embed.add_field(name="Monster's Health:", value="0 HP")
                    victory_embed = discord.Embed(color=discord.Colour.gold(), title="Victory!",
                                                  description="You have slain the **`{0}`**!".format(name))
                    goldadd = int((random.randint(25, 75) / 100) * monster_xp)
                    pointsadd = int((random.randint(85, 100) / 100) * monster_xp)
                    self.players[ctx.author.id].XP += pointsadd
                    self.players[ctx.author.id].gold += goldadd
                    victory_embed.add_field(
                        name="You gained `{0}` gold".format(goldadd),
                        value="You now have `{0}` gold pieces".format(self.players[ctx.author.id].gold))
                    victory_embed.add_field(name="You gained `{0}` XP".format(pointsadd),
                                            value="You now have `{0}` XP".format(self.players[ctx.author.id].XP))
                    await ctx.send(embed=victory_embed)
                    await self.levelup(ctx)
            else:
                player_embed.add_field(name="Your Attack:", value="You attempt to attack but miss!")
            await sent_message.edit(embed=player_embed)
            time.sleep(3)

    async def levelup(self, ctx):
        levelpass = int(1000 * (self.players[ctx.author.id].high_multiplier ** (self.players[ctx.author.id].level + 1)))
        if self.players[ctx.author.id].XP >= levelpass:
            self.players[ctx.author.id].health *= self.players[ctx.author.id].low_multiplier
            self.players[ctx.author.id].health = int(self.players[ctx.author.id].health)
            self.players[ctx.author.id].level += 1
            await ctx.send("You leveled up!")
            await ctx.send("You are now level `{0}`!".format(self.players[ctx.author.id].level))
            await ctx.send("Your health has now risen to `{0}` HP!".format(self.players[ctx.author.id].health))

    async def potiondrink(self, ctx):
        choice = await self.user_in(ctx,
                                    "Would you like to drink your `{0}` potion before the fight?".format(
                                        self.players[ctx.author.id].potion),
                                    ["yes", "yeah", "y", "no", "nah", "n"])
        if choice in ["yes", "yeah", "y"]:
            if self.players[ctx.author.id].potion_damage != 0:
                await ctx.send(
                    "You quickly drink the `{0}` and gain `{1}` attack damage!".format(
                        self.players[ctx.author.id].potion, self.players[ctx.author.id].potion_damage))
                self.players[ctx.author.id].WeaponDmg += self.players[ctx.author.id].potion_damage
            elif self.players[ctx.author.id].potion_hp != 0:
                await ctx.send(
                    "You quickly drink the `{0}` and gain `{1}` HP".format(self.players[ctx.author.id].potion,
                                                                           self.players[ctx.author.id].potion_hp))
                self.players[ctx.author.id].WeaponDmg += self.players[ctx.author.id].potion_hp
            self.players[ctx.author.id].potion = "None"
            self.players[ctx.author.id].potion_hp = 0
            self.players[ctx.author.id].potion_damage = 0


class Game(commands.Cog, name="Game"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playgame(self, ctx):
        game_play = self.bot.get_cog('Player_Game')
        if game_play is not None:
            await game_play.play_game(ctx)
        else:
            print("Error Cog not loaded!")


def setup(bot):
    bot.add_cog(Game(bot))
    bot.add_cog(Player_Game(bot))
    print("Game Cog added")

