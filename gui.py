'''
Tkinter GUI front-end for open source car stereo project
Made by Red in 2019
Greetings, from the ROC!

https://github.com/nlMeminger/MagiCarp

This code is licensed under the GNU General Public License
For more information see the LICENSE file that was distributed with this code
Or visit https://www.gnu.org/licenses/gpl-3.0.en.html
'''


import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
import time
import threading
import importlib

import tab
#import media_control

import CONFIG #Import the configuration options

#Define TK root object and set properties
root = tk.Tk()
root.title("PyMedia")
root.geometry("800x480") #Set window size
root.resizable(0,0) #Disallow resizing of window
#root.attributes("-fullscreen", True) #Make window full screen


def load_mods():
	global MODULES
	MODULES = []
	global TABS
	TABS = []
	for index in range(len(CONFIG.LOAD_MODULES)):
		importlib.import_module(CONFIG.LOAD_MODULES[index])
		MODULES.append(CONFIG.LOAD_MODULES[index](root))
		TABS.append(tab(root, 800/len(CONFIG.LOAD_MODULES), index, MODULES[index].displayName, root, MODULES[index]))

#Define global resource images


bluetooth_icon = tk.PhotoImage(file="interface_res/bluetooth.gif")


#Track info icons
artist_icon = tk.PhotoImage(file="interface_res/user-fill.gif").subsample(6,6)
track_icon = tk.PhotoImage(file="interface_res/music-2-fill.gif").subsample(6,6)
album_icon = tk.PhotoImage(file="interface_res/album-fill.gif").subsample(6,6)

#Player control icons
shuffle_icon = tk.PhotoImage(file="interface_res/shuffle-line.gif").subsample(3,3)
shuffle_icon_on = tk.PhotoImage(file="interface_res/shuffle-line-enabled.gif").subsample(3,3)
rewind_icon = tk.PhotoImage(file="interface_res/rewind-fill.gif").subsample(3,3)
pause_icon = tk.PhotoImage(file="interface_res/pause-fill.gif").subsample(3,3)
play_icon = tk.PhotoImage(file="interface_res/play-fill.gif").subsample(3,3)
forward_icon = tk.PhotoImage(file="interface_res/speed-fill.gif").subsample(3,3)
repeat_icon = tk.PhotoImage(file="interface_res/repeat-line.gif").subsample(3,3)
repeat_icon_single = tk.PhotoImage(file="interface_res/repeat-line-all.gif").subsample(3,3)
repeat_icon_multi = tk.PhotoImage(file="interface_res/repeat-line-1.gif").subsample(3,3)

#Settings quick actions icons
shutdown_icon = tk.PhotoImage(file="interface_res/shut-down-line.gif").subsample(2,2)
reboot_icon = tk.PhotoImage(file="interface_res/restart-line.gif").subsample(2,2)
exit_icon = tk.PhotoImage(file="interface_res/close-line.gif").subsample(2,2)

def menu_bar():

	menu_font = tkfont.Font(size=25, weight="bold")

	global file_button
	file_button = tk.Button(root, text='File', font=menu_font, command=file_menu)
	file_button.place(x=0, y=0, width=200, height=80)

	global bluetooth_button
	bluetooth_button = tk.Button(root, text="Bluetooth", font=menu_font, command=bluetooth_menu)
	bluetooth_button.place(x=200, y=0, width=200, height=80)

	global phone_button
	phone_button = tk.Button(root, text="Phone", font=menu_font, command=phone_menu)
	phone_button.place(x=400, y=0, width=200, height=80)

	global settings_button
	settings_button = tk.Button(root, text="Settings", font=menu_font, command=settings_menu)
	settings_button.place(x=600, y=0, width=200, height=80)


def file_menu_init():

	#Create a frame to hold the items in this menu. Makes switching menus a lot easier.
	global file_container
	file_container = tk.Frame()
	file_container.place(x=0, y=80, width=800, height=400)
	file_container.place_forget()

	wipfont = tkfont.Font(size=50)
	wiptext = tk.Label(file_container, text="Work in progress", font=wipfont)
	wiptext.place(x=0, y=100)
	

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
	wiptext = tk.Label(phone_container, text="Work in progress", font=wipfont)
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

	#Create shutdown, reboot, and exit buttons
	system_control_font = tkfont.Font(size=18)

	shutdown_button = tk.Button(settings_container, image=shutdown_icon)
	shutdown_button.place(x=10, y=10)
	shutdown_label = tk.Label(settings_container, text="Shutdown", font=system_control_font).place(x=14, y=145)

	reboot_button = tk.Button(settings_container, image=reboot_icon)
	reboot_button.place(x=140, y=10)
	reboot_label = tk.Label(settings_container, text="Reboot", font=system_control_font).place(x=161, y=145)

	exit_button = tk.Button(settings_container, image=exit_icon)
	exit_button.place(x=270, y=10)
	exit_label = tk.Label(settings_container, text="Exit", font=system_control_font).place(x=310, y=145)



	

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


def init_bt_device():
	'''
	Initialize the bluetooth device
	'''	

	global bluetooth_address_set
	bluetooth_address_set.config(state="disabled")

	global BT_DEVICE
	BT_DEVICE = media_control.mediaControl(bluetooth_address_entry.get()) #Create the bluetooth device

	global nc_container
	nc_container.place_forget() #Hide the "not connected" information

	#Start the track info thread
	threading.Thread(target=bt_song_info_thread).start()

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

	#Begin displaying the window	
	root.mainloop()

if __name__ == "__main__":
	main()
