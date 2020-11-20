import random


class Game:
    def __init__(self):
        self.points = 20
        self.gold = 100
        self.health = 100
        self.morale = 50
        self.weapon = 0
        self.WeaponDmg = 0
        self.level = 0
        self.potion = "no potion"
        self.dead = False
        self.rand = random.randint(1, 500)

    def profile(self):
        print("Points:", self.points)
        print("Gold:", self.gold)
        print("Health:", self.health)
        print("Morale:", self.morale)
        print("Weapon:", self.weapon)
        print("Weapon Damage:", self.WeaponDmg)
        print("Level", self.level)
        print("Potion:", self.potion)
        print("Dead:", self.dead)

    def playgame(self):
        confirm = input(
            "You have {0} points, this will be your levelling system, do you understand? Y/N ".format(self.points))
        if confirm.lower() in ["yes", "yeah", "y"]:
            print("You may continue with your adventure!")
        else:
            print("We're going to continue anyway")
        print("While walking through the woods something jumps out of the bushes!")
        print("Its a wild boar, and it doesnt look happy!")
        self.choice()
        self.profile()
        print("You notice there is a village up ahead...")
        village = input("Do you want to go to the village? (Y/N)")
        if village.lower() in ["yes", "yeah", "y"]:
            shop = "y"
            while shop in ["yes", "yeah", "y"]:
                shoptype = input("Would you like to go to:\n1. Potion Store\n2. Blacksmiths\n3. Forge\n")
                self.openshop(shoptype)
                self.profile()
                shop = input("Do you want to go to another store? (Y/N)")
        print("You decide to continue traveling through the woods")
        print("While in the woods you begin to here a rustling noise")
        # add other monsters here
        monsterchance = random.randint(1, 100)
        if monsterchance >= 2:
            print("Out pops a goblin from a nearby bush!")
            print("The goblin goes in for a attack!")
            choice = input("Do you want to fight or run?")
            if choice == "run":
                self.escape()
            elif choice == "fight":
                self.fight()
            self.profile()
        else:
            print("You check the bush and find a magic pile of money along with a silver key")
            self.gold += 20
            print("You found 20 gold inside the bag, you now have", self.gold, "pieces")
        print("After getting away from the goblin you notice a small cave nearby")
        cave = input("Do you want to enter the cave?")
        if cave.lower() in ["yes", "yeah", "y"]:
            print("You enter the cave")
            print("Out pops another goblin!")
            choice = input("Do you want to fight or run?")
            if choice == "run":
                self.escape()
                print("You ran away from the goblin and escaped the cave!")
                print("You continue to follow the trail")
            elif choice == "fight":
                self.fight()
                print("After defeating the goblin you search the cave and find some treasure!")
                self.gold += 15
                print("You found 15 gold!")
                print("You exit the cave and continue on the trail")
            self.profile()
        else:
            print("You continue on the trail and ignore the cave!")
        print(
            "While following the trail you find two routes to take, one up a dangerous cliff, and the other is a more safe path")
        cliffpath = input("Which one would you like to take? Cliff or Path")
        if cliffpath == "path":
            print(
                "You choose to go the safe route, but while following the path a bandit surprises you and charges in for a attack!")
            self.choice()
        elif cliffpath == "cliff":
            climb = random.randint(1, 10)
            while climb <= 5:
                print("You attempted to climb the cliff but fell!")
                climb += 1
                healthloss = random.randint(1, 5)
                self.health -= healthloss
                print("You lost", healthloss, "health from the fall!")
                self.profile()
                if self.health <= 0:
                    self.dead = True
                    print("Wow you died from the fall...")
            print("You successfully climbed the cliff!")
            print("When you reach the top of the cliff you see a small village (this will be your last time to shop)")
            village = input("Do you want to go to the village? (Y/N)")
            if village.lower() in ["yes", "yeah", "y"]:
                shop = input("Would you like to go to the Potion Store, Blacksmiths or the Forge?")
                while shop.lower() in ["yes", "yeah", "y"]:
                    shoptype = input("Would you like to go to the Potion Store, Blacksmiths or the Forge?")
                    self.openshop(shoptype)
                    self.profile()
                    shop = input("Do you want to go to another store? (Y/N)")
            else:
                print("You decide not to go into the village and continue following the path")
        print("You continue to follow the path and finally reach the top of the mountain")

    def choice(self):
        choice = input("Do you want to fight or run?")
        if choice == "run":
            self.escape()
        elif choice == "fight":
            self.fight()

    def openshop(self, shoptype):
        print("------------")
        print("shoptype", shoptype, type(shoptype))
        if shoptype == "1":
            print("You walk into the potion shop and notice there's a few items that catch your interest")
            print("Health+2: 10G\nStrength+2: 10G")
            buy = input("Would you like to buy one?")
            if buy.lower() in ["yes", "yeah", "y"]:
                potion = input("Which potion would you like")
                if potion == "health":
                    print(
                        "You walk up to the shop owner and point at the small red flask, the shop owner gives a disgruntled look and tries to take 15 gold")
                    if self.gold >= 15:
                        self.gold -= 15
                        print(" The shop keeper takes 15 gold from you and hands you the potion")
                        print("You now have", self.gold, "gold pieces")
                        self.potion = "health"
                        print("You now have a", self.potion, "potion")
                        print("Be careful you can only have one potion at a time")
                        print("You exit the shop")
                elif potion == "strength":
                    print(
                        "You walk up to the shop owner and point at the small green flask, the shop owner gives a disgruntled look and tries to take 15 gold")
                    if self.gold >= 10:
                        self.gold -= 10
                        print("The shop keeper takes 10 gold from you and hands you the potion")
                        print("You now have", self.gold, "gold pieces")
                        self.potion = "strength"
                        print("You now have a", self.potion, "potion")
                        print("Be careful you can only have one potion at a time")
                        print("You exit the shop")
            else:
                print("The shop owner doesn't understand you and points you towards the exit")
        elif shoptype == "2":
            print("You walk into the weapon shop and notice there's a few items that catch your interest")
            print(" Leather Armor+5: 20G\nIron Armor+10: 25G")
            buy = input("Would you like to buy one?")
            if buy.lower() in ["yes", "yeah", "y"]:
                armor = input("Which armor would you like?")
                if armor == "leather":
                    print("You point at the Leather Armor and the shop keeper tries to take 20 gold")
                    if self.gold >= 20:
                        self.gold -= 20
                        self.health += 5
                        print("You now have", self.health, "health")
                        print("You exit the shop")
                    else:
                        print('The shopkeeper says: "You dont have enough gold for that, now get out!"')
                        print("You leave the shop")
                if armor == "iron":
                    print("You point at the Iron Armor and the shop keeper tries to take 25 gold")
                    if self.gold >= 25:
                        self.gold -= 25
                        self.health += 10
                        print("You now have", self.health, "health")
                        print("You exit the shop")
                    else:
                        print('The shopkeeper says: "You dont have enough gold for that, now get out!"')
                        print("You leave the shop")
            else:
                print("The shop owner doesn't understand you and points you towards the exit")
        elif shoptype == "3":
            print("You walk into the weapon shop and notice there's a few items that catch your interest")
            print(" Sword+3: 15G\nAxe+5: 20G")
            buy = input("Would you like to buy one?")
            if buy.lower() in ["yes", "yeah", "y"]:
                weapon = input("Which weapon would you like?")
                if weapon.lower() == "sword":
                    self.WeaponDmg = 0
                    print("You point at the sword and the shop keeper tries to take 15 gold")
                    if self.gold >= 15:
                        self.gold -= 15
                        print("The shop keeper takes 15 gold from you and hands you the sword")
                        print("You now have", self.gold, "gold pieces")
                        self.WeaponDmg += 3
                        self.weapon = "sword"
                        print("You now deal a extra", self.WeaponDmg, "damage with your new", self.weapon, "!")
                        print("You exit the shop")
                    else:
                        print('The shopkeeper says: "You dont have enough gold for that, now get out!"')
                        print("You leave the shop")
                elif weapon.lower() == "axe":
                    self.WeaponDmg = 0
                    print("You point at the sword and the shop keeper tries to take 20 gold")
                    if self.gold >= 20:
                        self.gold -= 20
                        print("The shop keeper takes 20 gold from you and hands you the sword")
                        print("You now have", self.gold, "gold pieces")
                        self.WeaponDmg += 5
                        self.weapon = "axe"
                        print("You now deal a extra", self.WeaponDmg, "damage with your new", self.weapon, "!")
                        print("You exit the shop")
                    else:
                        print('The shopkeeper says: "You dont have enough gold for that, now get out!"')
                        print("You leave the shop")

    def escape(self):
        goldloss = random.randint(1, 20)
        healthloss = random.randint(1, 5)
        self.points -= 10
        self.morale -= 10
        print("You attempt to run away!")
        runchance = random.randint(1, 5)
        if runchance <= 5:
            self.health -= healthloss
            self.gold -= goldloss
            print("You lost", healthloss, "health and", goldloss, "gold while trying to run away!")
        else:
            print("You were able to escape without losing anything!")

    def fight(self):
        if self.potion != "no potion":
            self.potiondrink()
        monsterhealth = random.randint(1, 10) * (self.level + 1)
        while monsterhealth > 0:
            # monster attack
            monsterdamage = random.randint(1, 5) * (self.level + 1)
            monsterdamage += 1
            if monsterdamage >= 4:
                print("The monster hits you for", monsterdamage, "damage!")
                self.health -= monsterdamage
                if self.health <= 0:
                    print("You died from the monster's attack...")
                    self.dead = True
            elif monsterdamage < 2:
                print("The monster attempts to attack but misses!")
            print("You attempt to attack the monster!")
            # player attack
            attackdmg = random.randint(1, 5)
            attackdmg += self.WeaponDmg
            if attackdmg >= 2:
                monsterhealth -= attackdmg
                print("You hit the monster with", attackdmg, "points of damage!")
                if monsterhealth <= 0:
                    print("You killed the monster!")
                    goldadd = random.randint(1, 15)
                    pointsadd = random.randint(1, 10)
                    self.points += pointsadd
                    self.gold += goldadd
                    print("You gained", goldadd, "gold, you now have", self.gold, "gold pieces")
                    print("You gained", pointsadd, "gold, you now have", self.points, "points")
                    print("You now have", self.health, "hit points")
                    self.levelup()
            elif attackdmg <= 1:
                print("You missed your attack!")

    def levelup(self):
        levelpass = 10
        if self.points >= levelpass:
            self.health += 10
            self.WeaponDmg += 1
            self.points -= levelpass
            levelpass += 10
            self.level += 1
            print("You leveled up!")
            print("You are now level", self.level, "!")
            print("You gained 10 hit points!")
            print("You now deal 1 extra damage!")

    def potiondrink(self):
        choice = input("Would you like to drink your {0} potion before the fight?".format(self.potion))
        if choice in ["yes", "yeah", "y"]:
            if self.potion == "health":
                print("You quickly drink the health potion and gain 2 health!")
                self.health += 2
            if self.potion == "strength":
                print("You quickly drink the strength potion and gain 2 attack damage!")
                self.WeaponDmg += 2


print("yeet")
play = Game()
play.playgame()
