#! /bin/python3

'''
Tkinter GUI front-end for open source car stereo project
Made by Red in 2019
Greetings, from the ROC!

https://github.com/nlMeminger/MagiCarp

This code is licensed under the GNU General Public License
For more information see the LICENSE file that was distributed with this code
Or visit https://www.gnu.org/licenses/gpl-3.0.en.html
'''

from tkinter import *
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
import time
import threading

import subprocess
import shlex

import media_control
import systemhost as sh

import CONFIG #Import the configuration options

class Gui:

	sysHost = sh.SystemHost()

	#Define Window Attributes
	rootWindow = None
	windowTitle = 'PyMedia'
	windowDimensions = '800x480'

	#Define image attributes
	bluetoothImage = 'interface_res/bluetooth.gif'
	shuffleImage = "interface_res/shuffle-line.gif"
	shuffleOnImage = "interface_res/shuffle-line-enabled.gif"
	rewindImage = "interface_res/rewind-fill.gif"
	pauseImage = "interface_res/pause-fill.gif"
	playImage = "interface_res/play-fill.gif"
	forwardImage = "interface_res/speed-fill.gif"
	repeatImage = "interface_res/repeat-line.gif"
	repeatSingleImage = "interface_res/repeat-line-all.gif"
	repeatMultiImage = "interface_res/repeat-line-1.gif"
	artistImage = "interface_res/user-fill.gif"
	trackImage = "interface_res/music-2-fill.gif"
	albumImage = "interface_res/album-fill.gif"


	#Root Window
	root = None
	
	#Bluetooth Icon
	bluetooth_icon = None

	#Track info icons
	artist_icon = None
	track_icon = None
	album_icon = None

	#Player control icons
	shuffle_icon = None
	shuffle_icon_on = None
	rewind_icon = None
	pause_icon = None
	play_icon = None
	forward_icon = None
	repeat_icon = None
	repeat_icon_single = None
	repeat_icon_multi = None

	#menu buttons
	file_button = None
	bluetooth_button = None
	phone_button = None
	settings_button = None
	menu_button_height = 80
	menu_button_width = 200

	#menu containers
	file_container = None
	bluetooth_container = None
	phone_container = None
	settings_container = None

	def __init__(self):
		pass

	def exit_gui():
		self.root.destroy()
		exit()

	def defineWindow(self):
		#Define TK root object and set properties
		self.root = tk.Tk()
		self.root.title(self.windowTitle)
		self.root.geometry(self.windowDimensions) #Set window size
		self.root.resizable(0,0) #Disallow resizing of window
		self.root.attributes("-fullscreen", True) #Make window full screen

		#Define global resource images
		self.bluetooth_icon = tk.PhotoImage(file=self.bluetoothImage)

		#Track info icons
		self.artist_icon = tk.PhotoImage(file=self.artistImage).subsample(6,6)
		self.track_icon = tk.PhotoImage(file=self.trackImage).subsample(6,6)
		self.album_icon = tk.PhotoImage(file=self.albumImage).subsample(6,6)

		#Player control icons
		self.shuffle_icon = tk.PhotoImage(file=self.shuffleImage).subsample(3,3)
		self.shuffle_icon_on = tk.PhotoImage(file=self.shuffleOnImage).subsample(3,3)
		self.rewind_icon = tk.PhotoImage(file=self.repeatImage).subsample(3,3)
		self.pause_icon = tk.PhotoImage(file=self.pauseImage).subsample(3,3)
		self.play_icon = tk.PhotoImage(file=self.playImage).subsample(3,3)
		self.forward_icon = tk.PhotoImage(file=self.forwardImage).subsample(3,3)
		self.repeat_icon = tk.PhotoImage(file=self.repeatImage).subsample(3,3)
		self.repeat_icon_single = tk.PhotoImage(file=self.repeatSingleImage).subsample(3,3)
		self.repeat_icon_multi = tk.PhotoImage(file=self.repeatMultiImage).subsample(3,3)#Define TK root object and set properties
		

		def menu_bar():
			menu_font = tkfont.Font(size=20, weight="bold")

			self.file_button = tk.Button(self.root, text='File', font=menu_font, command=self.file_menu)
			self.file_button.place(x=0, y=0, width=self.menu_button_width, height=self.menu_button_height)

			self.bluetooth_button = tk.Button(self.root, text="Bluetooth", font=menu_font, command=self.bluetooth_menu)
			self.bluetooth_button.place(x=200, y=0, width=self.menu_button_width, height=self.menu_button_height)

			self.phone_button = tk.Button(self.root, text="Phone", font=menu_font, command=self.phone_menu)
			self.phone_button.place(x=400, y=0, width=self.menu_button_width, height=self.menu_button_height)

			self.settings_button = tk.Button(self.root, text="Settings", font=menu_font, command=self.settings_menu)
			self.settings_button.place(x=600, y=0, width=self.menu_button_width, height=self.menu_button_height)

		
		def file_menu_init():
			exitButtonWidth = 100
			exitButtonHeight = 20
			exitButtonXpos = 130
			exitButtonYpos = 10

			#Create a frame to hold the items in this menu. Makes switching menus a lot easier.
			self.file_container = tk.Frame()
			self.file_container.place(x=0, y=80, width=800, height=400)
			self.file_container.place_forget()

			#Create an exit button that will exit the program.
			exitButton = tk.Button(self.file_container, text='Exit', command=self.exit_gui)
			exitButton.place(x=exitButtonXpos, y=exitButtonYpos, width=exitButtonWidth, height=exitButtonHeight)

			#Create a slider to control the screen brightness
			brightness_slider = tk.Scale(self.file_container, command=self.sysHost.setBrightness(), from_=5, label='Brightness', orient=tk.HORIZONTAL, to=100,)
			brightness_slider.set(self.sysHost.getCurrBrightness())
			brightness_slider.place(x=130, y=50)
			
			#Create a slider to conteol the system volume
			volume_slider = tk.Scale(self.file_container, command=self.sysHost.setVolume(), from_=0, label='Volume', orient=tk.HORIZONTAL, to=25,)
			volume_slider.place(x=130, y=150)
			

		def bluetooth_menu_init():
			'''
			Contains the actual layout and code for the bluetooth media control menu
			'''
			#Define a new frame to hold the layout information
			self.bluetooth_container = tk.Frame()
			self.bluetooth_container.place(x=0, y=80, width=800, height=400) #Place under the menu bar with a size of 800x400
			self.bluetooth_container.place_forget() #Hide the container

			self.bluetooth_logo = tk.Label(self.bluetooth_container, image=self.bluetooth_icon).place(x=610, y=70) #Placeholder bluetooth icon

			#Create a label for the bluetooth mac address entry
			labelText = ''

			if self.sysHost.checkForConnectedDevices():
				labelText = 'Connected to: {}'.format(self.sysHost.getConnectedDeviceName())
			else:
				#Define the button for the bluetooth device entry
				global bluetooth_address_set
				bluetooth_address_set = tk.Button(this.bluetooth_container, text='Connect', command=init_bt_device)
				bluetooth_address_set.place(x=240, y=10, height=20)


				labelText = 'No Connected Devices'

			bluetooth_address_text = tk.Label(bluetooth_container, text=labelText)
			bluetooth_address_text.place(x=0, y=10, height=50)

			

			#Set the icons for the song info
			track_image = tk.Label(bluetooth_container, image=track_icon).place(x=5, y=60)
			artist_image = tk.Label(bluetooth_container, image=artist_icon).place(x=5, y=120)
			album_image = tk.Label(bluetooth_container, image=album_icon).place(x=5, y=180)

			#Define the text boxes for the song info
			track_info_font = tkfont.Font(size=24)
			global track_name_text
			track_name_text = tk.Label(bluetooth_container, text="", font=track_info_font)
			track_name_text.place(x=50, y=60)
			global artist_name_text
			artist_name_text = tk.Label(bluetooth_container, text="", font=track_info_font)
			artist_name_text.place(x=50, y=120)
			global album_name_text
			album_name_text = tk.Label(bluetooth_container, text="", font=track_info_font)
			album_name_text.place(x=50, y=180)


			#Define the player controls
			global SHUFFLE_VALUE
			global PLAYING
			global LOOP_TYPE

			SHUFFLE_VALUE = False
			PLAYING = False
			LOOP_TYPE = 0

			global shuffle_button
			shuffle_button = tk.Button(bluetooth_container, image=shuffle_icon, command=bt_shuffle_toggle)
			shuffle_button.place(x=15, y=300)
			
			rewind_button = tk.Button(bluetooth_container, image=rewind_icon, command=bt_back).place(x=105, y=300)
			
			global playpause_button
			playpause_button = tk.Button(bluetooth_container, image=play_icon, command=bt_playpause)
			playpause_button.place(x=195, y=300)
			
			forward_button = tk.Button(bluetooth_container, image=forward_icon, command=bt_forward).place(x=285, y=300)
			
			global loop_button
			loop_button = tk.Button(bluetooth_container, image=repeat_icon, command=bt_loop)
			loop_button.place(x=375, y=300)

			#Define the progress bar and track length
			song_position_font = tkfont.Font(size=15)

			global current_position
			current_position = tk.Label(bluetooth_container, text="0:00", font=song_position_font)
			current_position.place(x=15, y=250)
			
			global progress_bar
			progress_bar = ttk.Progressbar(bluetooth_container, orient="horizontal", length=470, mode="determinate")
			progress_bar.place(x=65, y=253)
			
			global track_length
			track_length = tk.Label(bluetooth_container, text="0:00", font=song_position_font)
			track_length.place(x=540, y=250)




























	#Create a container to hide the content of the player until a device is connected
	#global nc_container
	#nc_container = tk.Frame()
	#nc_container.place(x=0, y=130, width=800, height=350)

	#not_connected_font = tkfont.Font(size=40)
	#nc_text = tk.Label(nc_container, text="No Bluetooth Device Connected", font=not_connected_font)
	#nc_text.place(x=0, y=20)


