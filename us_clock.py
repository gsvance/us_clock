#!/usr/bin/env py
"""Simple graphical implementation of a five-timezone US clock"""

import datetime as dt
import tkinter as tk
from tkinter import ttk
from zoneinfo import ZoneInfo


# Time zone class to wrap together all the related info
class TimeZone:
    def __init__(self, time_zone_name, time_zone_city):
        self.name = time_zone_name
        self.city = time_zone_city
        city_with_underscores = time_zone_city.replace(' ', '_')
        self.info = ZoneInfo(f"America/{city_with_underscores}")


# Set up the five time zones sorted from west to east
time_zones = [
    TimeZone("Pacific", "Los Angeles"),
    TimeZone("Arizona", "Phoenix"),
    TimeZone("Mountain", "Denver"),
    TimeZone("Central", "Chicago"),
    TimeZone("Eastern", "New York"),
]


class USClockApp:

    def __init__(self, root):

        # Create the root window and fill it with a frame widget
        root.title("US Clock")
        frame = ttk.Frame(root)
        frame.grid(sticky="NSEW")

        # Set up graphical text labels for each time zone name
        for column, time_zone in enumerate(time_zones):
            label = ttk.Label(frame, text=time_zone.name)
            label.grid(column=column, row=0, sticky="S", padx=20, pady=(10, 5))

        # Set up graphical text labels for each clock display
        self.time_zone_clocks = {}
        for column, time_zone in enumerate(time_zones):
            clock = tk.StringVar()
            label = ttk.Label(frame, textvariable=clock, justify="center")
            label.grid(column=column, row=1, sticky="N", pady=(5, 10))
            self.time_zone_clocks[time_zone.name] = clock

        # Forbid resizing the window at all
        root.resizable(False, False)

        # Set styles for text and colors
        style = ttk.Style(root)
        style.configure("TFrame", background="black")
        style.configure(
            "TLabel", font=("Courier", 13),
            background="black", foreground="orange",
        )

        # Save the root and start the loop that updates the clocks
        self.root = root
        self.update_clocks()

    # Define function that gets called every time the clocks need updating
    def update_clocks(self, *args):

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
            self.time_zone_clocks[time_zone.name].set(current_time_str)

        # Wait a bit and then trigger this update function again
        self.root.after(50, self.update_clocks)


if __name__ == '__main__':
    root = tk.Tk()
    app = USClockApp(root)
    root.mainloop()
