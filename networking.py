import subprocess
import config
import time
from profile import profile

def set_up_network():
    print('trying to set up network with provided username and password')
    got_acess = use_access_point()
    if not got_acess:
        profile.connect_button['spinning'] = False
        profile.connect_button['disabled'] = False
        profile.connect_button['active'] = False
        print('should  now be returning fail could not bring up interface at all')
        return

    print('testing if network setup worked using ping')
    if test_access():
        profile.connect_button['active'] = True
        profile.connect_button['spinning'] = False
        profile.connect_button['disabled'] = False
        print('we should now be connected')
        status = profile.export()
    else:
        profile.connect_button['spinning'] = False
        profile.connect_button['disabled'] = False
        profile.connect_button['active'] = False
        print('should  now be returning fail ping test did not work')


def set_access_point_info(network_name, password):
    connection_file = open(config.network_file_location, 'w')
    file_contents = '''ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={{
          ssid="{network_name}"
          psk="{password}"
          key_mgmt=WPA-PSK
        }}
    '''
    file_contents = file_contents.format(password=password,
                                         network_name=network_name)
    connection_file.write(file_contents)


def test_access():
    print('testing access/ping')
    try:
        p = subprocess.Popen(['/bin/ping', '-c', '1', '-I', 'wlan1', 'www.google.com'])
        p.wait()
    except subprocess.CalledProcessError:
        print('we do not have access')
        return False
    print('we have access/ping')
    return True


def use_access_point():
    print('trying to set up wlan1')
    try:
        #TODO clean up
        # will need to check return codes
        print('trying if down')
        p =  subprocess.Popen(['/sbin/ifdown "wlan1"'], shell=True)
        exit_status = p.wait()
        if exit_status != 0:
            print('ifdown failed')
        print('got passed ifdown')
        p = subprocess.Popen(['/sbin/ifup --force "wlan1"'], shell=True)
        exit_status = p.wait()
        if exit_status != 0:
            print('ifup failed')
        print('got passed ifup')

    except subprocess.CalledProcessError:
        print('ifdown or ifup failed can not use access point')
        return False

    print('wlan1 setup commands worked now checking if interface is really up')
    for _ in range(20):
        time.sleep(1)
        try:
            p = subprocess.Popen(['/sbin/ifconfig | /bin/grep "inet addr"'], shell=True, stdout=subprocess.PIPE)
            grep_output, grep_error = p.communicate()
            print(grep_output)
        except subprocess.CalledProcessError as error:
            print('subprocess gave exception when trying to check ifconfig')
            print("CalledProcessError ({0}): {1}".format(error.errno, error.strerror))
            return False

        if len(grep_output.splitlines()) > 2:
            print('ifconfig reports wlan1 is up with an ip')
            print(len(grep_output.splitlines()))
            return True

    print('after waiting 20 seconds if config still claims wlan1 is not working giving up')
    return False

def become_access_point():
    '''
    not currently used
    '''
    try:
        subprocess.check_call(['ifdown', 'wlan0'])
        time.sleep(1)
        subprocess.check_call(['ifup', 'wlan0'])
        time.sleep(1)
        subprocess.check_call(['hostapd', '-B', '/etc/hostapd/hostapd.conf'])
        time.sleep(1)
        subprocess.check_call(['service', 'dnsmasq', 'restart'])
        time.sleep(1)
        subprocess.check_call(['ifdown', 'wlan0'])
        time.sleep(1)
        subprocess.check_call(['ifup', 'wlan0'])
        time.sleep(1)
        subprocess.check_call(['service', 'dnsmasq', 'restart'])
    except subprocess.CalledProcessError:
        print('failed to swap to access point mode')
        return

    print('swap to access point mode appears to have worked')
