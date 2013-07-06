from flask import request, Response, make_response, jsonify
from settings import relay_permissions, relay_names
import syslog

enable_logging = True

syslog.openlog('webrelais')

def log(msg):

    if enable_logging:
        
        host = 'unknown'
        if request.remote_addr:
            msg = "[%s] %s" % (request.remote_addr, msg)

        syslog.syslog( syslog.LOG_INFO, msg )

def auth_required():

    resp = make_response("Not authenticated")
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Relays Access"'

    return resp

def check_permission(relay):

    if not relay in relay_permissions:
        return True
    
    auth = request.authorization
    if not auth:
        return False

    for cred in relay_permissions[relay]:
        if cred['user'] == auth.username and cred['pass'] == auth.password:
            return True

    return False

def relay_result(relay, status):

    name = 'Relay #'+str(relay)
    if relay in relay_names:
        name = relay_names[relay]

    auth = False
    if relay in relay_permissions:
        auth = True

    return {'id': relay, 'name': name, 'status': status, 'needs_auth': auth}

