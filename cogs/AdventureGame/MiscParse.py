import json
import random
import sys

sys.path.insert(0, '../..')
import AkitrixDB

# with open('MonsterNames.json', "r") as f:
#     data_p = json.loads(f.read())
#     data_j = json.dumps(data_p, indent=2)
#     # [name,xp,challenge,size,alignment]
#     print(data_j)
#     datamod = AkitrixDB.Database()
#     datamod.initialize(0, 0)
#     for item in data_p:
#         # print(data_p[item]["name"], (item["challenge"]), (item["XP"]), item["size"], item["alignment"])
#         challenge = data_p[item]["challenge"]
#         if challenge == "1/2":
#             challenge = 0.5
#         elif challenge == "1/8":
#             challenge = 0.125
#         elif challenge == "1/4":
#             challenge = 0.25
#         name = data_p[item]["name"]
#         name = re.sub("[\']",'',name)
#         alignment = data_p[item]["alignment"]
#         if len(alignment)>10:
#             alignment = "Any"
#         print(name)
#         SQL = "INSERT INTO `Monsters`(`Name`, `Challenge`, `XP`, `Size`, `Alignment`) VALUES ('{0}',{1},{2},'{3}','{4}')".format(
#             name, float(challenge), int(data_p[item]["xp"]), data_p[item]["size"],
#             alignment)
#         print(SQL)
#         datamod.execute(SQL)
#     datamod.terminate()

with open('weapon2.json', "r") as d:
    weapons = d.read()
    # print(weapons)
    data_p = json.loads(weapons)
    data_j = json.dumps(data_p, indent=2)
    print(data_j)

    # datamod = AkitrixDB.Database()
    # datamod.initialize(0, 0)
    # for item in data_p:
    #     type = data_p[item]["type"]
    #     name = data_p[item]["name"]
    #     name = re.sub("[\']", '', name)
    #     if type in ["Weapon","Armor","Potion"]:
    #         SQL = "INSERT INTO `Items`(`Name`, `Type`,`Rarity`) VALUES ('{0}','{1}','{2}')".format(name,type,data_p[item]["rarity"])
    #         print(SQL)
    #         datamod.execute(SQL)
    # datamod.terminate()

    datamod = AkitrixDB.Database()
    datamod.initialize(0, 0)
    base_stats = {"gp": 100, "sp": 50, "attack": 100}
    for item in data_p:
        '''let gp=100, sp=50, base attack pow = 100'''
        print(item['Simple Weapons'])
        cost = item["Cost"]
        print("cost", cost, type(cost))
        if cost != "0" and cost != "?" and cost != "special":
            cost_list = cost.split(' ')
            print(cost_list)
            cost = int(cost_list[0]) * base_stats[cost_list[1]]
        elif cost == "special":
            cost = random.randint(20, 50)
        else:
            cost = 0
        damage_s = item['Dmg (S)'].split('d')
        damage_s = (10 ** int(damage_s[0])) * int(damage_s[1])
        damage_m = item['Dmg (M)'].split('d')
        damage_m = (10 ** int(damage_m[0])) * int(damage_m[1])
        SQL = "INSERT INTO `Weapons`(`Name`,`Cost`,`Damage (S)`,`Damage (M)`) VALUES ('{0}',{1},{2},{3})".format(
            item['Simple Weapons'], cost, damage_s, damage_m)
        print(SQL)
        datamod.execute(SQL)
    datamod.terminate()
