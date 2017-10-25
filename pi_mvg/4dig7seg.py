#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################
# Starting the internet part
from .core import MVGTracker, mvg_pars_factory
import RPi.GPIO as GPIO
import time
import os

# Using BCM pin numbering
GPIO.setmode(GPIO.BCM)
segments = (21, 16, 19, 6, 5, 20, 26, 13)  # 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
digits = (2, 3, 4, 14)

# Set as outputs
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

num = {' ':  (0, 0, 0, 0, 0, 0, 0),
       '0':  (1, 1, 1, 1, 1, 1, 0),
       '1':  (0, 1, 1, 0, 0, 0, 0),
       '2':  (1, 1, 0, 1, 1, 0, 1),
       '3':  (1, 1, 1, 1, 0, 0, 1),
       '4':  (0, 1, 1, 0, 0, 1, 1),
       '5':  (1, 0, 1, 1, 0, 1, 1),
       '6':  (1, 0, 1, 1, 1, 1, 1),
       '7':  (1, 1, 1, 0, 0, 0, 0),
       '8':  (1, 1, 1, 1, 1, 1, 1),
       '9':  (1, 1, 1, 1, 0, 1, 1),
       's:': (1, 0, 1, 1, 0, 1, 1)}


class FourDigSevSeg(MVGTracker):
    def __init__(self, mvg_pars, screen_timeout=1, update_interval=30):
        self.screen_timeout = screen_timeout

        super(FourDigSevSeg, self).__init__(mvg_pars=mvg_pars, update_interval=update_interval)

    @staticmethod
    def one_result(station,
                   transports=[],
                   destination=[],
                   max_time=None,
                   min_time=None,
                   screen_timeout=1,
                   update_interval=30):
        mvg_pars = mvg_pars_factory(
                station, line=transports, destination=destination, max_time=max_time, min_time=min_time)
        return FourDigSevSeg(mvg_pars=mvg_pars, screen_timeout=screen_timeout, update_interval=update_interval)

    def display_string(self):
        r = []
        for fr in self.mvg_filtered_results:
            r += [row['line'] + ' ' + unicode(row['minutes']) for row in fr]

        return r

    def display(self):
        OFF_time = time.time()+self.screen_timeout*60
        try:
            while (time.time()<OFF_time):
                # os.system('sudo shutdown -h now')

                s = self.display_string

                for digit in range(4):
                    for loop in range(0, 7):
                        GPIO.output(segments[loop], num[s[digit]][loop])
                    GPIO.output(digits[digit], 0)
                    time.sleep(0.001)
                    GPIO.output(digits[digit], 1)
        finally:
            GPIO.cleanup()

if __name__ == "__main__":

    pi_mvg = FourDigSevSeg.one_result(station='Olympiazentrum',
                                        transports=['u'],
                                        destination=['Fürstenried West'],
                                        screen_timeout=1,
                                        update_interval=5)

    pi_mvg.display()