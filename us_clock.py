#!/usr/bin/env py
"""Simple graphical implementation of a five-timezone US clock"""

import datetime as dt
import tkinter as tk
from tkinter import ttk
from typing import Final
from zoneinfo import ZoneInfo


class TimeZone:
    """A class that wraps together all the related time zone information."""

    __slots__ = ('name', 'city', 'info')

    def __init__(self, name: str, city: str) -> None:
        """Create a new time zone object using the given name and city."""
        self.name: str = name
        self.city: str = city
        city_with_underscores = city.replace(' ', '_')
        self.info: ZoneInfo = ZoneInfo(f'America/{city_with_underscores}')


# Set up the relevant time zones sorted from west to east
TIME_ZONES: Final[tuple[TimeZone, ...]] = (
    TimeZone('Pacific', 'Los Angeles'),
    TimeZone('Arizona', 'Phoenix'),
    TimeZone('Mountain', 'Denver'),
    TimeZone('Central', 'Chicago'),
    TimeZone('Eastern', 'New York'),
)

# ZoneInfo object to use for UTC
UTC_INFO: Final[ZoneInfo] = ZoneInfo('UTC')


class USClockApp:
    """A class that encapsulates the machinery of the Tkinter app."""

    __slots__ = ('root', 'clocks')

    def __init__(self, root: tk.Tk) -> None:

        # Grab control of the root window and fill it with a frame widget
        self.root: tk.Tk = root
        self.root.title('US Clock')
        frame = ttk.Frame(self.root)
        frame.grid(sticky='NSEW')

        # Set up graphical text labels for each time zone name
        for column, time_zone in enumerate(TIME_ZONES):
            label = ttk.Label(frame, text=time_zone.name)
            label.grid(column=column, row=0, sticky='S', padx=20, pady=(10, 5))

        # Set up graphical text labels for each clock display
        self.clocks: dict[str, tk.StringVar] = {}
        for column, time_zone in enumerate(TIME_ZONES):
            clock = tk.StringVar()
            label = ttk.Label(frame, textvariable=clock, justify="center")
            label.grid(column=column, row=1, sticky="N", pady=(5, 10))
            self.clocks[time_zone.name] = clock

        # Forbid resizing the window
        self.root.resizable(False, False)

        # Set styles for text and colors
        style = ttk.Style(self.root)
        style.configure("TFrame", background="black")
        style.configure(
            "TLabel", font=("Courier", 13),
            background="black", foreground="orange",
        )

        # Start the loop that updates the clocks
        self.update_clocks()

    # Define function that gets called every time the clocks need updating
    def update_clocks(self) -> None:

        # Get the current UTC date and time
        utc_time = dt.datetime.now(UTC_INFO)

        # Flash the colons in the clocks on or off once per second
        if utc_time.second % 2 == 0:
            format_str = '%I:%M %p\n%Z'
        else:
            format_str = '%I %M %p\n%Z'

        # Update all of the clock displays with the current time
        for time_zone in TIME_ZONES:
            current_time = utc_time.astimezone(time_zone.info)
            current_time_str = current_time.strftime(format_str).lstrip('0')
            self.clocks[time_zone.name].set(current_time_str)

        # Wait a bit and then trigger this update function again
        self.root.after(50, self.update_clocks)


if __name__ == '__main__':
    tkinter_root = tk.Tk()
    app = USClockApp(tkinter_root)
    tkinter_root.mainloop()
