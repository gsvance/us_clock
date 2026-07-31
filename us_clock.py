#!/usr/bin/env py
"""Simple graphical implementation of a five-timezone US clock"""

import pytz  # For timezone-handling functions
import datetime as dt  # To get the current UTC date and time
import graphics as gr  # Zelle's graphics for the GUI window
import time  # For the sleep function


# Set up the five time zones and time zone info objects
time_zone_names = ["Eastern", "Central", "Mountain", "Arizona", "Pacific"]
time_zones = {name: pytz.timezone(f"US/{name}") for name in time_zone_names}

# Open the window and make the background black
win = gr.GraphWin("US Clock", 100 * len(time_zone_names), 100, True)
win.setBackground("black")

# Set up graphical text labels for each time zone
for i, name in enumerate(time_zone_names):
    x_coord = 100 * (len(time_zone_names) - i) - 50
    label = gr.Text(gr.Point(x_coord, 25), name)
    label.setTextColor("orange")
    label.setFace("courier")
    label.draw(win)

# Set up graphical text objects for each clock display
time_zone_clocks = {}
for i, name in enumerate(time_zone_names):
    x_coord = 100 * (len(time_zone_names) - i) - 50
    clock = gr.Text(gr.Point(x_coord, 60), "")
    clock.setTextColor("orange")
    clock.setFace("courier")
    clock.draw(win)
    time_zone_clocks[name] = clock

# Infinite while loop to constantly update the time
while True:

    # Get the current UTC date and time
    utc_time = dt.datetime.now(dt.UTC)

    # Extract the current seconds value from the UTC time as an int
    seconds = int(utc_time.astimezone(pytz.utc).strftime("%S"))

    # Flash the colons in the clocks on or off once per second
    if seconds % 2 == 0:
        fmt = "%I:%M %p\n%Z"
    else:
        fmt = "%I %M %p\n%Z"

    for name in time_zone_names:
        current_time = utc_time.astimezone(time_zones[name])
        current_time_str = current_time.strftime(fmt)
        current_time_str = current_time_str.lstrip('0')
        time_zone_clocks[name].setText(current_time_str)

    # Wait a little to avoid taking up all the CPU resources
    time.sleep(0.05)

    # Break things off if the main window is ever closed
    if win.isClosed():
        break
