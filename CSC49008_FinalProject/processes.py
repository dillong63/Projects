#Code written by Dillon Geary for CSC49008 final project

#import all my libraries needed
from multiprocessing import Process, Value, Lock, Manager
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import time 
from mfrc522 import SimpleMFRC522
from status import statusPS1, statusPS2,statusPS3
import database 
import sqlite3
import dweepy


#initial setup
conn =sqlite3.connect('parking.db') #initialize database
cur= conn.cursor()
#ensure tables are empty for the new day
cur.execute("DELETE FROM moneyMade") 
cur.execute("DELETE FROM carP")
cur.execute("INSERT INTO moneyMade VALUES(0)")
#initialize and clear the lcd
lcd = CharLCD(i2c_expander='PCF8574', address=0x27,port=1,cols=16,rows=2, dotsize=8)
lcd.clear()
#ensure that DGmon dweet site exists for website read and its val is 0 for the new day
dweepy.dweet_for('DGmon',{'Money': 0})

#function for my rfid process
def rfid(mess,sOpen,l):
	reader = SimpleMFRC522() #initialize sensor
	while(True):
		#if no spots are available wait
		if(sOpen.value==0):
			while(sOpen.value==0):
				time.sleep(1)
		else:		
			id, text= reader.read() #read my rfid tag
			l.acquire() #lock display use
			lcd.clear()
			
			#checks if it is a new car and adds to the database
			if(database.checkCar(conn,id)==0):
				lcd.write_string('Welcome')
				arrInfo = (id,time.time())
				database.newCar(conn,arrInfo)
				
			#if it is not leaving procedure
			else:
				t=database.timeCar(conn,id) #time left
				owed=(time.time()-t)*0.25 #calc owed
				owed=round(owed,2) #to 2 decimals
				lcd.write_string('You owe: $'+str(owed))
				
				#update my database and dweet the new amount
				database.updateFin(conn,owed)
				mon = database.returnMon(conn)
				dweepy.dweet_for('DGmon',{'Money': mon})
				database.leaveCar(conn,id)
			#show message for 2 seconds
			time.sleep(2)
			lcd.clear()
			lcd.write_string(mess.value)
			l.release()#open display use
		
def pSpots(mess,sOpen,l):
	# all spots are open 
	currStatePs1=1 
	currStatePs2=1
	currStatePs3=1
	
	#set my shared memory for message to 3 on launch
	mess.value=("There are 3     spots available")
	l.acquire() #lock display
	lcd.clear()
	lcd.write_string("There are 3     spots available")
	l.release() #unlock display
	while(True):
		#check all the statuses and dweet these for website use
		statePs1=statusPS1(currStatePs1)
		statePs2=statusPS2(currStatePs2)
		statePs3=statusPS3(currStatePs3)
		dweepy.dweet_for('DGpark1',{'S1': statePs1})
		dweepy.dweet_for('DGpark2',{'S1':statePs2})
		dweepy.dweet_for('DGpark3',{'S1':statePs3})
		
		#add together for real time spots
		sOpenNow = statePs1 + statePs2 + statePs3
		
		#the previos val
		s=sOpen.value
		
		# if these are not equal something changed
		if(s != sOpenNow):
			sOpen.value =sOpenNow; #change this value in shared memory
			l.acquire() #lock display
			lcd.clear()
			
			#update display
			if(sOpenNow>1):
				mess.value = 'There are '+str(sOpen.value) + "     spots available"
				lcd.write_string(mess.value)
			elif sOpenNow==1:
				mess.value = 'There is '+str(sOpen.value) + "      spot available"
				lcd.write_string(mess.value)
			elif sOpenNow==0:
				mess.value = 'Parking is FULL'
				lcd.write_string(mess.value)
			l.release() #unlock display
		time.sleep(1)
	
def main():
	try:
		lock =Lock() #initialize lock
		manager=Manager() #initilaize manager for shared variable
		s=manager.Value('i', 3) #3 spots should be open
		smess=manager.Value('s',' ') #a string for shared memory
		rf = Process(target=rfid,args=(smess,s,lock)) #process for rfid sensor
		spots = Process(target=pSpots,args=(smess,s,lock)) #process monitor ps
		
		#start process
		rf.start() 
		spots.start()
		
		#join process
		rf.join()
		spots.join()
	except:
		conn.close() #if I get any exceptions which is usually databse ones close the datasbase to not get locked out


if __name__ == "__main__":
	main()
	

