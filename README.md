# Multifactor Authentication (MFA) for physical access control with Cisco Duo

This is a use case for using Cisco Duo APIs to bring Multifactor Authentication (MFA) to protect access control in different setup, this prototype uses a simple RFID reader on a Raspberry Pi to emulate the user experience.
When the user presents an RFID tag to the reader, the user will get a push notification from Cisco Duo to authorise the access before access is granted.

## Install

NOTE — please ensure both git and pip are installed in your environment by running the following command:
```
$ sudo apt-get -y install git python-pip
```


#### Clone the repo

```
$ git clone https://github.com/gve-sw/DNAC_usecase
```

#### Install dependencies

```
$ pip install pad4pi
$ pip install webexteamssdk
$ pip install duo_client
$ pip install mfrc522
$ pip install RPi.GPIO
```

## Software Setup

Before starting to play with this prototype you need to create accounts in Cisco Duo & Webex Teams and get the relevant credentials.

#### Duo

You can create a free account for 10 users at Duo, follow [this link](https://duo.com/pricing/duo-free) for details. For this project we are using the Duo Auth API, you can find documentation [here](https://duo.com/docs/authapi). The documentation will guide you through the creation of an application protection for our RFID client. Once created you can copy the application keys to export as environment variables.

```
$ export ikey='your  Integration key (DI...)'
$ export skey='your Secret key'
$ export host='your API hostname (api-....duosecurity.com)'
```

Create a user from the Duo admin panel, with the name 'test' this same username will be used in the RFID tag.

#### Webex Teams

You can create a free account in Webex Teams here. Once created you can follow the documentation here to create your first BOT, take note of the bot token as it will need to put it in an environment variable:

```
$ export WEBEX_TEAMS_ACCESS_TOKEN="Your webexteams bot token here"
```

Update duo_rfid.py with your own email address:

```python
		# Add people to the new demo room
		try:
			email_addresses = ["exmple@exmple.com"]
			for email in email_addresses:
			    api.memberships.create(demo_room.id, personEmail=email)
		except Exception as e:
			print(e)
```

## Hardware setup 

This project is run on a Raspberry Pi 3 model B with Raspbian OS. You can find documentation here on how to setup your Raspberry Pi. In addtion you will need the following:

- 3x LED (red, green, blue)
- 3x 100 resistance
- Raspberry Pi 4X4 Keypad
- Raspberry Pi RFID RC522 Reader
- RFID tags

#### Keypad 

The keypad used here is a 4x4, but you can use a 3x4 keypad by changing the keypad matrix. You can find [here](https://learn.adafruit.com/matrix-keypad/python-circuitpython) more details on the matrix and wiring .

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
You can test your keypad using the [keypadtest.py](./keypadtest.py) file.

#### RFID 

The RFID reader used in this project is the common RC522. Uou can use [rfidwrite.py](./rfidwrite.py) file and [rfidread.py](./rfidread.py) to write the username in your RFID tags. Follow [this tutorial](https://medium.com/coinmonks/for-beginners-how-to-set-up-a-raspberry-pi-rfid-rc522-reader-and-record-data-on-iota-865f67843a2d) for more details.

Please make sure that the username you are writing on the RFID is the same user you created in your Duo account.

#### Leds

Leds will show notifications of what is happening with the demo, and here is how to read those. Leds need to be wired.

* Green blinking : access granted 
* Red blinking : access denied
* Blue blinking : timeout, use the keypad for pin


#### Wiring

![Wiring photo][wiring]

[wiring]:./wiring.jpg "Wiring photo"


## Usage

run [duo_rfid.py](./duo_rfid.py)

```
$ python duo_rfid.py 
Hold a tag near the reader
```

Note: please make sure to update the keys for Duo in the code and export a variable for the Webex Teams token.

### Demo scenarios

![Diagram flow photo][flow]

[flow]:./flow.jpg "Diagram flow photo"

#### Standard login scenario with Duo app

1. User puts the RFID tag on the reader 
2. User approves the Duo authorisation notification 
3. User is granted access

#### New user enrollment

1. User presents a new RFID tag to reader
2. User is not granted access
3. Enrollment process is sent over Webex Teams for new user

#### Timeout Duo auth, PIN code login 

1. User puts the RFID tag on the reader 
2. Duo autorisation does NOT happen (timeout, connectivity...)
3. Pin is generated and sent through Webex Teams
3. User is granted access using a PIN code

### Video

<a href="http://www.youtube.com/watch?feature=player_embedded&v=NgMu5lcIi9Y
" target="_blank"><img src="http://img.youtube.com/vi/NgMu5lcIi9Y/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
