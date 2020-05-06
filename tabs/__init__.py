'''
Tab loader
Module to handle loading of tab files from extension files
Made by Red in 2020
Greetings, from the ROC!

https://github.com/nlMeminger/MagiCarp

This code is licensed under the GNU General Public License
For more information see the LICENSE file that was distributed with this code
Or visit https://www.gnu.org/licenses/gpl-3.0.en.html
'''

import importlib
import os
import json

modules = [] #Global modules list

def load_tabs(config, app):

	global modules
	
	registered_pages = []

	with open("MODULES.json") as f:
		#Open the modules file
		toImport = json.load(f)

	for item in toImport["modules"]:
		# Check duplicate names, as well as template filenames.

		#Check for duplicate module names		
		if item in modules:
			raise DuplicateModuleError("Module " + item + " is already registered")
		else:
			modules.append(importlib.import_module("tabs." + item)) #import the item from the string
			#Check for duplicate file names.
			for file in os.listdir("tabs/" + item + "/templates"):
				if file in registered_pages:
					print("Page " + file + "in module " + item + " is already registered by another module. This may cause collision errors.")
				else:
					registered_pages.append(file)
				
	for item in modules:
		app.register_blueprint(item.module)