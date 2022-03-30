import math
import signal
import sys
import time
import csv
import threading as th
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from datetime import datetime
from cflib.utils import uri_helper


class FlapperController:
    def __init__(self) -> None:
        self._cf = Crazyflie(rw_cache='./cache')
        # initialize when connected to drone
        self._cf.connected.add_callback(self._connected())
        # callbacks
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)
        # Initial position
        self.init_pos = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'yaw': math.radians(0)}
        self.kill_flight = False
        self.connected = False

        self.uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')
        # connect
        self._cf.open_link(self.uri)
        print('Connecting to %s' % self.uri)

    def activate_high_level_commander(self):
        self._cf.param.set_value('commander.enHighLevel', '1')

    def _connection_failed(self, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        self.connected = False
        print('Connection to %s failed: %s' % (self.uri, msg))

    def _connection_lost(self, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        self.connected = False
        print('Connection to %s lost: %s' % (self.uri, msg))

    def _disconnected(self):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        self.connected = False
        print('Disconnected from %s' % self.uri)

    def _connected(self):
        self.connected = True
        print('connected to %s' % self.uri)

    def set_initial_position(self):
        self._cf.param.set_value('kalman.initialX', self.init_pos['x'])
        self._cf.param.set_value('kalman.initialY', self.init_pos['y'])
        self._cf.param.set_value('kalman.initialZ', self.init_pos['z'])
        self._cf.param.set_value('kalman.initialYaw', self.init_pos['yaw_radians'])

    def take_off(self, h=0.5, duration=3.0):
        commander = self._cf.high_level_commander
        commander.takeoff(self.init_pos['z'] + h, duration)

    def emergency_land(self):
        commander = self._cf.high_level_commander
        commander.land(self.init_pos['z'], 3)

    def signal_handler(self, sig, frame):
        self.kill_flight = True
        self.emergency_land()
        sys.exit(0)

    def main_process(self):
        with SyncCrazyflie(self.uri, cf=self._cf) as scf:
            signal.signal(signal.SIGINT, self.signal_handler)
            self.set_initial_position()
            self.activate_high_level_commander()
            self.take_off()
            time.sleep(3)
            self.emergency_land()


if __name__ == '__main__':
    cflib.crtp.init_drivers()
    flapper = FlapperController()
    flapper.main_process()
