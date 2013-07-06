door_credentials = {'user':'username', 'pass':'password'}
user_credentials = {'user':'john', 'pass': 'doe'}


relay_permissions = {
    0: [door_credentials],
    1: [door_credentials],
    2: [door_credentials]
}

relay_cards = [
    {'serial': 'A702FJ36', 'start': 0, 'relays': 8},
    {'serial': 'A702FIL4', 'start': 8, 'relays': 8},
]

relay_names = {
    0: 'Door open',
    1: 'Door close',
    2: 'Door buzzer',
    3: 'Exitlight white',
    4: 'Exitlight red',
    5: 'Alarmlight',
    6: 'Heater'
}

