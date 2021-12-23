# -*- coding: utf-8 -*-
"""
Created on Mon May 10 00:55:47 2021

@author: Alexander Merolla
"""

import time
from time import sleep
from rpi_ws281x import PixelStrip, Color
import argparse
import spclass

def draw_bar(start_led, end_led, rows, db):
    num_leds = end_led - start_led + 1
    if num_leds <= 0:
        return None
    modby = num_leds // rows
    if db > 1:
        db = 1
    height = modby * db
    height = height // 1
    mod_color = int(db*255)
    for i in range(start_led, end_led + 1):
        if i != 0 and i % modby == 0:
            height += modby
        if i < height:
            strip.setPixelColor(i, Color(mod_color,200-(200-mod_color),255-mod_color))
        else:
            strip.setPixelColor(i, Color(0,0,0))
    strip.show()

def colorWipe():
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    

# LED strip configuration for Raspberry Pi 3B:
LED_COUNT = 64        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 30  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

test = spclass.sp('alecmerolla')

while True:
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    beat_gen = test.beat_bar()
    while test.is_Playing() == True and test.songID != None:
        test.update()
        draw_bar(0,63,8,next(beat_gen))
        sleep(50/1000)
    
    colorWipe()
        
    # Let's wait and check every second until another song is played
    while test.is_Playing() == False:
        test.update()
        sleep(1)