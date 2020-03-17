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
import json


def load_tabs(config, app):

	modules = []

	with open("MODULES.json") as f:
		toImport = json.load(f)

	for item in toImport["modules"]:
		modules.append(importlib.import_module("tabs." + item)) #import the item from the string
	
	for item in modules:
		app.register_blueprint(item.module)