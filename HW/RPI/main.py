#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 3      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PINS       = [12, 18, 40, 52]      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PINS       = [12, 18]      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    strips = []
    for ledPin in LED_PINS:
        print(ledPin)
        # Create NeoPixel object with appropriate configuration.
        strips.append(Adafruit_NeoPixel(LED_COUNT, ledPin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL))
        # Intialize the library (must be called once before other functions).
        strips[-1].begin()

    print(strips)
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        print ('  *-*  Simulation started!  *-*  ')
        while True:
     	    print('TL0: Green! Go!')
	    print('TL1: Red! Stop!')
            colorWipe(strips[0], Color(255, 0, 0))  # Green wipe
            colorWipe(strips[1], Color(0, 255, 0))  # Red wipe
            #setColor(strips[1], Color(0, 255, 0))  # Red wipe
	    time.sleep(10)
	    print('TL0: Yellow! Break!')
	    print('TL1: Yellow! Break!')
            colorWipe(strips[0], Color(255,255,0))  # Yellow wipe
            colorWipe(strips[1], Color(255,255,0))  # Yellow wipe
	    time.sleep(2)
	    print('TL0: Red! Stop!')
     	    print('TL1: Green! Go!')
            colorWipe(strips[0], Color(0, 255, 0))  # Red wipe
            colorWipe(strips[1], Color(255, 0, 0))  # Green wipe
	    time.sleep(10)
 	    print('TL0: Yellow! Get ready!')
 	    print('TL1: Yellow! Get ready!')
	    colorWipe(strips[0], Color(255,255,0))  # Yellow wipe
            colorWipe(strips[1], Color(255,255,0))  # Yellow wipe
	    time.sleep(2)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
