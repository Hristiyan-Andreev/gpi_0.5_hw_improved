import time
from threading import Timer
import liveapi
import config as cf

# Time measurement class
class TimeMeasure():
    start_time = 0
    end_time = 0

    def __init__(self):
        self.start_time = time.time()
        self.end_time = time.time()

    def start_measure(self):
        self.start_time = time.time()

    def end_measure(self):
        self.end_time = time.time() - self.start_time

    def print_measure(self, msg = "Time measured: "):
        print(msg + str(self.end_time))


# GPI to Stream class with more information
class GpiStream:
    stream_id = '0'
    in_cue = False
    channel_locked = False
    
    def __init__(self, id):
        self.stream_id = id
        
    def __str__(self):
        return "GPI: {} str_id: {} in_cue: {}".format(self.gpi_input, self.stream_id, self.in_cue)
        
    def update_info(self, stream):
        self.in_cue = stream.in_cue
        
    def start_cue(self, elemental_ip = cf.elemental_ip):
        if self.channel_locked is not True:
            response = liveapi.cue_command(elemental_ip, self.stream_id, 'start_cue')
            self.in_cue = True
            lock_channel(cf.lock_interval)
            return response
        else:
            return "Channel is locked"
        
    def stop_cue(self, elemental_ip = cf.elemental_ip):
        if self.channel_locked is not True:
            response = liveapi.cue_command(elemental_ip, self.stream_id, 'stop_cue')
            self.in_cue = False
            return response
        else:
            return "Channel is locked"

    def lock_channel(self, lock_interval):
        self.channel_locked = True
        unlock_timer = Timer(lock_interval, unlock_channnel)
        unlock_timer.start()

    def unlock_channnel(self):
        self.channel_locked = False