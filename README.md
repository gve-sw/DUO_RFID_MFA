# MFA for physical access controle with CISCO DUO
This is a use case for using CISCO DUO APIs to bring Multifactor Authentication to protect access controle in difrent setup, this prototype uses a simple RFID reader on a RaspberyPI to emulate the user experiance.
When the user would present an RFID tage to the reader, the user will get a push notification from CISCO DUO to authorise the access befeore access is granted.


## Install:

#### Clone the repo :
```
$ git clone https://github.com/gve-sw/DNAC_usecase
```

#### Install dependencies :

```
$ pip install pad4pi
$ pip install webexteamssdk
$ pip install duo_client
$ pip install mfrc522
$ pip install RPi.GPIO
```

## software Setup:

Before starting to play with this prototype you need to create accounts in CISCO DUO & WebExTeams and get the relevent credentials:
#### DUO  :
you can create a free account for 10 users at duo, follow [this](https://duo.com/pricing/duo-free) link for details, for this project we are using the DUO Auth API, you can find documentation [here](https://duo.com/docs/authapi), the documentation will guide you through the creation of an application protection for our RFID client, once created you can copy the application keys to export as envirenemnt variables.

```
$ export ikey='your  Integration key (DI...)'
$ export skey='your Secret key'
$ export host='your API hostname (api-....duosecurity.com)'
```
Create a user from the DUO admin panel, with the name 'test' this same username will be used in the RFID tag


#### webex :
you can create a free account in webexteams here, once created you can follow the documentation here to create your first BOT, take note of the bot token as it will need to put it in an envirenemnt variable:
```
$ export WEBEX_TEAMS_ACCESS_TOKEN="Your webexteams bot token here"
```
update the code with your email address:
```python
		# Add people to the new demo room
		try:
			email_addresses = ["exmple@exmple.com"]
			for email in email_addresses:
			    api.memberships.create(demo_room.id, personEmail=email)
		except Exception as e:
			print(e)
```

## hardware setup 

this project is run on a Raspbery pi 3 model B with the Rasbian os, you can find domcnyation here on how to setup your raspberry pi, in addtion you will need the folwing :
- 3 LED (red,green,blue)
- 3 100 resistance
- Raspberry Pi 4X4 Keypad
- Raspberry Pi RFID RC522 Reader
- RFID tags

#### keypad 
the keypad used here is a 4x4 you can use a 3x4 keypad by change the keypad matrix, you can find [here](https://learn.adafruit.com/matrix-keypad/python-circuitpython) more details on teh matrix and wiring 
```python
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
```
you can test your keypad using keypadtest.py

#### RFID 
the RFID reader used in this project is very comun RC522, you can use [rfidwrite.py](./rfidwrite.py) file and [rfidread.py](./rfidread.py)  to write the username in your rfid tags, follow this tutorial for more details [here](https://medium.com/coinmonks/for-beginners-how-to-set-up-a-raspberry-pi-rfid-rc522-reader-and-record-data-on-iota-865f67843a2d 

make sure that the  username you are writing on the rfid is the same user you created in your DUO account.

#### leds 
the leds are showing notifications of what is hapning with the demo here is how to read those, the leds need to be wired 
Green blinking : access granted 
Red blinking : Access denied
Blue blinking : timout, use the keypad for pin


#### wireing

![Wiring photo][wiring]

[wiring]:./wiring.jpg "Wiring photo"


## Usage:

run [duo_rfid.py](./duo_rfid.py) :
```
$ python duo_rfid.py 
Hold a tag near the reader
```
note: make sure to update the keys for DUO in the code and export a variable for webexteams token.

### demo scneraos :
![Diagram flow photo][flow]

[flow]:./flow.jpg "Diagram flow photo"

#### standrad loging scenario with DUO app
1. user put the rfid tag to the reader 
2. user approve the DUO authorisation notification 
3. user is grandted access
#### enrolement of new user
1. user presnt a new rfid tag to reader
2. user is not grandted access
3. Enrollemnt process is sent over webexteams for new user
#### timout Duo auth, PIN code login 
1. user put the rfid tag to the reader 
2. DUO autorisation dosent happen (timout, connectivity ...)
3. pin is genrated and sent trough webexteams
3. user is grandted access using a PIN code

### Video :

<a href="http://www.youtube.com/watch?feature=player_embedded&v=NgMu5lcIi9Y
" target="_blank"><img src="http://img.youtube.com/vi/NgMu5lcIi9Y/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>


