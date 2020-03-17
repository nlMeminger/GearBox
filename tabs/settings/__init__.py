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

module = Blueprint('settings', __name__, template_folder='html', static_folder='static')

@module.route("/settings")
def show():
	return render_template("settings.html")