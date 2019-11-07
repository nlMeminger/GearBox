'''
DBus Audio Device Control


'''

import dbus

bus = dbus.SystemBus()

class mediaControl:
	'''
	media Control Class
	'''

	def __init__(self, mac_address):

		dbusDeviceAddress = self.mac_to_dbus(mac_address)
		self.mediaDevice = bus.get_object('org.bluez', "/org/bluez/hci0/" + dbusDeviceAddress + "/player0")
		self.interface = dbus.Interface(self.mediaDevice, "org.freedesktop.DBus.Properties")

	def mac_to_dbus(self, mac_address):

		dbusDevice = "dev_"
		for char in mac_address:
			if char == ":":
				dbusDevice += "_"
			else:
				dbusDevice += char
		return dbusDevice


	def pause(self):

		self.mediaDevice.Pause(dbus_interface="org.bluez.MediaPlayer1")

	def play(self):

		self.mediaDevice.Play(dbus_interface="org.bluez.MediaPlayer1")

	def next(self):

		self.mediaDevice.Next(dbus_interface="org.bluez.MediaPlayer1")

	def previous(self):

		self.mediaDevice.Previous(dbus_interface="org.bluez.MediaPlayer1")

	def stop(self):

		self.mediaDevice.Stop(dbus_interface="org.bluez.MediaPlayer1")

	def get_song_info(self):



		print(self.interface.Get("org.bluez.MediaPlayer1", 'Track').join(chr(byte) for byte in byte_array))


