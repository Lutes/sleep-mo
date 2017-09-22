import RPi.GPIO as GPIO
import time
import datetime
from shutil import copyfile

#Set GPIO Mode
GPIO.setmode(GPIO.BCM)

#GPIO Pins
SWITCH = 4
MSENSOR = 21

#Set up switch pin 
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Set up motion sensor
GPIO.setup(MSENSOR, GPIO.IN)

# Don't terminate
while True:
    is_not_on = GPIO.input(SWITCH)
    motion_count = 0
    motion_array = []
    current_minute = datetime.datetime.now().minute
    time.sleep(1)
    #If motion sensor is on
    while (is_not_on == False):
        time.sleep(1)
    	# If a minute has passed
    	if current_minute != datetime.datetime.now().minute:
    		motion_array.append([motion_count , int(time.time())])
    		motion_count = 0
    		current_minute = datetime.datetime.now().minute

    	# If motion sensor is triggered
    	if GPIO.input(MSENSOR):
    		motion_count += 1
                print("MO")
    		time.sleep(3)

    	# See if user has turned off motion sensor
    	is_not_on = GPIO.input(SWITCH)

    	# If user turned off the motion sensor export sleep data to file
    	if is_not_on:
    		# Create json file and write motion data
    		f = open('today.json', 'w+')
    		f.write("{\n " + str(motion_array) + " \n}")
    		f.close()

    		# Create a copy of the file written from before, file name is todays date
    		today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    		copyfile('today.json', today_date + ".json")

    		# Print data for testing
    		print("{\n " + str(motion_array) + " \n}")

    		# Reset data
    		motion_array = []
    		motion_count = 0



    	



