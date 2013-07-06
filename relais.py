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


if __name__ == '__main__':
    
    import time

    sainsmart_usb0 = SainSmart('A702FJ36')
    sainsmart_usb1 = SainSmart('A702FIL4')

    relais0 = Relais(sainsmart_usb0)
    relais1 = Relais(sainsmart_usb1)

    for z in xrange(2):
        for n in xrange(8):
            relais0.toggle_pin(n)
            relais1.toggle_pin(n)
            time.sleep(0.1)
