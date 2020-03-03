import shlex
import subprocess

class SystemHost:

    def __init__(self):
        pass

    def _commandRun(self,command):
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

    def setBrightness(self,brightness):

        brightness = int(brightness) / 100

        #print(brightness)

        self._commandRun(' xrandr --output eDP-1 --brightness {}'.format(brightness))
        
        #file = open("/sys/class/backlight/rpi_backlight/brightness","w")
        #file.write(str(brightness))
        #file.close()

    def getCurrBrightness(self):
        #results = self._commandRun('cat /sys/class/backlight/rpi_backlight/brightness')
        #currBrightness = int(results['stdout']) / 2.55
        
        currBrightness = self._commandRun('xrandr --verbose |grep eDP-1 -A 5 | grep Brightness')
        currBrightness = float(currBrightness['stdout'].split()[1].strip()) * 100

        return currBrightness

    def setVolume(self,volume_level):
        volume_level = int(volume_level) * 1000
        self._commandRun('pactl set-sink-volume @DEFAULT_SINK@ {}'.format(volume_level))

    def getCurrVolume(self):
        pass

    def checkForConnectedDevices(self):
        results = self._commandRun('hcitool con')
        
        if '>' not in results['stdout']:
            return False
        else:
            return True

    def getConnectedDeviceName(self):
        results = self._commandRun('hcitool info {} | grep Name'.format(get_connected_mac()))
        name = results['stdout'].replace('Device Name: ', '')
        return name


    def getSystemTime(self):
        pass

    def setSystemTime(self):
        pass