def phone_menu_init():
	'''
	Contains the actual layout and functionality of the phone menu
	'''

	#Define a container to hold the items in the window
	global phone_container
	phone_container = tk.Frame()
	phone_container.place(x=0, y=80, width=800, height=400)
	phone_container.place_forget()


	#WIP Text
	wipfont = tkfont.Font(size=50)
	wiptext = tk.Label(phone_container, text="Nearby Devices", font=wipfont)
	wiptext.place(x=0, y=100)

def settings_menu_init():
	'''
	Contains the layout information and functionality of the settings menu
	'''

	#Create a new frame to hold section content
	global settings_container
	settings_container = tk.Frame()
	settings_container.place(x=0, y=80, width=800, height=400)
	settings_container.place_forget()

	#Define the WIP text
	wipfont = tkfont.Font(size=50)
	wiptext = tk.Label(settings_container, text="Work in progress", font=wipfont)
	wiptext.place(x=0, y=100)

def phone_menu():
	'''
	Switch to the phone menu
	'''

	#Disable currently selected button
	global phone_button
	phone_button.config(state="disabled")

	#Return other buttons to normal state
	global bluetooth_button
	bluetooth_button.config(state="normal")
	global file_button
	file_button.config(state="normal")
	global settings_button
	settings_button.config(state="normal")

	#Hide other tabs
	global file_container
	file_container.place_forget()
	global settings_container
	settings_container.place_forget()
	global bluetooth_container
	bluetooth_container.place_forget()

	#Show phone tab
	global phone_container
	phone_container.place(x=0, y=80, width=800, height=400)

