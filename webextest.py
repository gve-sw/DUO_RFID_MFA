from webexteamssdk import WebexTeamsAPI

#export WEBEX_TEAMS_ACCESS_TOKEN="ZjE1YTgwOTEtNjI3Ny00NDRlLWI3MWItNTY0M2JjNzQwYmZmMmNiYzVjZjgtZmQ2_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"

api = WebexTeamsAPI()

# Find all rooms that have 'webexteamssdk Demo' in their title
all_rooms = api.rooms.list()
#demo_rooms = [room for room in all_rooms if 'webexteamssdk Demo' in room.title]

# Delete all of the demo rooms
for room in all_rooms:
	print(room.title)
    #api.rooms.delete(room.id)

# Create a new demo room
demo_room = api.rooms.create('webexteamssdk Demo')

# Add people to the new demo room
email_addresses = ["agabdelb@cisco.com"]
for email in email_addresses:
    api.memberships.create(demo_room.id, personEmail=email)

# Post a message to the new room, and upload a file
api.messages.create(demo_room.id, text="Welcome to the room!")