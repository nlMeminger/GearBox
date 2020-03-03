import media_control as mc

class BtDevice:

    #Define the attributes:
    macAddress = ''
    deviceName = ''
    bluezPlayer = None

    def __init__(self, macAddress = '', deviceName = '', bluezPlayer = None):
        self.macAddress = macAddress
        self.deviceName = deviceName
        self.bluezPlayer = bluezPlayer

    def connectToPlayer(self):
        if self.macAddress == '':
            print('No mac address specified')
        elif (':' in self.macAddress) and (self.bluezPlayer is not None):
            try:
                self.bluezPlayer = mc.mediaControl(self.macAddress)
            except Exception as e:
                print(e)
        elif self.bluezPlayer is None:
            print('A bluez player has already been established')
        else:
            print('Something went wrong trying to connect to the bluetooth player')


