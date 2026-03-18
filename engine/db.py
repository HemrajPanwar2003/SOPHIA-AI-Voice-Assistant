import sqlite3

con = sqlite3.connect("Krishna.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id INTEGER PRIMARY KEY,name VARCHAR(100),path VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (NULL,'one note','C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE')"
# cursor.execute(query)

# con.commit()
# con.close()
# query = "CREATE TABLE IF NOT EXISTS web_command(id INTEGER PRIMARY KEY, name VARCHAR(100),url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (NULL,'canva','https://www.canva.com/')"
# cursor.execute(query)

# con.commit()
# con.close()

# testing module
app_name = "android studio"
cursor.execute("SELECT path FROM sys_command WHERE name = ?", (app_name,))
results = cursor.fetchall()

if results:
    print(results[0][0])
