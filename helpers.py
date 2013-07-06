from flask import request, Response, make_response, jsonify
from acl import port_permissions
from functools import wraps
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

def check_permission(relais, state):

    if not relais in port_permissions:
        log( "Switching on Relais %d to %r" % (relais, state) )
        return True
    
    auth = request.authorization
    if not auth:
        log("Relais %d needs permission. Not given." % (relais))
        return False

    for cred in port_permissions[relais]:
        if cred['user'] == auth.username and cred['pass'] == auth.password:
            log("Switching on Relais %d to %r (user=%s)" % (relais, state, auth.username))
            return True

    log("Relais %d needs permission. Credential check failed (user=%s)" % (relais, auth.username))

    return False

def format_output(data):

    format = request.args.get('format', 'json')

    if format == 'json':
        return jsonify(response=data)
    elif format == 'raw':

        if type(data) != list:
            data = [data]

        return ''.join(['1' if d is not False else '0' for d in data])
        
        
def output_handler(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            if isinstance(result, Response):
                return result

            return format_output(result)
        except Exception:
            return Exception.message, 404

    return decorator

