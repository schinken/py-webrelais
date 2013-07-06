import pylibftdi
#import parallel

class SainSmart:

    def __init__(self, serial):
        self.device = pylibftdi.BitBangDevice(serial)
        self.device.direction = 0xFF

    def update(self, byte):
        self.device.port = byte

class ParPort:

    def __init__(self):
        self.device = parallel.Parallel()
    
    def update(self, byte):
        self.conn.setData(byte)

class Relay:

    def __init__(self, delegate):
        self.delegate = delegate
        self.state = [False]*8
        self._update()

    def _update(self):

        result = 0x00
        for i, val in enumerate(self.state[:8]):
            if val:
                result |= (1 << i)
            else:
                result &= ~(1 << i)

        self.delegate.update(result)

    def set_relay(self, relay, value):
        self.state[relay] = value
        self._update()

    def set_relays(self, value):
        self.state = [value]*8
        self._update()

    def get_relay(self, relay):
        return self.state[relay]

    def get_relays(self):
        return self.state

    def toggle_relay(self, relay):
        self.state[relay] = not self.state[relay]
        self._update()

class RelaysProxy:

    relais = []
    pin_to_relais = {}

    def add_relay(self, offset, num_relais, relais):
        cur_offset = len(self.pin_to_relais)

        for relay in xrange(offset, offset+num_relais):
            self.pin_to_relais[relay] = (relais, relay-cur_offset)

        self.relais.append(relais)

    def set_relay(self, relay, value):
        relais, id = self.pin_to_relais[relay]
        relais.set_relay(id, value)

    def get_relay(self, relay):
        relais, id = self.pin_to_relais[relay]
        return relais.get_relay(id)

    def get_relays(self):
        result = []
        for relais in self.relais:
            result = result + relais.get_relays()

        return result

    def toggle_relay(self, relay):
        relais, id = self.pin_to_relais[relay]
        relais.toggle_relay(id)

    def num_relais(self):
        return len(self.pin_to_relais)
