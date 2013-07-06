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

class Relais:

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

    def set_pin(self, pin, value):
        self.state[pin] = value
        self._update()

    def set_pins(self, value):
        self.state = [value]*8
        self._update()

    def get_pin(self, pin):
        return self.state[pin]

    def get_pins(self):
        return self.state

    def toggle_pin(self, pin):
        self.state[pin] = not self.state[pin]
        self._update()

class RelaisProxy:

    relais = []
    pin_to_relais = {}

    def add_relais(self, offset, num_relais, relais):
        cur_offset = len(self.pin_to_relais)

        for pin in xrange(offset, offset+num_relais):
            self.pin_to_relais[pin] = (relais, pin-cur_offset)

        self.relais.append(relais)

    def set_pin(self, pin, value):
        relais, pin = self.pin_to_relais[pin]
        relais.set_pin(pin, value)

    def get_pin(self, pin):
        relais, pin = self.pin_to_relais[pin]
        return relais.get_pin(pin)

    def get_pins(self):
        result = []
        for relais in self.relais:
            result = result + relais.get_pins()

        return result

    def toggle_pin(self, pin):
        relais, pin = self.pin_to_relais[pin]
        relais.toggle_pin(pin)

    def num_relais(self):
        return len(self.pin_to_relais)
