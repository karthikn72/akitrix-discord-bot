import platform

import pymysql
from sshtunnel import SSHTunnelForwarder


class Database:
    plat = platform.system()

    def initialize(self, server_ID, server_name):
        if self.plat != "Linux":
            self.server = SSHTunnelForwarder(
                'YOUR SERVER ADDRESS',
                ssh_username='YOUR SSH USERNAME',
                ssh_password='YOUR SSH PASSWORD',
                remote_bind_address=('127.0.0.1', 3306)
            )
            self.server.start()

            self.cnx = pymysql.connect(
                host='localhost',
                port=self.server.local_bind_port,
                user='YOUR MYSQL DATABASE USERNAME',
                password='YOUR MYSQL DB PASSWORD',
                db='YOUR MYSQL DB NAME'
            )
        else:
            self.cnx = pymysql.connect(
                host='localhost',
                user='YOUR MYSQL DATABASE USERNAME',
                password='YOUR MYSQL DB PASSWORD',
                db='YOUR MYSQL DB NAME'
            )
        print("Connection Successful!")
        self.cur = self.cnx.cursor()
        self.server_ID = server_ID
        self.server_name = server_name
        self.cur.execute("SELECT `SID` FROM `Servers`")
        self.servers = [sid for (sid,) in self.cur]
        self.check_server()

    def check_server(self):
        if self.server_ID not in self.servers:
            self.create_server()
        else:
            SQL = "SELECT `ServerName` FROM `Servers` WHERE `Servers`.`SID` = {0}".format(self.server_ID)
            self.execute(SQL)
            name = self.cur.fetchone()
            if name[0] != self.server_name:
                self.update_server()

    def create_server(self):
        SQL = "INSERT INTO `Servers`(`SID`,`ServerName`) VALUES ({0},'{1}')".format(self.server_ID, self.server_name)
        self.execute(SQL)
        print("New Server Added:", self.server_name)
        print("Server ID:", self.server_ID)

    def update_server(self):
        SQL = "UPDATE `Servers` SET `ServerName` = '{0}' WHERE `Servers`.`SID` = {1}".format(self.server_name,
                                                                                             self.server_ID)
        self.execute(SQL)
        print("Server Name changed to:", self.server_name)
        print("Server ID:", self.server_ID)

    def add_member(self, *member):
        indb, inserver, ingame = self.check_mem(member[0])
        print("server", inserver, "db", indb, "game", ingame)
        # in_game = self.check_player(member[0])
        if not ingame:
            SQL = "INSERT INTO `UserItems`(`UID`) VALUES ({0})".format(member[0])
            self.execute(SQL)
            print("New Player ID: {0}".format(member[0]))
        if inserver and indb:
            """member id, member name, avatar url, 0,10000, 1, 100"""
            SQL = "SELECT `Name`,`Avatar` FROM `Main` WHERE `Main`.`UID` = {0}".format(member[0])
            self.execute(SQL)
            x = self.cur.fetchone()
            if member[1] != x[0]:
                self.update_name(member[0], member[1])
            if member[2] != x[1]:
                self.update_pfp(member[0], member[2])
            SQL = "SELECT `WID` FROM `UserItems` WHERE `UserItems`.`UID` = {0} ".format(member[0])
            self.execute(SQL)
            x = self.cur.fetchone()
            if x[0] == 0:
                self.update_weapon(member[0], 'Unarmed strike', 'S')
            return False

        if not indb:
            SQL = "INSERT INTO `Main`(`UID`, `Name`, `Avatar`, `Bot`,`Credits`, `Level`, `XP`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            self.cur.execute(SQL, member)
            self.cnx.commit()
            print("New Member info:", member)

        SQL = "INSERT INTO `UServers` (`UID`,`SID`,`Present`) VALUES ({0},{1},1)".format(member[0], self.server_ID)
        self.execute(SQL)
        print("Member Updated:", member[0])
        return True

    def remove_member(self, member_id):
        SQL = "UPDATE `UServers` SET `Present` = 0 WHERE `UServers`.`UID` = {0} AND `UServers`.`SID` = {1}".format(
            member_id, self.server_ID)
        self.execute(SQL)
        print("Member removed:", member_id)
        print("From:", self.server_name)

    def check_mem(self, member_id):
        """returns in_server, in_db, in_game"""
        SQL = "SELECT 1 FROM `Main` WHERE `Main`.`UID` = {0}".format(member_id)
        self.execute(SQL)
        in_db = self.cur.fetchone()
        SQL = "SELECT 1 FROM `UServers` WHERE `UServers`.`UID` = {0} AND `UServers`.`SID` = {1}".format(member_id,
                                                                                                        self.server_ID)
        self.execute(SQL)
        in_server = self.cur.fetchone()
        SQL = "SELECT 1 FROM `UserItems` WHERE `UserItems`.`UID` = {0}".format(member_id)
        self.execute(SQL)
        in_game = self.cur.fetchone()
        return (not isinstance(in_db, type(None))), (not isinstance(in_server, type(None))), (
            not isinstance(in_game, type(None)))

    # def check_player(self, member_id):
    #     SQL = "SELECT 1 FROM `UserItems` WHERE `UserItems`.`UID` = {0}".format(member_id)
    #     self.execute(SQL)
    #     x = self.cur.fetchone()
    #     if isinstance(x, type(None)):
    #         return False

    def reset_credits(self, member_id, amount):
        SQL = "UPDATE `Main` SET `Credits` = '{0}' WHERE `Main`.`UID` = {1}".format(amount, member_id)
        self.execute(SQL)
        print("Member's credits updated:", member_id)

    def execute(self, *sql):
        SQL = (' '.join(sql)).strip(' ')
        print("SQL:", SQL)
        self.cur.execute(SQL)
        self.cnx.commit()
        print("SQL Command executed:", SQL)

    def reset_xp(self, member_id):
        SQL = "UPDATE `Main` SET `XP` = 0 WHERE `Main`.`UID` = {0}".format(member_id)
        self.execute(SQL)
        print("Member's credits updated:", member_id)

    def update_pfp(self, member_id, avatar_url):
        SQL = "UPDATE `Main` SET `Avatar` = '{0}' WHERE `Main`.`UID` = {1}".format(avatar_url, member_id)
        self.execute(SQL)
        print("Member's profile picture updated:", member_id)

    def update_name(self, member_id, new_name):
        SQL = "UPDATE `Main` SET `Name` = '{0}' WHERE `Main`.`UID` = {1}".format(new_name, member_id)
        self.execute(SQL)
        print("Member's name updated:", member_id, "to:", new_name)

    def update_xp(self, member_id, xp_gain):
        SQL = ""

    def update_weapon(self, member_id, weapon_name, weapon_level):
        SQL = "UPDATE `UserItems` SET `WID` = (SELECT `WID` FROM `Weapons` WHERE `Name`='{0}'),`Weapon Level` = '{1}' WHERE `UID`= {2}".format(
            weapon_name, weapon_level, member_id)
        self.execute(SQL)
        print("Weapon Updated: {0}\nat level: {1}\nfor member ID: {2}\nfor server ID: {3}".format(weapon_name,
                                                                                                  weapon_level,
                                                                                                  member_id,
                                                                                                  self.server_ID))

    def update_potion(self, member_id, potion_name):
        SQL = "UPDATE `UserItems` SET `UserItems`.`PID` = `Items`.`IID` WHERE `Items`.`Name`={0} AND `UserItems`.`UID`= '{1}'".format(
            potion_name, member_id)
        self.execute(SQL)
        print("Potion Updated: {0}\nfor member ID: {1}".format(potion_name, member_id))

    def update_armor(self, member_id, armor_name, armor_level):
        SQL = "UPDATE `UserItems` SET `UserItems`.`AID` = `Weapons`.`AID`,`UserItems`.`Armor Level` = {0} WHERE `Items`.`Name`='{1}' AND `UserItems`.`UID`= '{2}'".format(
            armor_level, armor_name, member_id)
        self.execute(SQL)
        print("Armor Updated: {0}\nat level: {1}\nfor member ID: {2}".format(armor_name, armor_level, member_id))

    def fetch_profile(self, member_id):
        SQL = "SELECT * FROM `Main` WHERE `Main`.`UID` = %s"
        self.cur.execute(SQL, member_id)
        elements = [element for element in self.cur.fetchone()]
        return elements

    def fetch_gameprofile(self, member_id):
        # SQL = "SET @potion_name = (SELECT `Item Name` FROM `UserItems`,`Items` WHERE `UserItems`.`UID` = {0} AND `UserItems`.`SID` = {1} AND `UserItems`.`PID` = `Items`.`IID`);" \
        #       "SET @armor_name = (SELECT `Item Name` FROM `UserItems`,`Items` WHERE `UserItems`.`UID` = {0} AND `UserItems`.`SID` = {1} AND `UserItems`.`AID` = `Items`.`IID`);" \
        #       "SET @weapon_name = (SELECT `Name` FROM `UserItems`,`Weapons` WHERE `UserItems`.`UID` = {0} AND `UserItems`.`SID` = {1} AND `UserItems`.`WID` = `Weapons`.`WID`);" \
        #       "SET @user_name = (SELECT `Name` FROM `UserItems`,`Main` WHERE `UserItems`.`UID` = {0} AND `UserItems`.`UID`=`Main`.`UID`);" \
        #       "SET @weapon_level = (SELECT `Weapon Level` FROM `UserItems` WHERE `UserItems`.`UID` = {0} AND `UserItems`.`SID` = {1});" \
        #       "SET @armor_level = (SELECT `Armor Level` FROM `UserItems` WHERE `UserItems`.`UID` = {0} AND `UserItems`.`SID` = {1});" \
        #       "SELECT @user_name, @weapon_name, @weapon_level, @potion_name, @armor_name, @armor_level;".format(member_id, self.server_ID)

        self.cur.execute(
            "SET @potion_name = (SELECT `Item Name` FROM `UserItems`,`Items` WHERE `UserItems`.`UID` = %s AND `UserItems`.`PID` = `Items`.`IID`)",
            member_id)
        self.cur.execute(
            "SET @armor_name = (SELECT `Item Name` FROM `UserItems`,`Items` WHERE `UserItems`.`UID` = %s AND `UserItems`.`AID` = `Items`.`IID`)",
            member_id)
        self.cur.execute(
            "SET @weapon_name = (SELECT `Name` FROM `UserItems`,`Weapons` WHERE `UserItems`.`UID` = %s AND `UserItems`.`WID` = `Weapons`.`WID`)",
            member_id)
        self.cur.execute(
            "SET @user_name = (SELECT `Name` FROM `UserItems`,`Main` WHERE `UserItems`.`UID` = %s AND `UserItems`.`UID`=`Main`.`UID`)",
            member_id)
        self.cur.execute(
            "SET @user_avatar = (SELECT `Avatar` FROM `UserItems`,`Main` WHERE `UserItems`.`UID` = %s AND `UserItems`.`UID`=`Main`.`UID`)",
            member_id)
        self.cur.execute("SELECT @potion_name,@armor_name,@weapon_name,@user_name,@user_avatar")
        elements = [element for element in self.cur.fetchone()]
        self.cur.execute("SELECT `Weapon Level`,`Armor Level` FROM `UserItems` WHERE `UserItems`.`UID` = %s", member_id)
        for i in self.cur.fetchone():
            elements.append(i)
        return elements

    def terminate(self):
        self.cur.close()
        self.cnx.close()
        if self.plat != "Linux":
            self.server.close()
