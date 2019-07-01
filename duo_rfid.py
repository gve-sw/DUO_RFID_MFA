#!/usr/bin/env python


#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
import os
import duo_client
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
from pad4pi import rpi_gpio
import time
import random
from webexteamssdk import WebexTeamsAPI



api = WebexTeamsAPI()

entered_passcode = ""
correct_passcode = "1234"
passcode_status  = False
number_of_tries  = 0

GPIO.setmode(GPIO.BCM)
# Setup Keypad
KEYPAD = [
		["1","2","3","A"],
		["4","5","6","B"],
		["7","8","9","C"],
		["*","0","#","D"]
]

# same as calling: factory.create_4_by_4_keypad, still we put here fyi:
ROW_PINS = [5, 13, 19, 26] # BCM numbering
COL_PINS = [12, 16, 20, 21] # BCM numbering

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
#keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

rfid_reader = SimpleMFRC522()

def get_webexteams_room(room_title='MFA RFID access'):
		all_rooms = api.rooms.list()

		demo_rooms = [room for room in all_rooms if room_title in room.title]

		# Delete all of the demo rooms
		#for room in all_rooms:
		#	print(room.title)
		#   api.rooms.delete(room.id)

		# Create a new demo room
		if not demo_rooms:
			demo_room = api.rooms.create(room_title)
		else:
			demo_room = demo_rooms[0]

		print(demo_room.id)
		# Add people to the new demo room
		try:

			email_addresses = ["exmple@exmple.com"]
			for email in email_addresses:
			    api.memberships.create(demo_room.id, personEmail=email)
		except Exception as e:
			print(e)

		return demo_room

def send_enrolement_to_webexteams(enrolement_url,user):
	# Find all rooms that have 'webexteamssdk Demo' in their title
	try:

		demo_room=get_webexteams_room('MFA RFID access')
		# Post a message to the new room, and upload a file
		api.messages.create(demo_room.id, text="New user : **"+user+"** enrolement link : "+enrolement_url)

		return True
	except Exception as e:
		print(e)
		return False


def send_pin_to_webexteams(correct_passcode,user):
	# Find all rooms that have 'webexteamssdk Demo' in their title
	try:

		demo_room=get_webexteams_room('MFA RFID access')
		# Post a message to the new room, and upload a file
		api.messages.create(demo_room.id, text="Genrtaed pin passcode for User "+user+" : "+correct_passcode)

		return True
	except Exception as e:
		print(e)
		return False



def duo_auth(user):
	# Configuration and information about objects to create.
	#TODO put these to env variables
	auth_api = duo_client.Auth(
		ikey=os.environ['ikey'],
		skey=os.environ['skey'],
		host=os.environ['host'],
	)

	# Retrieve user info from API:
	ping_result = auth_api.ping()

	print('ping result :' + json.dumps(ping_result)) 


	# Retrieve user info from API:
	preauth_result = auth_api.preauth(username=user)

	print('preauth result :' + json.dumps(preauth_result)) 



	# Retrieve user info from API:
	if preauth_result['result']=='auth':
		auth_result = auth_api.auth(username=user,factor='push',device='auto')
	elif preauth_result['result']=='enroll':
		r=send_enrolement_to_webexteams(preauth_result['enroll_portal_url'],user)
		status='enroll'
		return status
	else:
		print(preauth_result['status_msg'])
		status='error' #TODO  do enrole here and send enrolment process over webex (see json response for unrecongnized user)
		return status

	print('auth result :'+ json.dumps(auth_result)) 
	if auth_result['status']:
		status= auth_result['status']
	else:
		status= "error"


	return status


def set_gpio():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False) # Ignore warning for now
	#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
	GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off) allow green 
	GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off) denny red
	GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off) passcode blue

def blink_led(LED_PIN,number_of_blinks):
	#GPIO.setmode(GPIO.BCM)
	for i in range(number_of_blinks): # Run forever
		GPIO.output(LED_PIN, GPIO.HIGH) # Turn on
		sleep(0.2) # Sleep for 1 second
		GPIO.output(LED_PIN, GPIO.LOW) # Turn off
		sleep(0.2) # Sleep for 1 second





def correct_passcode_entered():
	global passcode_status,entered_passcode 
	print("Passcode accepted. Access granted.")
	passcode_status=True
	entered_passcode = ""

def incorrect_passcode_entered():
	global number_of_tries,entered_passcode
	print("Incorrect passcode. try again !")
	entered_passcode = ""
	number_of_tries+=1
	blink_led(18,1)	
	#cleanup()
	#sys.exit()

def digit_entered(key):
	global entered_passcode, correct_passcode

	entered_passcode += str(key)
	print(entered_passcode)
	blink_led(14,1)

	if len(entered_passcode) == len(correct_passcode):
		if entered_passcode == correct_passcode:
			correct_passcode_entered()
		else:
			incorrect_passcode_entered()

def non_digit_entered(key):
	global entered_passcode

	if key == "*" and len(entered_passcode) > 0:
		entered_passcode = entered_passcode[:-1]
		print(entered_passcode)

def key_pressed(key):
	try:
		int_key = int(key)
		if int_key >= 0 and int_key <= 9:
			digit_entered(key)
	except ValueError:
		non_digit_entered(key)

def keypad_input():
	global passcode_status,number_of_tries

	try:



		keypad.registerKeyPressHandler(key_pressed)


		print("Enter your passcode (hint: {0}).".format(correct_passcode))
		print("Press * to clear previous digit.")

		while (not passcode_status) and (number_of_tries<4):

			time.sleep(1)
			if number_of_tries==3:
				print("mas tries exceeded")
				return False

		return True
	except Exception as e:
		print(e)
		return False
	finally:
		#resetvalues
		passcode_status=False
		number_of_tries=0
		entered_passcode = ""
		keypad.unregisterKeyPressHandler(key_pressed)
		set_gpio() #issue with the cleanup of keybord


	

if __name__ == '__main__':

	
	set_gpio() #issue with the cleanup of keybord
	try:
		while True:
			print("Hold a tag near the reader")
			id, user = rfid_reader.read()
			print(id)
			print(user)
			r=duo_auth(user)
			if r=="allow":
				print('loging authorised !')
				blink_led(14,3)
			elif r=="deny":
				print('loging denied !')
				blink_led(18,3)	
			elif r=='enroll':
				print('New user enrolement process sent to webex!')
				blink_led(18,3)
			else: #fall back to PIN code using keypad
				print('login fialed !')
				blink_led(23,3)
				print("enter passcode")
				#genrate passcode and send it to webexteams
				correct_passcode=str(random.randint(1000,9999))
				r=send_pin_to_webexteams(correct_passcode,user)
				r=keypad_input()
				if r==True:
					print('loging authorised !')
					blink_led(14,3)
				elif r==False:
					print('loging denied !')
					blink_led(18,3)				

	finally:

		keypad.cleanup()
		GPIO.cleanup()