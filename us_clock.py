#!/usr/bin/env python

# Simple graphical implementation of a five-timezone US clock

# Last modified 12/18/18 by Greg Vance

import pytz  # For timezone-handling functions
import datetime as dt  # To get the current UTC date and time
import graphics as gr  # Zelle's graphics for the GUI window
import time  # For the sleep function

# Set up the five timezones that I want
eastern = pytz.timezone("US/Eastern")
central = pytz.timezone("US/Central")
mountain = pytz.timezone("US/Mountain")
arizona = pytz.timezone("US/Arizona")
pacific = pytz.timezone("US/Pacific")

# Open the window and make the background black
win = gr.GraphWin("US Clock", 500, 100, True)
win.setBackground("black")

# Create label text for each of the five timezones
eastern_name = gr.Text(gr.Point(450, 25), "Eastern")
central_name = gr.Text(gr.Point(350, 25), "Central")
mountain_name = gr.Text(gr.Point(250, 25), "Mountain")
arizona_name = gr.Text(gr.Point(150, 25), "Arizona")
pacific_name = gr.Text(gr.Point(50, 25), "Pacific")

# Make the label text orange
eastern_name.setTextColor("orange")
central_name.setTextColor("orange")
mountain_name.setTextColor("orange")
arizona_name.setTextColor("orange")
pacific_name.setTextColor("orange")

# Draw the label text in the window
eastern_name.draw(win)
central_name.draw(win)
mountain_name.draw(win)
arizona_name.draw(win)
pacific_name.draw(win)

# Create text objects for each clock to be displayed
eastern_time = gr.Text(gr.Point(450, 60), "")
central_time = gr.Text(gr.Point(350, 60), "")
mountain_time = gr.Text(gr.Point(250, 60), "")
arizona_time = gr.Text(gr.Point(150, 60), "")
pacific_time = gr.Text(gr.Point(50, 60), "")

# Set the clock displays to the color orange too
eastern_time.setTextColor("orange")
central_time.setTextColor("orange")
mountain_time.setTextColor("orange")
arizona_time.setTextColor("orange")
pacific_time.setTextColor("orange")

# Change the font face to a monospace font
#eastern_time.setFace("courier")
#central_time.setFace("courier")
#mountain_time.setFace("courier")
#arizona_time.setFace("courier")
#pacific_time.setFace("courier")

# Draw the clock text in the window
eastern_time.draw(win)
central_time.draw(win)
mountain_time.draw(win)
arizona_time.draw(win)
pacific_time.draw(win)

# Infinite while loop to constantly update the time
while True:
	
	# Get the current UTC date and time
	utc_dt = pytz.utc.localize(dt.datetime.utcnow())
	
	# Extract the current seconds value from the UTC time as an int
	seconds = int(utc_dt.astimezone(pytz.utc).strftime("%S"))
	
	# Flash the colons in the clocks on or off once per second
	if seconds % 2 == 0:
		fmt = "%I:%M %p\n%Z"
	else:
		fmt = "%I %M %p\n%Z"
	
	# Calculate the time in each timezone from the UTC time
	eastern_dt = utc_dt.astimezone(eastern)
	central_dt = utc_dt.astimezone(central)
	mountain_dt = utc_dt.astimezone(mountain)
	arizona_dt = utc_dt.astimezone(arizona)
	pacific_dt = utc_dt.astimezone(pacific)
	
	# Format each of the clock text strings with the current time
	eastern_str = eastern_dt.strftime(fmt)
	central_str = central_dt.strftime(fmt)
	mountain_str = mountain_dt.strftime(fmt)
	arizona_str = arizona_dt.strftime(fmt)
	pacific_str = pacific_dt.strftime(fmt)
	
	# Remove any leading zeros on the hour in the times
	eastern_str = eastern_str.lstrip('0')
	central_str = central_str.lstrip('0')
	mountain_str = mountain_str.lstrip('0')
	arizona_str = arizona_str.lstrip('0')
	pacific_str = pacific_str.lstrip('0')
	
	# Update the text clock objects with the new time
	eastern_time.setText(eastern_str)
	central_time.setText(central_str)
	mountain_time.setText(mountain_str)
	arizona_time.setText(arizona_str)
	pacific_time.setText(pacific_str)
	
	# Wait a little to avoid taking up all the CPU resources
	time.sleep(0.05)
	
	# Break things off if the main window is ever closed
	if win.isClosed():
		break

