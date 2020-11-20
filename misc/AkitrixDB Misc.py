import AkitrixDB

datamod = AkitrixDB.Database()
datamod.initialize(459815151445737482, 'Epic Yeet')
# SQL = "SELECT `WID` FROM `Weapons` WHERE `Name`='Unarmed strike'"
# datamod.execute(SQL)
# x = datamod.cur.fetchone()
# SQL = "UPDATE `Weapons` SET `Damage (S)` = 2*`Cost`"
# datamod.execute(SQL)
# SQL = "UPDATE `Weapons` SET `Damage (S)` = 2*`Cost`"
# SQL = "UPDATE `Weapons` SET `Damage (M)` = 3*`Cost`"
# SQL = "SELECT `Item Name`,`Cost`,`HP`,`Damage` FROM `Items` WHERE `Item Name` LIKE '% Armor'"
# SQL = "UPDATE `UserItems` SET `Time` = CURRENT_TIMESTAMP"
SQL = "SELECT `Time` FROM `UserItems` WHERE `UID`={0}".format(320937702767984642)
datamod.execute(SQL)
# potions = datamod.cur.fetchall()
# potions = list(potions)
datamod.terminate()

my_dict = {'thumbnail': {
    'url': 'https://cdn.discordapp.com/avatars/432126465254096896/f6cd60963db07e02ee0a41115bbc13c9.webp?size=1024'},
    'fields': [{'inline': False, 'name': 'User ID:', 'value': '432126465254096896'},
               {'inline': True, 'name': 'Level:', 'value': '1'}, {'inline': True, 'name': 'XP:', 'value': '100'},
               {'inline': True, 'name': 'Credits:', 'value': '1000'}], 'color': 2123412, 'type': 'rich',
    'title': "Gioraffe Joestar >~<'s profile"}
