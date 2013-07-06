door_credentials = {'user':'username', 'pass':'password'}
user_credentials = {'user':'john', 'pass': 'doe'}


port_permissions = {}

port_permissions[0] = [door_credentials]
port_permissions[1] = [door_credentials]
port_permissions[2] = [door_credentials, user_credentials]
port_permissions[3] = [user_credentials]


relais_cards = [
    {'serial': 'A702FJ36', 'start': 0, 'relais': 8},
    {'serial': 'A702FIL4', 'start': 8, 'relais': 8},
]
