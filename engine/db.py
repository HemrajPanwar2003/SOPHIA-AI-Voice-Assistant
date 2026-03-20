import sqlite3

con = sqlite3.connect("Krishna.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id INTEGER PRIMARY KEY,name VARCHAR(100),path VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (NULL,'powerpoint','C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE')"
# cursor.execute(query)

# con.commit()
# con.close()
# query = "CREATE TABLE IF NOT EXISTS web_command(id INTEGER PRIMARY KEY, name VARCHAR(100),url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (NULL,'google','https://www.google.com/')"
# cursor.execute(query)

# con.commit()
# con.close()

# testing module
# app_name = "android studio"
# cursor.execute("SELECT path FROM sys_command WHERE name = ?", (app_name,))
# results = cursor.fetchall()

# if results:
#   print(results[0][0])

# Create a table with the desired columns
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS contacts (
#   id integer primary key,
#  name VARCHAR(200),
# mobile_no VARCHAR(255),
# email VARCHAR(255) NULL
# )
# """)

# Create a table with the desired columns
# cursor.execute(
#   """CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)""")

# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 18]

# with open("contacts.csv", "r", encoding="utf-8") as csvfile:
#   csvreader = csv.reader(csvfile)

#    next(csvreader)  # skip header

#   for row in csvreader:
#      try:
#         selected_data = [row[i] for i in desired_columns_indices]

#        cursor.execute(
#           """
#      INSERT INTO contacts (name, mobile_no)
#     VALUES (?, ?)
#    """,
#       tuple(selected_data), )

# except IndexError:
#   continue  # skip bad rows

# con.commit()
# con.close()

# cursor.execute(
#   "INSERT INTO contacts (name, mobile_no) VALUES (?, ?)", ("Hemraj", "9772549748")
# )

# con.commit()
# con.close()

# query = "kunal"
# query = query.strip().lower()

# cursor.execute(
#   """
# SELECT mobile_no FROM contacts
# WHERE LOWER(name) LIKE ?
# """,
#   ("%" + query + "%",),)

# results = cursor.fetchall()

# if results:
#   print(results[0][0])
