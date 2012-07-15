from flask import request, make_response, jsonify
from acl import port_permissions
from functools import wraps

def auth_required():

    resp = make_response("Not authenticated")
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Relais Access"'

    return resp

def check_permissions(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):

        if not 'port' in kwargs:
            return fn(*args, **kwargs)

        port = kwargs['port']
        auth = request.authorization

        # check if there are special port credentials, and if
        # validate them
        if not port in port_permissions:
            return fn(*args, **kwargs)

        for cred in port_permissions[port]:
            if auth and cred['user'] == auth.username and cred['pass'] == auth.password:
                if ('host' in cred and cred['host'] == request.remote_addr) or 'host' not in cred:
                    return fn(*args, **kwargs)
        
        return auth_required()

    return decorator

def format_output( data ):

    format = request.args.get('format', 'json')

    if format == 'json':
        return jsonify( response=data )
    elif format == 'raw':

        if type(data) != list:
            data = [data]

        return ''.join([ '1' if d is not False else '0' for d in data ])
        
        
def output_handler(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            return format_output( fn(*args, **kwargs) )
        except Exception:
            return Exception.message, 404

    return decorator

