#!/usr/bin/env py
"""Simple graphical implementation of a five-timezone US clock"""

import datetime as dt
import time  # For the sleep function
from zoneinfo import ZoneInfo

import graphics as gr  # Zelle's graphics for the GUI window


# Time zone class to wrap together all the related info
class TimeZone:
    def __init__(self, time_zone_name, time_zone_city):
        self.name = time_zone_name
        self.city = time_zone_city
        city_with_underscores = time_zone_city.replace(' ', '_')
        self.info = ZoneInfo(f"America/{city_with_underscores}")

# Set up the five time zones sorted from east to west
time_zones = [
    TimeZone("Eastern", "New York"),
    TimeZone("Central", "Chicago"),
    TimeZone("Mountain", "Denver"),
    TimeZone("Arizona", "Phoenix"),
    TimeZone("Pacific", "Los Angeles"),
]

# Open the window and make the background black
win = gr.GraphWin("US Clock", 100 * len(time_zones), 100, True)
win.setBackground("black")

# Set up graphical text labels for each time zone
for i, time_zone in enumerate(time_zones):
    x_coord = 100 * (len(time_zones) - i) - 50
    label = gr.Text(gr.Point(x_coord, 25), time_zone.name)
    label.setTextColor("orange")
    label.setFace("courier")
    label.draw(win)

# Set up graphical text objects for each clock display
time_zone_clocks = {}
for i, time_zone in enumerate(time_zones):
    x_coord = 100 * (len(time_zones) - i) - 50
    clock = gr.Text(gr.Point(x_coord, 60), "")
    clock.setTextColor("orange")
    clock.setFace("courier")
    clock.draw(win)
    time_zone_clocks[time_zone.name] = clock

# Infinite while loop to constantly update the time
while True:

    # Get the current UTC date and time
    utc_time = dt.datetime.now(dt.UTC)

    # Extract the current seconds value from the UTC time as an int
    seconds = int(utc_time.astimezone(ZoneInfo("UTC")).strftime("%S"))

    # Flash the colons in the clocks on or off once per second
    if seconds % 2 == 0:
        fmt = "%I:%M %p\n%Z"
    else:
        fmt = "%I %M %p\n%Z"

    for time_zone in time_zones:
        current_time = utc_time.astimezone(time_zone.info)
        current_time_str = current_time.strftime(fmt).lstrip('0')
        time_zone_clocks[time_zone.name].setText(current_time_str)

    # Wait a little to avoid taking up all the CPU resources
    time.sleep(0.05)

    # Break things off if the main window is ever closed
    if win.isClosed():
        break
