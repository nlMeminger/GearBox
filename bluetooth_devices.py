import bluetooth


class bluetoothConnection:

	def __init__(self, name):
		
		self.socket = bluetooth.BluetoothSocket(bluetooth.HCI)

		bluetooth.advertise_service(socket, name, service_id=bluetooth.AUDIO_SINK_CLASS, service_classes=[bluetooth.AUDIO_SINK_CLASS], profiles=[bluetooth.AUDIO_SINK_CLASS])

		self.client_sock, self.client_info = socket.accept()

	
	def getClientInfo(self):
		return self.client_info

	def 

