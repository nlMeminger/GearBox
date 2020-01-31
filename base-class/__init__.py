'''
This file contains a base/example class for a module for a "tab" for the Stereo
GUI program. It contains a standard set of functions and variables that are
required for the tab to function correctly. Use this as an example when creating
new modules.

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
		self.displayName = "Display Name"
		self.container = root.Frame() #Define the frame
		self.container.place(x=0, y=80, width=800, height=400) #Place the container to define the position and height
		self.container.place_forget() #Hide the container

		# Here we define the objects that make up the layout of the container

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