def settings_menu():
	'''
	Switch to the settings meny
	'''
	#Disable currently selected button
	global settings_button
	settings_button.config(state="disabled")

	#Return other buttons to normal state
	global bluetooth_button
	bluetooth_button.config(state="normal")
	global phone_button
	phone_button.config(state="normal")
	global file_button
	file_button.config(state="normal")

	#Hide other tabs
	global file_container
	file_container.place_forget()
	global phone_container
	phone_container.place_forget()
	global bluetooth_container
	bluetooth_container.place_forget()

	#Show settings tab
	global settings_container
	settings_container.place(x=0, y=80, width=800, height=400)

def bluetooth_menu():
	'''
	Show the bluetooth menu
	'''


	#Disable the currently selected button
	global bluetooth_button
	bluetooth_button.config(state="disabled")

	#Return other buttons to normal state
	global file_button
	file_button.config(state="normal")
	global phone_button
	phone_button.config(state="normal")
	global settings_button
	settings_button.config(state="normal")

	#Hide other tabs
	global file_container
	file_container.place_forget()
	global settings_contianer
	settings_container.place_forget()
	global phone_container
	phone_container.place_forget()

	#Show bluetooth tab
	global bluetooth_container

	bluetooth_container.place(x=0, y=80, width=800, height=400)

