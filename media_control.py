'''
Tkinter GUI front-end for open source car stereo project
Made by Red in 2019
Greetings, from the ROC!

https://github.com/nlMeminger/MagiCarp

This code is licensed under the GNU General Public License
For more information see the LICENSE file that was distributed with this code
Or visit https://www.gnu.org/licenses/gpl-3.0.en.html
'''

import dbus

bus = dbus.SystemBus() #open the dbus system bus.

class mediaControl:
	'''
	Media control class
	To create a media control device you must pass a bluetooth mac address when you first call it.
	'''
	
	def __init__(self, mac_address):
		'''
		Initialize the media control device
		'''
		dbusDeviceAddress = self.mac_to_dbus(mac_address) #Take the mac address and convert it to the dbus device name.
		self.mediaDevice = bus.get_object('org.bluez', "/org/bluez/hci0/" + dbusDeviceAddress + "/player0") #Define the bluez media class player device.
		self.interface = dbus.Interface(self.mediaDevice, "org.freedesktop.DBus.Properties") #Define the interface to be able to get properties for album info

	def mac_to_dbus(self, mac_address):
		'''
		Convert a standard colon sepatated mac address to a dbus device name. Prepends dev_ and converts the colons to underscores.
		Takes a string for the bluetooth device mac address
		Returns a string containing the dbus device name.
		'''

		#Error handling
		if ":" not in mac_address:
			raise ValueError("mac_address does not appear to be a valid mac address")
		if len(mac_address) != 17:
			raise ValueError("mac_address does not appear to be a valid mac address")


		dbusDevice = "dev_"
		for char in mac_address: #For character in the mac address
			if char == ":":
				dbusDevice += "_" #Convert : to _
			else:
				dbusDevice += char
		return dbusDevice


		'''
		Music control functions do not return anything
		'''
	def pause(self):
		'''
		Pause the music
		'''
		self.mediaDevice.Pause(dbus_interface="org.bluez.MediaPlayer1")

	def play(self):
		'''
		Play the music
		'''
		self.mediaDevice.Play(dbus_interface="org.bluez.MediaPlayer1")

	def next(self):
		'''
		Skip to the next track
		'''
		self.mediaDevice.Next(dbus_interface="org.bluez.MediaPlayer1")

	def previous(self):
		'''
		Skip to previous track
		sends to begining of track in some players, and must double previous to actually return to previous track.
		'''
		self.mediaDevice.Previous(dbus_interface="org.bluez.MediaPlayer1")

	def stop(self):
		'''
		Stop the music
		'''
		self.mediaDevice.Stop(dbus_interface="org.bluez.MediaPlayer1")

	def shuffle(self, state):
		'''
		Set the shuffle state
		Expects a bool to determine the shuffle state
		'''
		if state == True:
			self.mediaDevice.Set("org.bluez.MediaPlayer1", "Shuffle", "alltracks")
		elif state == False:
			self.mediaDevice.Set("org.bluez.MediaPlayer1", "Shuffle", "off")

	def getShuffle(self):
		'''
		Determine if the music is shuffled or not.
		Returns a bool
		'''		
		shuffleState = self.mediaDevice.get("org.bluez.MediaPlayer1", "Shuffle")

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
			self.mediaDevice.Set("org.bluez.MediaPlayer1", "Repeat", "off")
		elif state == 1:
			self.mediaDevice.Set("org.bluez.MediaPlayer1", "Repeat", "alltrack")	
		elif state == 2:
			self.mediaDevice.Set("org.bluez.MediaPlayer1", "Repeat", "singletrack")
	
	def getRepeat(self):
		'''
		Get the status of the repeat loop
		Returns an integer with the following possible values
		0: off, 1: all tracks, or 2: single track.
		'''
		repeatState = self.mediaDevice.Get("org.bluez.MediaPlayer1", "Repeat")

		if repeatState == "off":
			return 0
		elif repeatState == "alltrack":
			return 1
		elif repeatState == "singletrack":
			return 2

	def getSongInfo(self):
		'''
		Get the info of the song as a python dictionary. 
		Available fields are:
		Title
		Album
		TrackNumber
		Artist
		TrackNumber
		NumberOfTracks
		Duration

		The duration is the length of the song in miliseconds
		'''

		return self.interface.Get("org.bluez.MediaPlayer1", 'Track')


	def getTrackName(self):
		'''
		Get the name of the currently playing track
		Returns a string with the name of the track
		'''
		return self.interface.Get("org.bluez.MediaPlayer1", 'Track')['Title']

	def getAlbumName(self):
		'''
		Get the name of the album currently playing
		Returns a string with the album name
		'''

		return self.interface.Get("org.bluez.MediaPlayer1", 'Track')['Album']

	def getArtistName(self):
		'''
		Get the name of the artist currently playing
		Returns a string with the name of the artist
		'''

		return self.interface.Get("org.bluez.MediaPlayer1", 'Track')['Artist']


	def getDuration(self):
		'''
		Get the duration of the currently playing song in miliseconds
		Returns and integer containing the length of the song.
		'''
		return int(self.interface.Get("org.bluez.MediaPlayer1", 'Track')['Duration'])
	
	def getPosition(self):
		'''
		Get the current position of the song in miliseconds
		Returns an int
		'''
		return int(self.interface.Get("org.bluez.MediaPlayer1", 'Position'))
	
	def isPlaying(self):
		'''
		Get the status of if the song is playing or not
		Returns a bool containing the status of the song.
		If the status is unknown, the function automatically returns false.
		'''
		status = self.interface.Get("org.bluez.MediaPlayer1", 'Status')

		if status == "playing":
			return True
		elif status == "paused":
			return False
		elif status == "stopped":
			return True
		else:
			return False