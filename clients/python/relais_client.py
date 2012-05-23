__author__ = 'schinken'

import urllib2
import json

class restlib2(urllib2.Request):

    """ Workaround for using DELETE with urllib2
        Thanks to: http://abhinandh.com/post/2383952338/making-a-http-delete-request-with-urllib2
    """

    def __init__(self, url, method, data=None, headers={}, origin_req_host=None, unverifiable=False):
        self._method = method
        urllib2.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)

    def get_method(self):

        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)


class RelaisClient(object):

    host = ''

    get = 'GET'
    set = 'POST'
    reset = 'DELETE'

    def __init__(self, host, port=80):
        self.host = "http://%s:%s" % (host, port)

    def sendCommand(self, path, type ):

        try:
            req = restlib2( self.host+path, type )
            f = urllib2.urlopen( req )
        except ValueError:
            raise Exception('Unable to fulfill request')

        try:
            return json.load(f)
        except ValueError:
            raise Exception('Unable to parse result')

    def setPort(self, port, value=1 ):

        if not value:
            return self.resetPort( port )

        return self.sendCommand( "/ports/%d" % port, self.set )

    def setPorts(self, value=1 ):

        if not value:
            return self.resetPorts()

        return self.sendCommand("/ports", self.set )


    def resetPort(self, port):
        return self.sendCommand( '/ports/%d' % port, self.reset )

    def resetPorts(self):
        return self.sendCommand( '/ports', self.reset )


    def getPort(self, port):
        return self.sendCOmmand( '/ports/%d' % port, self.get )


    def getPorts(self):
        return self.sendCommand( '/ports', self.get )


if __name__ == '__main__':

    rc = RelaisClient(host='localhost', port=5000)
    print rc.getPorts()