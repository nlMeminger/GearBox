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

	sysHost = None
	device = None

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
	volumeUpImage = 'interface_res/volume-up-fill.gif'
	volumeDownImage = 'interface_res/volume-down-fill.gif'
	brightnessUpImage = 'interface_res/brightness-up.png'
	brightnessDownImage = 'interface_res/brightness-down.png'

	#Root Window
	root = None
	
	#system control icons
	brightness_up_icon = None
	brightness_down_icon = None
	volume_up_icon = None
	volume_down_icon = None

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

	#buttons
	file_button = None
	bluetooth_button = None
	phone_button = None
	settings_button = None
	menu_button_height = 80
	menu_button_width = 200
	shuffle_button = None
	rewind_button = None
	playpause_button = None
	forward_button = None
	loop_button = None
	current_position = None
	progress_bar = None
	track_length = None

	#menu containers
	file_container = None
	bluetooth_container = None
	phone_container = None
	settings_container = None

	#define playback attributes
	SHUFFLE_VALUE = False
	PLAYING = False
	LOOP_TYPE = 0
	INITSTART =True

	artistNameText = None
	albumNameText = None
	trackNameText = None
	currentPosition = None

	def __init__(self, device, sysHost):
		self.device = device
		self.sysHost = sysHost
		self.defineWindow()
		
		 #Start menu bar
		#Initialize menus	
		self.phone_menu_init()
		self.settings_menu_init()
		self.file_menu_init()
		self.bluetooth_menu_init()
		self.menu_bar()		
		self.INITSTART = False

		#Find which tab to start on
		if CONFIG.DEFAULT_TAB == 1: #File menu
			self.switchMenu('file')

		elif CONFIG.DEFAULT_TAB == 2: #Bluetooth menu
			self.switchMenu('bluetooth')

		elif CONFIG.DEFAULT_TAB == 3: #Phone menu
			self.switchMenu('phone')

		elif CONFIG.DEFAULT_TAB == 4: #Settings menu
			self.switchMenu('settings')
		
		self.init_bt_device()

				

		#Begin displaying the window	
		self.root.mainloop()

	def exit_gui(self):
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
		self.track_icon  = tk.PhotoImage(file=self.trackImage).subsample(6,6)
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
		
		#system control icons
		self.brightness_up_icon = tk.PhotoImage(file=self.brightnessUpImage).subsample(6,6)
		self.brightness_down_icon = tk.PhotoImage(file=self.brightnessDownImage).subsample(6,6)
		self.volume_up_icon = tk.PhotoImage(file=self.volumeUpImage).subsample(6,6)
		self.volume_down_icon = tk.PhotoImage(file=self.volumeDownImage).subsample(6,6)

	def menu_bar(self):

		menu_font = tkfont.Font(size=20, weight="bold")
		
		self.file_button = tk.Button(self.root, text='File', font=menu_font, command= lambda: self.switchMenu('file'))
		self.file_button.place(x=0, y=0, width=self.menu_button_width, height=self.menu_button_height)
		
		self.bluetooth_button = tk.Button(self.root, text="Bluetooth", font=menu_font, command= lambda: self.switchMenu('bluetooth'))
		self.bluetooth_button.place(x=200, y=0, width=self.menu_button_width, height=self.menu_button_height)
		
		self.phone_button = tk.Button(self.root, text="Phone", font=menu_font, command= lambda: self.switchMenu('phone'))
		self.phone_button.place(x=400, y=0, width=self.menu_button_width, height=self.menu_button_height)
		
		self.settings_button = tk.Button(self.root, text="Settings", font=menu_font, command= lambda: self.switchMenu('settings'))
		self.settings_button.place(x=600, y=0, width=self.menu_button_width, height=self.menu_button_height)
	
	def file_menu_init(self):
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
		brightness_slider = tk.Scale(self.file_container)
		currentBrightness = self.sysHost.getCurrBrightness()
		brightness_slider = tk.Scale(self.file_container, length=200, command=self.sysHost.setBrightness, from_=5, label='Brightness', orient=tk.HORIZONTAL, to=100,)
		brightness_slider.set(currentBrightness)
		brightness_slider.place(x=130, y=60)
		
		brightnessUpButton = tk.Button(self.file_container, command= lambda: self.brightnessUp(brightness_slider), image=self.brightness_up_icon)
		brightnessDownButton = tk.Button(self.file_container, command= lambda: self.brightnessDown(brightness_slider), image=self.brightness_down_icon)
		brightnessUpButton.place(x=50, y=30)
		brightnessDownButton.place(x=50, y=90)
		
		#Create a slider to control the system volume
		volume_slider = tk.Scale(self.file_container)
		currentVolume = self.sysHost.getCurrVolume()
		volume_slider = tk.Scale(self.file_container, length=200, command=self.sysHost.setVolume, from_=0, label='Volume', orient=tk.HORIZONTAL, to=100,)
		volume_slider.set(currentVolume)

		volume_slider.place(x=130, y=150)
		
		volumeUpButton = tk.Button(self.file_container, command= lambda: self.volumeUp(volume_slider), image=self.volume_up_icon)
		volumeDownButton = tk.Button(self.file_container, command= lambda: self.volumeDown(volume_slider), image=self.volume_down_icon)
		volumeUpButton.place(x=50, y=140)
		volumeDownButton.place(x=50, y=190)

	def bluetooth_menu_init(self):
		'''
		Contains the actual layout and code for the bluetooth media control menu
		'''
		#Define a new frame to hold the layout information
		self.bluetooth_container = tk.Frame()
		self.bluetooth_container.place(x=0, y=80, width=800, height=400) #Place under the menu bar with a size of 800x400
		self.bluetooth_container.place_forget() #Hide the container

		self.bluetooth_logo = tk.Label(self.bluetooth_container, image=self.bluetooth_icon)
		self.bluetooth_logo.place(x=610, y=70) #Placeholder bluetooth icon

		#Create a label for the device name
		labelText = ''

		if self.sysHost.checkForConnectedDevices():
			labelText = 'Connected to: {}'.format(self.device.deviceName)
		else:
			#Define the button for the bluetooth device entry
			connectDevice = tk.Button(self.bluetooth_container, text='Connect', command=self.device.connectToPlayer())
			connectDevice.place(x=240, y=10, height=20)
			labelText = 'No Connected Devices'

		bluetooth_address_text = tk.Label(self.bluetooth_container, text=labelText)
		bluetooth_address_text.place(x=0, y=10, height=50)

		

		#Set the icons for the song info
		self.artist_icon = tk.Label(self.bluetooth_container, image=self.artist_icon)
		self.artist_icon.place(x=5, y=120)
		self.track_icon = tk.Label(self.bluetooth_container, image=self.track_icon)
		self.track_icon.place(x=5, y=60)
		
		self.album_icon = tk.Label(self.bluetooth_container, image=self.album_icon)
		self.album_icon.place(x=5, y=180)

		#Define the text boxes for the song info
		trackInfoFont = tkfont.Font(size=24)
		self.trackNameText = tk.Label(self.bluetooth_container, text="", font=trackInfoFont)
		self.trackNameText.place(x=50, y=60)
		
		self.artistNameText = tk.Label(self.bluetooth_container, text="", font=trackInfoFont)
		self.artistNameText.place(x=50, y=120)
		
		self.albumNameText = tk.Label(self.bluetooth_container, text="", font=trackInfoFont)
		self.albumNameText.place(x=50, y=180)



		self.shuffle_button = tk.Button(self.bluetooth_container, image=self.shuffle_icon, command=self.bt_shuffle_toggle)
		self.shuffle_button.place(x=15, y=300)
		
		self.rewind_button = tk.Button(self.bluetooth_container, image=self.rewind_icon, command=self.bt_back)
		self.rewind_button.place(x=105, y=300)
		
		self.playpause_button = tk.Button(self.bluetooth_container, image=self.play_icon, command=self.bt_playpause)
		self.playpause_button.place(x=195, y=300)
		
		self.forward_button = tk.Button(self.bluetooth_container, image=self.forward_icon, command=self.bt_forward)
		self.forward_button.place(x=285, y=300)
		
		self.loop_button = tk.Button(self.bluetooth_container, image=self.repeat_icon, command=self.bt_loop)
		self.loop_button.place(x=375, y=300)

		#Define the progress bar and track length
		song_position_font = tkfont.Font(size=15)

		self.current_position = tk.Label(self.bluetooth_container, text="0:00", font=song_position_font)
		self.current_position.place(x=15, y=250)
		
		self.progress_bar = ttk.Progressbar(self.bluetooth_container, orient="horizontal", length=470, mode="determinate")
		self.progress_bar.place(x=65, y=253)
		
		self.track_length = tk.Label(self.bluetooth_container, text="0:00", font=song_position_font)
		self.track_length.place(x=540, y=250)

	def phone_menu_init(self):
		'''
		Contains the actual layout and functionality of the phone menu
		'''

		#Define a container to hold the items in the window
		self.phone_container = tk.Frame()
		self.phone_container.place(x=0, y=80, width=800, height=400)
		self.phone_container.place_forget()


		#WIP Text
		wipfont = tkfont.Font(size=50)
		wiptext = tk.Label(self.phone_container, text="Nearby Devices", font=wipfont)
		wiptext.place(x=0, y=100)

	
	def settings_menu_init(self):
		'''
		Contains the layout information and functionality of the settings menu
		'''

		#Create a new frame to hold section content
		self.settings_container = tk.Frame()
		self.settings_container.place(x=0, y=80, width=800, height=400)
		self.settings_container.place_forget()

		#Define the WIP text
		wipfont = tkfont.Font(size=50)
		wiptext = tk.Label(self.settings_container, text="Work in progress", font=wipfont)
		wiptext.place(x=0, y=100)

	def brightnessUp(self, slider):
		curr = int(self.sysHost.currBrightness)
		new = curr + 1
		if new > 100:
			return
		self.sysHost.setBrightness(new)
		slider.set(new)

	def brightnessDown(self, slider):
		curr = int(self.sysHost.currBrightness)
		new = curr - 1
		if new < 5:
			return
		self.sysHost.setBrightness(new)
		slider.set(new)

	def volumeUp(self, slider):
		curr = self.sysHost.currVolume
		new = curr + 1
		if new < 0:
			return
		self.sysHost.setVolume(new)
		slider.set(new)
	
	def volumeDown(self, slider):
		curr = self.sysHost.currVolume
		new = curr - 1
		if new > 75: return
		self.sysHost.setVolume(new)
		slider.set(new)

	def switchMenu(self, menuName = ''):
		if self.INITSTART == False:	
			menus = {
				'file':[self.file_button, self.file_container], 
				'phone': [self.phone_button, self.phone_container], 
				'bluetooth': [self.bluetooth_button, self.bluetooth_container] , 
				'settings': [self.settings_button, self. settings_container],
				}
			
			selectedMenu = menus[menuName]
			
			if menuName.lower() in menus:
				menus.pop(menuName)
			elif menuName.lower() not in menus:
				print('No such menu name')

			for menu in menus:
				menus[menu][0].config(state='normal')
				menus[menu][1].place_forget()

			selectedMenu[0].config(state='disabled')
			selectedMenu[1].place(x=0, y=80, width=800, height=400)
	
	def init_bt_device(self):
		'''
		Initialize the bluetooth device
		'''	
		
		if self.sysHost.checkForConnectedDevices():
			self.device.connectToPlayer() #Create the bluetooth device

		#Start the track info thread
		threading.Thread(target=self.bt_song_info_thread).start()

		self.root.update()

	def bt_shuffle_toggle(self):
		'''
		Toggle shuffle control
		'''

		if self.SHUFFLE_VALUE == True:
			self.SHUFFLE_VALUE = False
			self.shuffle_button['image'] = self.shuffle_icon
			try:
				self.device.bluezPlayer.shuffle(False)
			except Exception as e:
				print(e)
				print("Error")

		elif SHUFFLE_VALUE == False:
			SHUFFLE_VALUE = True
			self.shuffle_button['image'] = self.shuffle_icon_on
			try:
				self.device.bluezPlayer.shuffle(True)
			except Exception as e:
				print(e)
				print("Error")

	def bt_forward(self):
		'''
		Send the forward command
		'''		

		if self.PLAYING == False:
			#If not playing do nothing
			pass
		elif self.PLAYING == True:
			#If playing skip the song
			self.device.bluezPlayer.next() #Send the next command
			
	def bt_back(self):
		'''
		Send the previous command
		'''
		if self.PLAYING == False:
			#If not playing do nothing
			pass

		elif self.PLAYING == True:
			#If playing skip the song
			self.device.bluezPlayer.previous() #Send the next command


	def bt_playpause(self):
		'''
		Play and pause the music
		'''
		
		if self.PLAYING == True:
			#If playing
			self.PLAYING = False
			self.playpause_button['image'] = self.play_icon #Set play button to the play icon
			self.device.bluezPlayer.pause() #Send the pause command

		elif self.PLAYING == False:
			#If paused
			self.PLAYING = True
			self.playpause_button['image'] = self.pause_icon #Set the play button to the pause icon
			self.device.bluezPlayer.play() #Send the play command

	def bt_loop(self):
		'''
		Toggle between the 3 different loop types, song, album, and off
		'''

		if self.LOOP_TYPE == 0:
			#Song
			self.LOOP_TYPE = 1
			self.loop_button['image'] = self.repeat_icon_single #repeat song
			try:
				self.device.bluezPlayer.repeat(1)
			except:
				print("error")
				self.LOOP_TYPE = 0

		elif self.LOOP_TYPE == 1:
			#Album
			self.LOOP_TYPE = 2
			self.loop_button['image'] = self.repeat_icon_multi #Repeat album
			try:
				self.device.bluezPlayer.repeat(2)
			except:
				print("error")
				self.LOOP_TYPE = 0

		elif self.LOOP_TYPE == 2:
			#Off
			self.LOOP_TYPE = 0
			self.loop_button['image'] = self.repeat_icon #Repeat off
			try:
				self.device.bluezPlayer.repeat(0)
			except:
				print("error")
				self.LOOP_TYPE = 0

	def bt_song_info_thread(self):
		'''
		Thread for the bluetooth song info
		'''

		while True: #Always
			while self.PLAYING:
				#Only update info while playing

				#Update the artist infi
				#If it fails to obtain the info for any reason, just set the value to nothing
				try:
					self.artistNameText['text'] = self.textslice(self.device.bluezPlayer.getArtistName()) #Update the artist name
				except Exception as e:
					print(e)
					self.artistNameText['text'] = ""
				try:	
					self.artistNameText['text'] = self.textslice(self.device.bluezPlayer.getAlbumName()) #Album Name
				except Exception as e:
					print(e)
					self.artistNameText['text'] = ""
				try:
					self.trackNameText['text'] = self.textslice(self.device.bluezPlayer.getTrackName()) #Song name
				except Exception as e:
					print(e)
					self.trackNameText['text'] = ""
				
				#Detect if the device is playing music to see if it was paused from another place
				if self.device.bluezPlayer.isPlaying() == False:
					#If playing
					self.PLAYING = False
					self.playpause_button['image'] = self.play_icon #Set play button to the play icon
				
				#Try changing shuffle
				try:
					if self.device.bluezPlayer.getShuffle() == False and self.SHUFFLE_VALUE == True: #If there's a mismatch	
						self.SHUFFLE_VALUE = True
						self.shuffle_button['image'] = self.shuffle_icon_on #Set icon to shuffle on
					elif self.device.bluezPlayer.getShuffle() == True and self.SHUFFLE_VALUE == False:
						self.SHUFFLE_VALUE = False
						self.shuffle_button['image'] = self.shuffle_icon #Set icon to shuffle off
				except Exception as e:
					print(e)
					#If there's a problem, set the shuffle to off
					self.SHUFFLE_VALUE = False
					self.shuffle_button['image'] = self.shuffle_icon 

				#See if the repeat mode is on
				try:
					if self.device.bluezPlayer.getRepeat() == 0 and (self.LOOP_TYPE == 1 or self.LOOP_TYPE == 2):
						self.LOOP_TYPE = 0
						self.loop_button['image'] = self.repeat_icon
					elif self.device.bluezPlayer.getRepeat() == 1 and (self.LOOP_TYPE == 0 or self.LOOP_TYPE == 2):
						self.LOOP_TYPE = 1
						self.loop_button['image'] = self.repeat_icon_single
					elif self.device.bluezPlayer.getRepeat() == 2 and (self.LOOP_TYPE == 0 or self.LOOP_TYPE == 1):
						self.LOOP_TYPE = 2
						self.loop_button['image'] = self.repeat_icon_multi
				except Exception as e:
					print(e)
					#If there's an error just set it to off
					self.LOOP_TYPE = 0
					self.loop_button['image'] = self.repeat_icon

				#Constantly update the track length and the progress bar
				try:
					self.track_length['text'] = self.ms_to_timecode(self.device.bluezPlayer.getDuration()) #Update the track length
					self.current_position['text'] = self.ms_to_timecode(self.device.bluezPlayer.getPosition()) #Update the current position
					self.progress_bar['value'] = self.mapper(self.device.bluezPlayer.getPosition(), 0, self.device.bluezPlayer.getDuration()) #Update the progress bar
				except Exception as e:
					print(e)
					#If there's any error, just set everything to 0
					self.track_length['text'] = "0:00"
					self.current_position['text'] = "0:00"
					self.progress_bar['value'] = 0

				time.sleep(0.1) #Sleep to prevent the thread from taking all CPU time

			#Wait for the device to keep playing
			if self.device.bluezPlayer.isPlaying() == True:
				self.PLAYING = True
				self.playpause_button['image'] = self.pause_icon
			time.sleep(0.01) #Sleep to prevent the thread from taking all CPU time


	def mapper(self, in_value, minimum, maximum):
		'''
		Map a value to a percentage between 1 and 100
		Take an input value, the minimum possible value, and the maximum possible value
		'''
		in_range = maximum - minimum #Get the range
		out_value = (float(in_value)/in_range)*100 #Map the value
		return out_value+minimum

	def ms_to_timecode(self, ms):
		'''
		Converts miliseconds to a time code MM:SS
		Returns a string containing the time code
		'''
		secs = int((ms/1000) % 60)
		if secs < 10:
			secs = "0{}".format(secs)
		mins = int((ms/1000) / 60)

		return "{}:{}".format(mins,secs)

	def textslice(self, text):
		'''
		Slice text that is too long to be displayed on the screen
		Takes input text
		Returns output text that is sliced
		'''
		if len(text) >= 24:
			return "{}...".format(text[:24])
		else:
			return text
