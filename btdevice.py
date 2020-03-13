import media_control as mc

import dbus
import bluetooth
import time

class BtDevice:

    #Define the attributes:
    macAddress = ''
    deviceName = ''
    bluetoothPort = 1
    player = None
    bluetoothSocket = None
    bluezInterface = None
    controlerPropertiesInterface = None
    playerPropertiesInterface = None
    systemBus = None
    playerPath = ''
    songInfo = {}

    def __init__(self, macAddress = '', deviceName = ''):
        self.macAddress = macAddress
        self.deviceName = deviceName

        if macAddress == '':
            print('Invalid mac format: cannot be empty')
        elif deviceName == '':
            print('retrieving device name:')

        try:
            self.connectDevice()
            self.systemBus = dbus.SystemBus()
            self.connectToInterface()
            time.sleep(1)
            self.connectToPlayer

        except Exception as e:
            print (e)


    def connectToPlayer(self):
        self.getPlayerPath()
        self.player = self.systemBus.get_object('org.bluez', self.playerPath)
        self.playerPropertiesInterface = dbus.Interface(self.player, "org.freedesktop.DBus.Properties")
    
    def connectToInterface(self):
        intPath = "/org/bluez/hci0/dev_{}".format(self.macToDbus(self.macAddress))
        self.bluezInterface = self.systemBus.get_object('org.bluez', intPath)
        self.bluezInterface.Connect(dbus_interface='org.bluez.Device1')
        self.controlerPropertiesInterface = dbus.Interface(self.bluezInterface, "org.freedesktop.DBus.Properties")
        

    def getPlayerPath(self):
        self.playerPath =  str(self.controlerPropertiesInterface.Get( 'org.bluez.MediaControl1', 'Player'))

    def macToDbus(self, mac):
        if ':' not in mac or len(mac) != 17:
            print('invalid format')
            return
        else:
            mac = mac.replace(':', '_')
            return mac


    def connectDevice(self):
        self.bluetoothSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.bluetoothSocket.connect((self.macAddress, self.bluetoothPort))

    def disconnectDevice(self):
        pass

    
    def play(self):
        try:
            self.player.Play(dbus_interface='org.bluez.MediaPlayer1')
        except dbus.exceptions.DBusException as e:
            ##print(e)
            self.connectToPlayer()
            self.player.Play(dbus_interface='org.bluez.MediaPlayer1')
        except AttributeError:
            print('no player')
            self.connectToPlayer()
            return
        
    def pause(self):
        try:
            self.player.Pause(dbus_interface='org.bluez.MediaPlayer1')
        except dbus.exceptions.DBusException as e:
            #print(e)
            self.connectToPlayer()
            self.player.Pause(dbus_interface='org.bluez.MediaPlayer1')
        except AttributeError:
            print('no player')
            self.connectToPlayer()
            return
        
    def next(self):
        '''
        Skip to the next track
        '''

        try:
            self.player.Next(dbus_interface='org.bluez.MediaPlayer1')
        except dbus.exceptions.DBusException as e:
            #print(e)
            self.connectToPlayer()
            self.player.Next(dbus_interface='org.bluez.MediaPlayer1')
        except AttributeError:
            return
        
    def previous(self):
        '''
        Skip to previous track
        sends to begining of track in some players, and must double previous to actually return to previous track.
        '''

        try:
            self.player.Previous(dbus_interface='org.bluez.MediaPlayer1')
        except dbus.exceptions.DBusException as e:
            #print(e)
            self.connectToPlayer()
            self.player.Previous(dbus_interface='org.bluez.MediaPlayer1')
        except AttributeError:
            return
        
    def stop(self):
        '''
        Stop the music
        '''
        try:
            self.player.Stop(dbus_interface='org.bluez.MediaPlayer1')
        except dbus.exceptions.DBusException as e:
            #print(e)
            self.connectToPlayer()
            self.player.Stop(dbus_interface='org.bluez.MediaPlayer1')
        except AttributeError:
            return
        
    def getSongInfo(self):
        try:
            
            self.songInfo = self.playerPropertiesInterface.Get("org.bluez.MediaPlayer1", 'Track')
            print('\n' + 'Song info:' + self.songInfo + '\n')
            return self.songInfo
        except dbus.exceptions.DBusException as e:
            self.connectToPlayer()
            ##print(e)
        


    def getTrackName(self):
        '''
        Get the name of the currently playing track
        Returns a string with the name of the track
        '''
        return self.songInfo['Title']

    def getAlbumName(self):
        '''
        Get the name of the album currently playing
        Returns a string with the album name
        '''

        return self.songInfo['Album']

    def getArtistName(self):
        '''
        Get the name of the artist currently playing
        Returns a string with the name of the artist
        '''
        return self.songInfo['Artist']


    def getDuration(self):
        '''
        Get the duration of the currently playing song in miliseconds
        Returns and integer containing the length of the song.
        '''
        return int(self.songInfo['Duration'])

    def getPosition(self):
        '''
        Get the current position of the song in miliseconds
        Returns an int
        '''
        return int(self.playerPropertiesInterface.Get("org.bluez.MediaPlayer1", 'Position'))

    def isPlaying(self):
        '''
        Get the status of if the song is playing or not
        Returns a bool containing the status of the song.
        If the status is unknown, the function automatically returns false.
        '''
        status = None
        try:
            status = self.playerPropertiesInterface.Get("org.bluez.MediaPlayer1", 'Status')
        except AttributeError:
            self.connectToPlayer()
            return False

        if status == "playing":
                return True
        elif status == "paused":
            return False
        elif status == "stopped":
            return True
        else:
            return False

    def shuffle(self, state):
        '''
        Set the shuffle state
        Expects a bool to determine the shuffle state
        '''
        if state == True:
            self.playerPropertiesInterface.Set("org.bluez.MediaPlayer1", "Shuffle", "alltracks")
        elif state == False:
            self.playerPropertiesInterface.Set("org.bluez.MediaPlayer1", "Shuffle", "off")

    def getShuffle(self):
        '''
        Determine if the music is shuffled or not.
        Returns a bool
        '''		
        shuffleState = self.playerPropertiesInterface.Get("org.bluez.MediaPlayer1", "Shuffle")

        if shuffleState == "alltracks":
            return True
        elif shuffleState == "group":
            return True
        elif shuffleState == "off":
            return False

    def repeat(self, state):
        '''
        Control the repeat functionality of the bluetooth audio player
        Expects an int to determine the state
        valid inputs are 0: off, 1: all tracks, or 2: single track.
        '''
        if state == 0:
            self.playerPropertiesInterface.Set("org.bluez.MediaPlayer1", "Repeat", "off")
        elif state == 1:
            self.playerPropertiesInterface.Set("org.bluez.MediaPlayer1", "Repeat", "alltrack")	
        elif state == 2:
            self.playerPropertiesInterface.Set("org.bluez.MediaPlayer1", "Repeat", "singletrack")

    def getRepeat(self):
        '''
        Get the status of the repeat loop
        Returns an integer with the following possible values
        0: off, 1: all tracks, or 2: single track.
        '''
        repeatState = self.playerPropertiesInterface.Get("org.bluez.MediaPlayer1", "Repeat")

        if repeatState == "off":
            return 0
        elif repeatState == "alltrack":
            return 1
        elif repeatState == "singletrack":
            return 2


#    def shuffle(self, state):
#        '''
#        Set the shuffle state
#        Expects a bool to determine the shuffle state
#        '''
#        if state == True:
#            self.playerPropertiesInterface.Set("org.bluez.MediaPlayer1", "Shuffle", "alltracks")
#        elif state == False:
#            self.playerPropertiesInterface.Set("org.bluez.MediaPlayer1", "Shuffle", "off")
#