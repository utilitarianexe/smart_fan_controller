import threading
import multiprocessing
import time
import json
import signal
import sys
import os

from flask import Flask, request

import config
import datetime
import hardware
from sensor import sensor
import outside_data
import networking
from profile import profile


'''
'''
network_test_info = 'not_done'
application = Flask(__name__, static_url_path='')
application.debug = False
hardware = hardware.Hardware(profile)
lock = threading.Lock()

def update_data():
    profile.inside_temp = str(sensor.get_inside_temp())    
    if profile.lon is not None and profile.lat is not None and profile.connect_button['active']:
        #TODO excepiton
        profile.outside_temp = str(outside_data.get_outside_temp(profile.lat, profile.lon))
        if profile.set_temperature_preferences_button['active'] and not profile.turn_automatic_mode_on_button['active']:
            profile.turn_automatic_mode_on_button['disabled'] = False

@application.route("/hard_reset")
def hard_reset():
    turn_fan_off()
    profile.hard_reset()
    return get_status()

@application.route("/get_status")
def get_status():
    update_data()
    status = profile.export()
    profile.save_state()
    return json.dumps(status)

@application.route("/")
def start():
    return application.send_static_file('page.html')


@application.route('/set_location', methods=['POST'])
def set_location():
    lat = request.form['lat']
    lon = request.form['lon']
    profile.lat = lat
    profile.lon = lon
    profile.set_location_button['active'] = True
    return get_status()

@application.route('/set_temperature_preferences', methods=['POST'])
def set_temperature_preferences():
    min_temp = request.form['min_temp']
    temp_margin = request.form['temp_margin']
    min_cycle_time = request.form['min_cycle_time']

    profile.min_cycle_time = min_cycle_time
    profile.min_temp = min_temp
    profile.temp_margin = temp_margin
    profile.set_temperature_preferences_button['active'] = True
    status = get_status()
    return status

@application.route('/connect', methods=['POST'])
def connect():
    password = request.form['password']
    network_name = request.form['network_name']
    profile.password = password
    profile.network_name = network_name
    profile.connect_button['active'] = False
    profile.connect_button['spinning'] = True
    profile.connect_button['disabled'] = True
    networking.set_access_point_info(network_name, password)
    thread = threading.Thread(target=networking.set_up_network, name='check_info')
    thread.start()
    return 'bla'

@application.route("/network_status")
def network_status():
    status = get_status()
    return status

@application.route("/turn_fan_on")
def turn_fan_on():
    lock.acquire()
    profile.turn_fan_on_button['active'] = True
    profile.turn_automatic_mode_on_button['active'] = False
    profile.turn_fan_off_button['active'] = False
    profile.connect_button['disabled'] = False
    profile.set_location_button['disabled'] = False
    profile.set_temperature_preferences_button['disabled'] = False
    profile.mode = "manual on"
    hardware.turn_fan_on()
    status = get_status()
    lock.release()
    return status


@application.route("/turn_fan_off")
def turn_fan_off_endpoint():

    status = turn_fan_off()
    return status

def turn_fan_off():
    lock.acquire()
    profile.turn_fan_on_button['active'] = False
    profile.turn_automatic_mode_on_button['active'] = False
    profile.turn_fan_off_button['active'] = True
    profile.connect_button['disabled'] = False
    profile.set_location_button['disabled'] = False
    profile.set_temperature_preferences_button['disabled'] = False
    profile.mode = "manual off"
    hardware.turn_fan_off()
    status = get_status()
    lock.release()
    return status

@application.route("/turn_automatic_mode_on")
def turn_automatic_mode_on_end_point():
    lock.acquire()
    turn_automatic_mode_on()
    status = get_status()
    lock.release()
    return status

def turn_automatic_mode_on():
    profile.turn_automatic_mode_on_button['active'] = True
    profile.turn_automatic_mode_on_button['disabled'] = True
    profile.turn_fan_on_button['active'] = False
    profile.turn_fan_off_button['active'] = False
    profile.connect_button['disabled'] = True
    profile.set_location_button['disabled'] = True
    profile.set_temperature_preferences_button['disabled'] = True
    profile.mode = "automatic"
    t = threading.Thread(target=run_automatic_mode, name='check_info')
    t.start()

def run_automatic_mode():
    '''
    '''
    while True:
        lock.acquire()
        lat = profile.lat
        lon = profile.lon
        if not profile.turn_automatic_mode_on_button['active']:
            lock.release()
            break
        try:
            outside_temp = outside_data.get_outside_temp(lat, lon)
            inside_temp = sensor.get_inside_temp()
        except:
            turn_fan_off()
            lock.release()
            break
        inside_temp = float(inside_temp)
        outside_temp = float(outside_temp)
        if config.record_temp:
            record_temp(inside_temp, outside_temp)
        cooler_outside = outside_temp < inside_temp - float(profile.temp_margin)
        if cooler_outside and inside_temp > float(profile.min_temp):
            hardware.turn_fan_on()
        else:
            hardware.turn_fan_off()
        lock.release()
        time.sleep(float(profile.min_cycle_time))

def record_temp(inside_temp, outside_temp):
    with open(config.temperature_file_path, 'a') as temp_file:
        temp_data = {'inside_temp': inside_temp,
                     'outside_temp': outside_temp,
                     'time': str(datetime.datetime.utcnow()),
                     'state': profile.fan_state,
                 }
        temp_data = json.dumps(temp_data)
        temp_file.write(temp_data + '\n')


def handle_boot():
    # make sure connection still works
    if profile.connect_button['active']:
        networking.set_up_network()

    if profile.turn_automatic_mode_on_button['active']:
        if profile.connect_button['active']:
            turn_automatic_mode_on()
        else: # reconnecting after reboot failed so swap to off mode
            turn_fan_off()
    elif profile.turn_fan_on_button['active']:
        turn_fan_on()
    else:
        turn_fan_off()

handle_boot()



if __name__ == "__main__":
    pass
    #application.run(host='0.0.0.0', debug=True)

