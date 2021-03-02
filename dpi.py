from gpiozero import LED
from gpiozero import MotionSensor
from datetime import datetime
from time import sleep
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


blue_led = LED(17)
green_led = LED(27)
red_led = LED (22)
s_led = LED(26)
pir = MotionSensor(23)
blue_led.on()
red_led.off()
green_led.off()

Detected="Motion Detected"
Stopped="Motion Stopped"

connection = mysql.connector.connect(host='localhost', database='RaspberryPI', user='test', password='password')
cursor=connection.cursor()

while True:
	try:
		cursor=connection.cursor()
		pir.wait_for_motion()
		print Detected
		now = datetime.now()
		now = now.strftime("%Y-%m-%d %H:%M:%S")
		print now
		sleep(0.1)
		red_led.on()
		blue_led.off()
		green_led.off()

		mysql_insert_query = """INSERT INTO Motion (detected,date_time) VALUES (%s,%s)"""
		records=(Detected,now)
		cursor.execute(mysql_insert_query,records)
		connection.commit()
		print("Success\n")
	except mysql.connector.Error as error:
		print("Failed\n")

	try:
		pir.wait_for_no_motion()
		print Stopped
		now = datetime.now()
		now = now.strftime("%Y-%m-%d %H:%M:%S")
		print now
		sleep(0.1)
		red_led.off()
		blue_led.off()
		green_led.on()

		mysql_insert_query = """INSERT INTO Motion (stopped,date_time) VALUES (%s,%s)"""
		records=(Stopped,now)
		cursor.execute(mysql_insert_query,records)
		connection.commit()
		print("Success\n")
	except mysql.connector.Error as error:
		print("Failed\n")