def file_menu():
	'''
	Show the file player menu
	'''

	#Disable currently selected button
	global file_button
	file_button.config(state="disabled")

	#Return other buttons to normal state
	global bluetooth_button
	bluetooth_button.config(state="normal")
	global phone_button
	phone_button.config(state="normal")
	global settings_button
	settings_button.config(state="normal")

	#Hide other tabs
	global settings_container
	settings_container.place_forget()
	global phone_container
	phone_container.place_forget()
	global bluetooth_container
	bluetooth_container.place_forget()

	#Show file tab
	global file_container
	file_container.place(x=0, y=80, width=800, height=400)

def get_connected_mac():
	command = 'hcitool con'
	
	results = command_run(command)

	stdout = results['stdout'].split()
	print(stdout)
	stdout = stdout[3].strip()	
	return stdout

def init_bt_device():
	'''
	Initialize the bluetooth device
	'''	

	global bluetooth_address_set
	#bluetooth_address_set.config(state="disabled")

	global BT_DEVICE
	if check_for_connected_devices():
		BT_DEVICE = media_control.mediaControl(get_connected_mac()) #Create the bluetooth device

	#Start the track info thread
	threading.Thread(target=bt_song_info_thread).start()

	root.update()

def bt_shuffle_toggle():
	'''
	Toggle shuffle control
	'''
	global SHUFFLE_VALUE
	global shuffle_button
	global BT_DEVICE

	if SHUFFLE_VALUE == True:
		SHUFFLE_VALUE = False
		shuffle_button['image'] = shuffle_icon
		try:
			BT_DEVICE.shuffle(False)
		except:
			print("Error")

	elif SHUFFLE_VALUE == False:
		SHUFFLE_VALUE = True
		shuffle_button['image'] = shuffle_icon_on
		try:
			BT_DEVICE.shuffle(True)
		except:
			print("Error")

def bt_forward():
	'''
	Send the forward command
	'''

	global PLAYING
	global BT_DEVICE

	if PLAYING == False:
		#If not playing do nothing
		pass
	elif PLAYING == True:
		#If playing skip the song
		BT_DEVICE.next() #Send the next command

def bt_back():
	'''
	Send the previous command
	'''

	global PLAYING
	global BT_DEVICE

	if PLAYING == False:
		#If not playing do nothing
		pass
	elif PLAYING == True:
		#If playing skip the song
		BT_DEVICE.previous() #Send the next command

def bt_playpause():
	'''
	Play and pause the music
	'''
	global PLAYING
	global playpause_button
	global BT_DEVICE

	if PLAYING == True:
		#If playing
		PLAYING = False
		playpause_button['image'] = play_icon #Set play button to the play icon
		BT_DEVICE.pause() #Send the pause command

	elif PLAYING == False:
		#If paused
		PLAYING = True
		playpause_button['image'] = pause_icon #Set the play button to the pause icon
		BT_DEVICE.play() #Send the play command

def bt_loop():
	'''
	Toggle between the 3 different loop types, song, album, and off
	'''
	global LOOP_TYPE
	global loop_button
	global BT_DEVICE

	if LOOP_TYPE == 0:
		#Song
		LOOP_TYPE = 1
		loop_button['image'] = repeat_icon_single #repeat song
		try:
			BT_DEVICE.repeat(1)
		except:
			print("error")
			LOOP_TYPE = 0

	elif LOOP_TYPE == 1:
		#Album
		LOOP_TYPE = 2
		loop_button['image'] = repeat_icon_multi #Repeat album
		try:
			BT_DEVICE.repeat(2)
		except:
			print("error")
			LOOP_TYPE = 0

	elif LOOP_TYPE == 2:
		#Off
		LOOP_TYPE = 0
		loop_button['image'] = repeat_icon #Repeat off
		try:
			BT_DEVICE.repeat(0)
		except:
			print("error")
			LOOP_TYPE = 0

