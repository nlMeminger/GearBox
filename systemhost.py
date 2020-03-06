import shlex
import subprocess

class SystemHost:

    currVolume = 0 #current Volume as a percent
    currBrightness = 0 #current Volume as a percent

    def __init__(self):
        #self.currVolume = self.getCurrVolume()
        self.currBrightness = self.getCurrBrightness()

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
        
        newBrightness = int(brightness) / 100

        if newBrightness <= 0 or newBrightness >= 1:
            return
        self.currBrightness = brightness

        self._commandRun(' xrandr --output eDP-1 --brightness {}'.format(newBrightness))
        
        #file = open("/sys/class/backlight/rpi_backlight/brightness","w")
        #file.write(str(brightness))
        #file.close()

    def getCurrBrightness(self):
        #results = self._commandRun('cat /sys/class/backlight/rpi_backlight/brightness')
        #currBrightness = int(results['stdout']) / 2.55
        
        #currBrightness = self._commandRun('xrandr --verbose |grep eDP-1 -A 5 | grep Brightness')
        #currBrightness = float(currBrightness['stdout'].split()[1].strip()) * 100
        return self.currBrightness

    def setVolume(self,volume_level):
        volume_level = int(volume_level)
        self.currVolume = volume_level
        self._commandRun('pactl set-sink-volume @DEFAULT_SINK@ {}%'.format(volume_level))

    def getCurrVolume(self):
        return self.currVolume

    def checkForConnectedDevices(self):
        results = self._commandRun('hcitool con')
        
        if '>' not in results['stdout']:
            return False
        else:
            return True

    def getConnectedDeviceName(self, macAddress):
        results = self._commandRun('hcitool info {} | grep Name'.format(macAddress))
        name = results['stdout'].replace('Device Name: ', '')
        return name


    def getSystemTime(self):
        pass

    def setSystemTime(self):
        pass