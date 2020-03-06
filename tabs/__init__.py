'''
Tabs interface
Module to handle loading and processing of tab modules
Made by Red in 2020
Greetings, from the ROC!

https://github.com/nlMeminger/MagiCarp

This code is licensed under the GNU General Public License
For more information see the LICENSE file that was distributed with this code
Or visit https://www.gnu.org/licenses/gpl-3.0.en.html
'''

import flask
from flask import render_template

import tabs.loader


class tabHandler:
	'''
	Class to handle the initialization of tabs
	'''

	def __init__(self, config, app):
		'''
		Must pass the config file and the app instance to start the tab handler
		'''
		self.app = app
		self.config = config

		self.tabs = loader.getTabs(self.app, self.config)




		