import mysql.connector

# Connect to the existing InventoryDB
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Letmein2272",
    database="InventoryDB"
)
cursor = conn.cursor()

# Example insert into Provider table
sql = "INSERT INTO Provider (ProviderID, ProviderName, ProviderAddress) VALUES (%s, %s, %s)"
values = (1, "Tech Supplies Ltd", "123 Tech Street, Silicon City")

cursor.execute(sql, values)
conn.commit()

print("✅ Data inserted successfully into Provider.")

cursor.close()
conn.close()
