'''
Bluetooth class

Made by Red in 2020
Greetings, from the ROC!

https://github.com/nlMeminger/MagiCarp

This code is licensed under the GNU General Public License
For more information see the LICENSE file that was distributed with this code
Or visit https://www.gnu.org/licenses/gpl-3.0.en.html
'''

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

class module:

	def __init__(self, root):
		'''
		Initialize the module
		The TK root object must be passed to initialize the object
		'''
		self.displayName = "Bluetooth"
		self.container = root.Frame() #Define the frame
		self.container.place(x=0, y=80, width=800, height=400) #Place the container to define the position and height
		self.container.place_forget() #Hide the container


		bluetooth_icon = tk.PhotoImage(file="bluetooth/interface_res/bluetooth.gif")


		#Track info icons
		artist_icon = tk.PhotoImage(file="bluetooth/interface_res/user-fill.gif").subsample(6,6)
		track_icon = tk.PhotoImage(file="bluetooth/interface_res/music-2-fill.gif").subsample(6,6)
		album_icon = tk.PhotoImage(file="bluetooth/interface_res/album-fill.gif").subsample(6,6)

		#Player control icons
		shuffle_icon = tk.PhotoImage(file="bluetooth/interface_res/shuffle-line.gif").subsample(3,3)
		shuffle_icon_on = tk.PhotoImage(file="bluetooth/interface_res/shuffle-line-enabled.gif").subsample(3,3)
		rewind_icon = tk.PhotoImage(file="bluetooth/interface_res/rewind-fill.gif").subsample(3,3)
		pause_icon = tk.PhotoImage(file="bluetooth/interface_res/pause-fill.gif").subsample(3,3)
		play_icon = tk.PhotoImage(file="bluetooth/interface_res/play-fill.gif").subsample(3,3)
		forward_icon = tk.PhotoImage(file="bluetooth/interface_res/speed-fill.gif").subsample(3,3)
		repeat_icon = tk.PhotoImage(file="bluetooth/interface_res/repeat-line.gif").subsample(3,3)
		repeat_icon_single = tk.PhotoImage(file="bluetooth/interface_res/repeat-line-all.gif").subsample(3,3)
		repeat_icon_multi = tk.PhotoImage(file="bluetooth/interface_res/repeat-line-1.gif").subsample(3,3)

		bluetooth_logo = tk.Label(self.container, image=bluetooth_icon).place(x=610, y=70) #Placeholder bluetooth icon

		#Define a form for the bluetooth device mac address entry. This is only temporary until we can detect connections
		bluetooth_address_entry = tk.Entry(self.container)
		bluetooth_address_entry.place(x=130, y=10, width=100, height=20)

		#Create a label for the bluetooth mac address entry
		bluetooth_address_text = tk.Label(self.container, text="Bluetooth Mac Address")
		bluetooth_address_text.place(x=0, y=10, height=20)

		#Define the button for the bluetooth device entry
		bluetooth_address_set = tk.Button(self.container, text='Set', command=init_bt_device)
		bluetooth_address_set.place(x=240, y=10, height=20)

		track_image = tk.Label(self.container, image=track_icon).place(x=5, y=60)
		artist_image = tk.Label(self.container, image=artist_icon).place(x=5, y=120)
		album_image = tk.Label(self.container, image=album_icon).place(x=5, y=180)

		#Define the text boxes for the song info
		track_info_font = tkfont.Font(size=24)
		self.track_name_text = tk.Label(self.container, text="", font=track_info_font)
		self.track_name_text.place(x=50, y=60)
		self.artist_name_text = tk.Label(self.container, text="", font=track_info_font)
		self.artist_name_text.place(x=50, y=120)
		self.album_name_text = tk.Label(self.container, text="", font=track_info_font)
		self.album_name_text.place(x=50, y=180)

		self.SHUFFLE_VALUE = False
		self.PLAYING = False
		self.LOOP_TYPE = 0

		self.shuffle_button = tk.Button(self.container, image=shuffle_icon, command=bt_shuffle_toggle)
		self.shuffle_button.place(x=15, y=300)
		
		rewind_button = tk.Button(self.container, image=rewind_icon, command=bt_back).place(x=105, y=300)
		
		self.playpause_button = tk.Button(self.container, image=play_icon, command=bt_playpause)
		self.playpause_button.place(x=195, y=300)
		
		forward_button = tk.Button(self.container, image=forward_icon, command=bt_forward).place(x=285, y=300)
		
		self.loop_button = tk.Button(self.container, image=repeat_icon, command=bt_loop)
		self.loop_button.place(x=375, y=300)

		song_position_font = tkfont.Font(size=15)

		self.current_position = tk.Label(self.container, text="0:00", font=song_position_font)
		self.current_position.place(x=15, y=250)
		
		self.progress_bar = ttk.Progressbar(self.container, orient="horizontal", length=470, mode="determinate")
		self.progress_bar.place(x=65, y=253)
		
		self.track_length = tk.Label(self.container, text="0:00", font=song_position_font)
		self.track_length.place(x=540, y=250)


		#Create a container to hide the content of the player until a device is connected
		self.nc_container = tk.Frame(self.container)
		self.nc_container.place(x=0, y=30, width=800, height=370)

		not_connected_font = tkfont.Font(size=40)
		nc_text = tk.Label(nc_container, text="No Bluetooth Device Connected", font=not_connected_font)
		nc_text.place(x=0, y=20)

	def show(self):
		'''
		Code to show the panel.
		'''
		self.place(x=0, y=80, width=800, height=400)


	def hide(self):
		'''
		Code to hide the panel.
		If the panel is playing media, it is recommended to pause the media.
		'''
		self.place_forget()

	# After the hide function, any other functions for the module can be defined.