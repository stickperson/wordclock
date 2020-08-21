# Wordclock
Instructions how to make this:

![alt tag](clock.jpg)

# Introduction
I've made this clock two times. Trying a third time with a raspberry pi. Here are my notes.

# Contents
* [Frame Construction](#frame-construction)
* [Electronics](#electronics)
* [Software](#software)
    * [Arduino](#arduino)
    * [Raspberry Pi](#raspberry-pi)
* [Notes](#notes)


# Frame Construction
Parts list:
* 12" x 12" 1/8" plywood (x3) for the face, back, and grid.
* 12" x 12" acrylic (need to figure out how opaque). Make sure you get acrylic and not the toxic stuff. These pieces will sit in the grid which 1) prevents light from leaking out and 2) diffuses the light across the entire letter.
* Get dimensions for walnut

The frame of the clock consists of the following parts:
* Laser cut face
* Laser cut grid which should be glued to the back of the face
* Laser cut acylic pieces that fit into the grid. Should be glued carefully to the back of the letters
* Laser cut back
* Walnut sides

Files for the laser cut parts are in the `lasercut` folder. I need to double check some stuff.


# Electronics
Parts list:
* APA 102 LED strip 60/m
* Arduino UNO or Raspberry Pi Zero W
* 9-12V, 1.5A power supply (see notes below)
* Push buttons (x3)

If you use an Arduino you will need the following:
* Buck converter

If you use a Raspberry Pi you will need the following:
* Logic level converter

# Software
## Arduino
Software + wiring notes
## Raspberry Pi
Software + wiring notes

Why use a raspberry pi? Wifi + code updates.

Steps:
* Systemd unit to check if wifi connected/listen for wps. See [this gist](https://gist.github.com/stickperson/354e79bf5e2af848f8ae7f6a88e5080f) for inspiration

# Notes
TODO. Power consumption notes.