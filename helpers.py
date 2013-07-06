from flask import request, Response, make_response, jsonify
from settings import port_permissions, relais_names
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
    resp.headers['WWW-Authenticate'] = 'Basic realm="Relais Access"'

    return resp

def check_permission(relais):

    if not relais in port_permissions:
        return True
    
    auth = request.authorization
    if not auth:
        return False

    for cred in port_permissions[relais]:
        if cred['user'] == auth.username and cred['pass'] == auth.password:
            return True

    return False

def relais_result(pin, status):

    name = 'Pin #'+str(pin)
    if pin in relais_names:
        name = relais_names[pin]

    auth = False
    if pin in port_permissions:
        auth = True

    return {'id': pin, 'name': name, 'status': status, 'needs_auth': auth}

