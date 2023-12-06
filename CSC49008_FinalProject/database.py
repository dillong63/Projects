### Code written by Dillon Geary for CSC 49008 final project

import sqlite3

#functions that can be used to create a new sqlite table and database. I executed them once and are no  longer needed;
con =sqlite3.connect('parking.db')
def createTable(db):
	cur= db.cursor()
	cur.execute("CREATE TABLE carP(id VARCHAR(20), arrTime INT)")
	
def createTotalTable(db):
	cur= db.cursor()
	cur.execute("CREATE TABLE moneyMade(Money REAL)")
	
#function update the money made for the day
def updateFin(db,mon):
	cur= db.cursor()
	cur.execute("UPDATE moneyMade SET Money=Money+?",(mon,))

#function to return money made for the day
def returnMon(db):
	cur = db.cursor()
	res = cur.execute("SELECT * FROM moneyMade")
	t=res.fetchone()
	return t[0]

#function to add a new car to table
def newCar(db,data):
	cur= db.cursor()
	cur.execute("INSERT INTO carP VALUES(?,?)",data)

#check if the car is in table
def checkCar(db,carID):
	cur= db.cursor()
	temp = [carID]
	res = cur.execute("SELECT id FROM carP WHERE id=(?)",temp)
	#there will be one match or none
	if res.fetchone() is None:
		return 0
	else:
		return 1 #car found
		
#returns arrival time of car
def timeCar(db,carID):
	cur= db.cursor()
	temp = [carID]
	res = cur.execute("SELECT arrTime FROM carP WHERE id=(?)",temp)
	t=res.fetchone()
	return t[0]
		
#function to remove car from table
def leaveCar(db,carID):
	cur= db.cursor()
	temp = [carID]
	cur.execute("DELETE FROM carP WHERE id=(?)",temp)



