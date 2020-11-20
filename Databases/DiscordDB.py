import pymysql
from sshtunnel import SSHTunnelForwarder


class Database:

    def initialize(self, server_name):
        self.server = SSHTunnelForwarder(
            '51.75.163.1',
            ssh_username='karthik',
            ssh_password='btm56Vy.3',
            remote_bind_address=('127.0.0.1', 3306)
        )
        self.server.start()

        self.cnx = pymysql.connect(
            host='localhost',
            port=self.server.local_bind_port,
            user='discordb0t',
            password='d1sCORDb()t!',
            db='discordbot'
        )
        print("Connection Successful!")
        self.cur = self.cnx.cursor()
        self.server_name = server_name
        self.cur.execute("SHOW TABLES")
        self.tables = [table_name for (table_name,) in self.cur]
        if self.server_name not in self.tables:
            self.create_table()

    def create_table(self):
        SQL = "CREATE TABLE `{0}` LIKE `{1}`".format(self.server_name, "Default_Table")
        self.cur.execute(SQL)
        self.cnx.commit()

    def add_member(self, *member):
        if not self.check_mem('Main', member[0]):
            SQL = "INSERT INTO `Main`(`UID`, `Name`, `Avatar`, `Bot`, `Banned`, `Credits`, `Level`, `XP`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cur.execute(SQL, member)
            self.cnx.commit()
            SQL = "INSERT INTO `{0}`(`UID`, `Name`, `Avatar`, `Bot`, `Banned`, `Credits`, `Level`, `XP`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)".format(
                self.server_name)
            self.cur.execute(SQL, member)
            self.cnx.commit()
        elif self.check_mem('Main', member[0]):
            SQL = "INSERT INTO `{0}`(`UID`, `Name`, `Avatar`, `Bot`, `Banned`, `Credits`, `Level`, `XP`) " \
                  "SELECT `UID`, `Name`, `Avatar`, `Bot`, `Banned`, `Credits`, `Level`, `XP` " \
                  "FROM `Main` WHERE `Main`.`UID` = {1}".format(
                self.server_name, member[0])
            self.cur.execute(SQL)
            self.cnx.commit()

    def remove_member(self, member_id):
        SQL = "DELETE FROM `{0}` WHERE `{0}`.`UID` = {1}".format(self.server_name, member_id)
        self.cur.execute(SQL)
        self.cnx.commit()

    def check_mem(self, server_name, member_id):
        SQL = "SELECT 1 FROM `{0}` WHERE `{0}`.`UID` = {1}".format(server_name, member_id)
        self.cur.execute(SQL)
        x = self.cur.fetchone()
        if isinstance(x, type(None)):
            return False
        return True

    def reset_credits(self, member_id, amount):
        for table in self.tables:
            if self.check_mem(table, member_id):
                SQL = "UPDATE `{0}` SET `Credits` = '{1}' WHERE `{0}`.`UID` = {2}".format(table, amount, member_id)
                self.cur.execute(SQL)
                self.cnx.commit()

    def reset_xp(self, member_id):
        for table in self.tables:
            if self.check_mem(table, member_id):
                SQL = "UPDATE `{0}` SET `XP` = '{1}' WHERE `{0}`.`UID` = {2}".format(table, 0, member_id)
                self.cur.execute(SQL)
                self.cnx.commit()

    def update_pfp(self, member_id, avatar_url):
        for table in self.tables:
            if self.check_mem(table, member_id):
                SQL = "UPDATE `{0}` SET `Avatar` = '{1}' WHERE `{0}`.`UID` = {2}".format(table, avatar_url, member_id)
                self.cur.execute(SQL)
                self.cnx.commit()

    def update_name(self, new_name, member_id):
        for table in self.tables:
            if self.check_mem(table, member_id):
                SQL = "UPDATE `{0}` SET `Name` = '{1}' WHERE `{0}`.`UID` = {2}".format(table, new_name, member_id)
                self.cur.execute(SQL)
                self.cnx.commit()

    def update_table(self, current_name):
        SQL = "ALTER TABLE `{0}` RENAME TO `{1}`".format(self.server_name, current_name)
        self.cur.execute(SQL)
        self.cnx.commit()

    def update_xp(self, member_id, xp_gain):
        SQL = ""

    def fetch_profile(self, member_id):
        SQL = "SELECT * FROM `Main` WHERE `Main`.`UID` = %s"
        self.cur.execute(SQL, member_id)
        elements = [element for element in self.cur.fetchone()]
        return elements

    def terminate(self):
        print("terminated")
        self.cur.close()
        self.cnx.close()
        self.server.close()
