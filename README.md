# Wordclock
:construction: **Under Construction** :construction:

Instructions how to make this:

![alt tag](clock.jpg)

# Introduction
I've made this clock two times. Trying a third time with a raspberry pi. Here are my notes.

# Contents
* [Materials](#materials)
    * [Frame Construction](#frame-construction)
        * [Parts](#parts)
        * [Laser Cutter](#laser-cutter)
    * [Electronics](#electronics)
* [Software](#software)
    * [Arduino](#arduino)
    * [Python](#python)
* [TODO](#todo)


# Materials
## Frame Construction
### Parts
* 12" x 12" 1/8" plywood (x3) for the face, back, and grid.
* 12" x 12" acrylic (need to figure out how opaque). Make sure you get acrylic and not the toxic stuff. These pieces will sit in the grid which 1) prevents light from leaking out and 2) diffuses the light across the entire letter.
* Get dimensions for walnut

The frame of the clock consists of the following parts:
* Laser cut face
* Laser cut grid which should be glued to the back of the face. You can edit the `face.svg` file and just remove all of the letters.
* Laser cut acylic pieces that fit into the grid. Should be glued carefully to the back of the letters
* Laser cut back
* Walnut sides

### Laser Cutter
Files for the laser cut parts are in the `lasercut` folder. You'll probably need to convert the svgs to dxfs first. I'm familiar with Ikscape so I'll go through those steps:
- open an svg in Inkscape
- Select everything. There should be an outer box border
- Change the stroke color to blue and path to 0.01mm
- With everything selected, change the dimensions to 11"x11" for the face file. The grid should be 8.7"x8.7". You can double check these measurements by superimposing the grid over the face and make sure the grid cutouts align with the letters
- Save as `.dxf`. There's some option for 12/14. Use 14.

## Electronics
Parts list:
* LED strip, 60/m. Note: the arduino code assumes that an APA102 strip is being used. That can easily be changed. The python code has a display class for the APA102 as well. Instructions for how to use the python code will be in the python directory.
* Arduino UNO or Raspberry Pi Zero W
* 9-12V, 1.5A power supply (see notes below)
* Push buttons
* Buck converter
* RTC module

If you use a Raspberry Pi you will need the following:
* Logic level converter

# Software
## Arduino
The first version of this was built using an Arduino Uno and 3 push buttons-- one to change animations/colors/brightness, and one each for increasing/decreasing time. Arduino code and a bit more information can be found [here](./code/arduino/).

## Python
The new and (hopefully) improved version will use python. You can choose to run this on whatever you would like, however, only the raspberry pi (any model will work) has been tested.

Why the change?

Running on the raspberry pi allows users to remotely update the code when new animations are available, update birthdays etc. You also don't need an RTC module and in general it's just easier to deal with the time with a wifi connection.

Python code and additional instructions can be found [here](./code/python/).

# TODO
* power consumption notes
* Systemd unit to check if wifi connected/listen for wps. See [this gist](https://gist.github.com/stickperson/354e79bf5e2af848f8ae7f6a88e5080f) for inspiration
* software + wiring notes
* links to products