def bt_song_info_thread():
	'''
	Thread for the bluetooth song info
	'''
	global PLAYING
	global BT_DEVICE
	global track_length
	global progress_bar
	global playpause_button
	global artist_name_text
	global album_name_text
	global track_name_text
	global current_position
	while True: #Always
		while PLAYING:
			#Only update info while playing

			#Update the artist infi
			#If it fails to obtain the info for any reason, just set the value to nothing
			try:
				artist_name_text['text'] = textslice(BT_DEVICE.getArtistName()) #Update the artist name
			except:
				artist_name_text['text'] = ""
			try:	
				album_name_text['text'] = textslice(BT_DEVICE.getAlbumName()) #Album Name
			except:
				album_name_text['text'] = ""
			try:
				track_name_text['text'] = textslice(BT_DEVICE.getTrackName()) #Song name
			except:
				track_name_text['text'] = ""
			
			#Detect if the device is playing music to see if it was paused from another place
			if BT_DEVICE.isPlaying() == False:
				#If playing
				PLAYING = False
				playpause_button['image'] = play_icon #Set play button to the play icon
			
			#Try changing shuffle
			try:
				if BT_DEVICE.getShuffle() == False and SHUFFLE_VALUE == True: #If there's a mismatch	
					SHUFFLE_VALUE = True
					shuffle_button['image'] = shuffle_icon_on #Set icon to shuffle on
				elif BT_DEVICE.getShuffle() == True and SHUFFLE_VALUE == False:
					SHUFFLE_VALUE = False
					shuffle_button['image'] = shuffle_icon #Set icon to shuffle off
			except:
				#If there's a problem, set the shuffle to off
				SHUFFLE_VALUE = False
				shuffle_button['image'] = shuffle_icon 

			#See if the repeat mode is on
			try:
				if BT_DEVICE.getRepeat() == 0 and (LOOP_TYPE == 1 or LOOP_TYPE == 2):
					LOOP_TYPE = 0
					loop_button['image'] = repeat_icon
				elif BT_DEVICE.getRepeat() == 1 and (LOOP_TYPE == 0 or LOOP_TYPE == 2):
					LOOP_TYPE = 1
					loop_button['image'] = repeat_icon_single
				elif BT_DEVICE.getRepeat() == 2 and (LOOP_TYPE == 0 or LOOP_TYPE == 1):
					LOOP_TYPE = 2
					loop_button['image'] = repeat_icon_multi
			except:
				#If there's an error just set it to off
				LOOP_TYPE = 0
				loop_button['image'] = repeat_icon

			#Constantly update the track length and the progress bar
			try:
				track_length['text'] = ms_to_timecode(BT_DEVICE.getDuration()) #Update the track length
				current_position['text'] = ms_to_timecode(BT_DEVICE.getPosition()) #Update the current position
				progress_bar['value'] = mapper(BT_DEVICE.getPosition(), 0, BT_DEVICE.getDuration()) #Update the progress bar
			except:
				#If there's any error, just set everything to 0
				track_length['text'] = "0:00"
				current_position['text'] = "0:00"
				progress_bar['value'] = 0

			time.sleep(0.1) #Sleep to prevent the thread from taking all CPU time

		#Wait for the device to keep playing
		if BT_DEVICE.isPlaying() == True:
			PLAYING = True
			playpause_button['image'] = pause_icon
		time.sleep(0.01) #Sleep to prevent the thread from taking all CPU time

def mapper(in_value, minimum, maximum):
	'''
	Map a value to a percentage between 1 and 100
	Take an input value, the minimum possible value, and the maximum possible value
	'''
	in_range = maximum - minimum #Get the range
	value = in_value - minimum
	out_value = (float(in_value)/in_range)*100 #Map the value
	return out_value+minimum

def ms_to_timecode(ms):
	'''
	Converts miliseconds to a time code MM:SS
	Returns a string containing the time code
	'''
	secs = int((ms/1000) % 60)
	if secs < 10:
		secs = "0{}".format(secs)
	mins = int((ms/1000) / 60)

	return "{}:{}".format(mins,secs)

def textslice(text):
	'''
	Slice text that is too long to be displayed on the screen
	Takes input text
	Returns output text that is sliced
	'''
	if len(text) >= 24:
		return "{}...".format(text[:24])
	else:
		return text

def main():

	
	menu_bar() #Start menu bar


	#Initialize menus	
	phone_menu_init()
	settings_menu_init()
	file_menu_init()
	bluetooth_menu_init()


	#Find which tab to start on
	if CONFIG.DEFAULT_TAB == 1: #File menu
		file_menu()

	elif CONFIG.DEFAULT_TAB == 2: #Bluetooth menu
		bluetooth_menu()

	elif CONFIG.DEFAULT_TAB == 3: #Phone menu
		phone_menu()

	elif CONFIG.DEFAULT_TAB == 4: #Settings menu
		settings_menu()

	init_bt_device()

	#Begin displaying the window	
	root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
