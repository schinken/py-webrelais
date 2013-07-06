
# host is optional
door_credentials = {'user':'username', 'pass':'password'}
user_credentials = {'user':'john', 'pass': 'doe'}


port_permissions = {}

port_permissions[0] = [door_credentials]
port_permissions[1] = [door_credentials]
port_permissions[2] = [door_credentials, user_credentials]
port_permissions[3] = [user_credentials]
