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

import CONFIG #Import the configuration options

#Define TK root object and set properties
root = tk.Tk()
root.title("PyMedia")
root.geometry("800x480") #Set window size
root.resizable(0,0) #Disallow resizing of window
root.attributes("-fullscreen", True) #Make window full screen

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

def exit_gui():
	root.destroy()
	exit()
	raise Exception
def command_run(command):
	command = shlex.quote(command)
	command = shlex.split(command)
	process = subprocess.Popen(
	command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
	)
	stdout, stderr = process.communicate()
	stdout_ = stdout.decode().strip()
	stderr_ = stderr.decode().strip()
	status_ = process.returncode

	results = {'stdout': stdout_, 'stderr': stderr_, 'status': status_}

	return results

def adjust_brightness(brightness):

	brightness = int(brightness) / 100

	#print(brightness)

	command_run(' xrandr --output eDP-1 --brightness {}'.format(brightness))
	
	#file = open("/sys/class/backlight/rpi_backlight/brightness","w")
	#file.write(str(brightness))
	#file.close()

def get_curr_brightness():
	#results = command_run('cat /sys/class/backlight/rpi_backlight/brightness')
	#currBrightness = int(results['stdout']) / 2.55
	
	currBrightness = command_run('xrandr --verbose |grep eDP-1 -A 5 | grep Brightness')
	currBrightness = float(currBrightness['stdout'].split()[1].strip()) * 100

	return currBrightness


def adjust_volume(volume_level):
	volume_level = int(volume_level) * 1000
	command_run('pactl set-sink-volume @DEFAULT_SINK@ {}'.format(volume_level))

def check_for_connected_devices():
	results = command_run('hcitool con')
	
	if '>' not in results['stdout']:
		return False
	else:
		return True

def get_connected_device_name():
	results = command_run('hcitool info {} | grep Name'.format(get_connected_mac()))
	name = results['stdout'].replace('Device Name: ', '')
	return name

def menu_bar():

	menu_font = tkfont.Font(size=20, weight="bold")

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

	exitButton = tk.Button(file_container, text='Exit', command=exit_gui)
	exitButton.place(x=130, y=10, width=100, height=20)

	#wipfont = tkfont.Font(size=50)
	#wiptext = tk.Label(file_container, text="Work in progress", font=wipfont)
	#wiptext.place(x=0, y=100)


	brightness_slider = tk.Scale(file_container, command=adjust_brightness, from_=5, label='Brightness', orient=tk.HORIZONTAL, to=100,)
	brightness_slider.set(get_curr_brightness())
	brightness_slider.place(x=130, y=50)
	
	volume_slider = tk.Scale(file_container, command=adjust_volume, from_=0, label='Volume', orient=tk.HORIZONTAL, to=25,)
	volume_slider.place(x=130, y=150)

	#master = Tk()
	#w = Scale(master, from_=0, to=42)
	#w.pack()
	#w = Scale(master, from_=0, to=200, orient=HORIZONTAL)
	

def bluetooth_menu_init():
	'''
	Contains the actual layout and code for the bluetooth media control menu
	'''
	#Define a new frame to hold the layout information
	global bluetooth_container
	bluetooth_container = tk.Frame()
	bluetooth_container.place(x=0, y=80, width=800, height=400) #Place under the menu bar with a size of 800x400
	bluetooth_container.place_forget() #Hide the container

	bluetooth_logo = tk.Label(bluetooth_container, image=bluetooth_icon).place(x=610, y=70) #Placeholder bluetooth icon

	#Define a form for the bluetooth device mac address entry. This is only temporary until we can detect connections
	#global bluetooth_address_entry
	#bluetooth_address_entry = tk.Entry(bluetooth_container)
	#bluetooth_address_entry.place(x=130, y=10, width=100, height=20)

	#Create a label for the bluetooth mac address entry
	labelText = ''

	if check_for_connected_devices():
		labelText = 'Connected to: ' + get_connected_device_name()
	else:
		#Define the button for the bluetooth device entry
		global bluetooth_address_set
		bluetooth_address_set = tk.Button(bluetooth_container, text='Connect', command=init_bt_device)
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
