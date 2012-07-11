__author__ = 'schinken'

import parallel

class Parport(object):

    conn = None
    data = 0x00

    def __init__(self):
#        self.conn = parallel.Parallel()
        self.setPort()

    def setPin(self, pin=None, value=1):

        if pin is None:
            if value:
                return self.setPins()
            else:
                return self.resetPins()

        if pin > 7 or pin < 0:
            raise Exception('PortPin is out of range')

        if value:
            self.data |= ( 0x01 << pin )
        else:
            self.data &= ~( 0x01 << pin )

        self.setPort()

    def setPins(self):

        self.data = 0xFF
        self.setPort()

    def togglePin(self, pin ):

        val = self.getPin( pin )

        if val:
            self.setPin( pin, 0 )
        else:
            self.setPin( pin, 1 )

    def getPin(self, pin=None):
        if pin is None:
            return self.getPins()

        if self.data & ( 0x01 << pin ):
            return True
        else:
            return False

    def getPins(self):

        pins = []
        for pin in range(8):
            pins.append( self.getPin( pin ) )

        return pins

    def resetPin(self, pin=None):
        if pin is None:
            return self.resetPins()

        self.setPin(pin, 0)

    def resetPins(self):
        self.data = 0x00
        self.setPort()

    def setPort(self):
#        self.conn.setData( self.data )
        pass
