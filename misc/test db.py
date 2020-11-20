import pymysql

db = pymysql.connect("localhost", "testuser", "test123", "test3")

cursor = db.cursor()

cursor.execute("USE test3")

cursor.execute("SHOW TABLES")

print("These are the available tables:", [table_name for (table_name,) in cursor])

sql = """CREATE TABLE TEACHERS (
    FIRST_NAME CHAR(30) NOT NULL,
    LAST_NAME CHAR(30),
    AGE INT,
    SUBJECT CHAR(30))"""

cursor.execute(sql)

db.close()
