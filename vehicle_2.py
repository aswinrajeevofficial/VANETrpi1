from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sched,time
import os
import threading
from geopy.distance import geodesic
import socket

pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-cbac1ba8-84b2-469d-a59b-7d66d9b4cb2a'
pnconfig.subscribe_key = 'sub-c-88b6488e-3adb-11eb-b6eb-96faa39b9528'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
   # Check whether request successfully completed or not
    if not status.is_error():
        pass
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        print("From Traffic Signal: ",message.message)
        if(message.message == "RED"):
            stop_moving()
        if(message.message == "ORANGE"):
            slow_moving()
        if(message.message == "GREEN"):
            continue_moving()

#Traffic Signal 1 Lattitude
signal_coords = [53.369673,-6.254447]
vehicle_1_start_coords = [53.368020,-6.255396]
vehicle_1_stop_coords = [53.370812, -6.253679]

def continue_moving():
    print("Vehicle continuing moving")
    pubnub.unsubscribe().channels("signal-1").execute()
    while(vehicle_1_start_coords[0] <= vehicle_1_stop_coords[0] and vehicle_1_start_coords[1] <= vehicle_1_stop_coords[1]):
        vehicle_1_start_coords[0] += 0.00001
        vehicle_1_start_coords[1] -= 0.00001
        print("Current Coordinates", vehicle_1_start_coords[0],vehicle_1_start_coords[1])
        time.sleep(0.5)

def stop_moving():
    print("Vehicle Stopped")

def slow_moving():
    print("Vehicle decclerating/accelerating")

def moving_vehicle():
    while((geodesic(vehicle_1_start_coords,signal_coords).m) > 45):
        print("Distance to signal (metres): ",geodesic(vehicle_1_start_coords,signal_coords).m)
        time.sleep(0.5)
        vehicle_1_start_coords[0] = round((vehicle_1_start_coords[0] + 0.0001),6)
        vehicle_1_start_coords[1] = round((vehicle_1_start_coords[1] + 0.0001),6)
        print("Current Coordinates", vehicle_1_start_coords[0],vehicle_1_start_coords[1])
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels("signal-1").execute()
moving_vehicle()
