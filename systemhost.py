import shlex
import subprocess
import yaml


class SystemHost:

    currVolume = 0 #current Volume as a percent
    currBrightness = 0 #current Volume as a percent
    configFile = 'config.yml'

    def __init__(self):
        #self.currVolume = self.getCurrVolume()
        self.currBrightness = self.getCurrBrightness()
        #config = yaml.safe_load(os.environ.get("CONFIGPATH", open("config.yml"))) 

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
        
        #newBrightness = int(brightness) / 100
        newBrightness = float(brightness) * 9.37
        newBrightness = int(newBrightness)
        if newBrightness <= (5 * 9.37) or newBrightness > 937:
            return

        self.currBrightness = brightness

        #self._commandRun(' xrandr --output eDP-1 --brightness {}'.format(newBrightness))
        
        file = open("/sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-eDP-1/intel_backlight/brightness", "w")
        #file = open("/sys/class/backlight/rpi_backlight/brightness","w")
        file.write(str(newBrightness))
        file.close()

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
        
        if '<' not in results['stdout']:
            return False
        else:
            return True

    def getConnectedDeviceMac(self):
        results = self._commandRun('hcitool con')

        device = results['stdout'].strip().split()
        deviceMac = device[3]
        print(deviceMac)
        return deviceMac

    def getConnectedDeviceName(self, macAddress = ''):

        if macAddress == '':
            macAddress = self.getConnectedDeviceMac()

        results = self._commandRun('hcitool info {} | grep Name'.format(macAddress))
        name = results['stdout'].replace('Device Name: ', '')
        return name

    def connnectToDevice(self, mac):
        command = "rfcomm connect hci0 {} &".format(mac)
        results = self._commandRun(command)

        for i in results:
            print(i)

        if self.checkForConnectedDevices():
            print('got one!')
        else:
            print('boo')

    def getSystemTime(self):
        pass

    def setSystemTime(self):
        pass