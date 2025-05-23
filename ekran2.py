#! /usr/bin/env python
# Import necessary libraries for communication and display use
import drivers
from time import sleep

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()

# Main body of code
try:
    while True:
        # Remember that your sentences can only be 16 characters long!
        print("Selam Turbish!")
        display.lcd_display_string("Selam Turbis!", 1)  # Write line of text to first line of display
        display.lcd_display_string("Ben Kumfiris!", 2)  # Write line of text to second line of display
        sleep(2)                                           # Give time for the message to be read
        display.lcd_display_string("Yine gel emi!", 1)   # Refresh the first line of display with a different message
        sleep(2)                                           # Give time for the message to be read
        display.lcd_clear()                                # Clear the display of any data
        sleep(2)                                           # Give time for the message to be read
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()


# Simple string program. Writes and updates strings.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel