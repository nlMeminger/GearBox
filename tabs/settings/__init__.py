'''
Settings tab
Made by Red in 2020
Greetings, from the ROC!

https://github.com/nlMeminger/MagiCarp

This code is licensed under the GNU General Public License
For more information see the LICENSE file that was distributed with this code
Or visit https://www.gnu.org/licenses/gpl-3.0.en.html
'''

from flask import Blueprint, render_template
import json
import redis



NAME = "settings"


module = Blueprint(NAME, __name__, template_folder='templates', static_folder='static')
red = redis.StrictRedis() #Listen for redis events

@module.route("/settings")
def show():
	#Show the tab. This should contain all the necessary setup before the template is rendered.
	return render_template("settings.html", settings = settings)

def hide():
	#Hide the tab.
	#Contains functions that the tab should run on switching to another tab.
	#This should do stuff like closing open files, etc.
	#This will be left as pass for most tabs.
	pass

def sever_msg(data):
	#Send a string to the server_msg stream. This is used to send data to the client.
	red.publish('server_msg', u'%s' % (data))

def hide_tab(name):
	#Hide another tab
	#send "ALL" to hide all tabs.
	red.publish('server_msg', name)

def hide_stream(): 
	#Subscribe to the hide stream
	pubsub = red.pubsub()
	pubsub.subscribe('hide') #subscribe to hide stream
	for message in pubsub.listen():
		if message == "ALL":
			#Listen to the ALL stream
			hide()
		elif message == NAME:
			hide()
		

#Arbitrary functions for this particular module
def change_config(key, value):
	#Change the config option key to the specified value.
	#Writes directly to the config file.

	with open("CONFIG.json", "w") as f:
		configuration = json.load(f)
		configuration[key] = value
		json.dumps(configuration, f, indent=4)


#Required functions to make the module run

#Open the config.json file
with open("CONFIG.json") as f:
		settings = json.load(f)

hide_stream() #Subscribe to the hide events stream.