'''
Tab class

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

class tab:
	def __init__(self, width, position, text, root, module):
		'''
		Create a new tab
		Reqires the width of the tab, the position in the list, the text that the tab will display, the TK root object, as well as the module associated with the tab.
		'''
		self.button = tk.Button(root, width=width, text=text, command=module.show)
		self.button.place(x=(width * position), y=0, height=80)
