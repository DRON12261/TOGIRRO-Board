import pyodbc

server = 'localhost\sqlexpress'
dbname = 'TOGIRRO'
user = 'DESKTOP-M7C36LJ\DRON12261'
password = '12262000'
print("SAS")
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+dbname+';UID='+user+';Trusted_connection=yes')
print("LOL")

# server = 'localhost\sqlexpress' 
# database = 'mydb' 
# username = 'myusername' 
# password = 'mypassword' 
# conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = conn.cursor()

#cursor.execute("INSERT INTO InferiorList (ChiefID, InferiorID) VALUES(7, 8)")
#cursor.execute("INSERT INTO Employees (Surname, Name, Patronymic, Login, Password, RightsLevel) VALUES('Test','Test', 'Test02', 'TestUser2', 'User1234', 0)")
#cursor.execute("INSERT INTO Employees (Surname, Name, Patronymic, Login, Password, RightsLevel) VALUES('Плотоненко','Юрий', 'Анатольевич', 'ПЮА', '1234567', 3)")

#cursor.execute("DELETE FROM Employees WHERE Name='Юрий'")
conn.commit()
#print(cursor.execute("SELECT * FROM Employees").fetchall())
answer = cursor.execute("SELECT * FROM Employees WHERE EmployeeID NOT IN (6,7)").fetchall()
print(answer)
