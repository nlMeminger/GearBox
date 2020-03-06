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

from tabs.MODULES import TABS as toImport


def getTabs(config, app):

	tabs = []
	modules = []

	for item in toImport:
		modules.append(importlib.import_module("tabs." + item)) #import the item from the string
	
	for item in modules:
		tabs.append(item.register(config, app))

	return tabs