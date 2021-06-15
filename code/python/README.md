# :construction: Under Construction :construction:

## Introduction
This code is broken up into several components in order to keep things modular.

### Displays
Chipsets etc. Currently, there is support for the APA102 led strip and displaying to the console. The `ConsoleDisplay` is helpful for development. If you would like to use another chipset, you can implement your own display class.

### Layouts
Represents the physical layout of words on the clock in terms of what positions words are at and what words to return for birthdays and the time of day. New languages can be supported by implementing new layouts.

### Models
The `models.py` file contains all the knowledge about how to update the clock. The `main.py` file contains the logic for how to use the models. These files should probably be split out. I need to think of a better home.

### Animations
Custom animations.

## Setup
Configuration can go into a settings file. Here, `example_local_config.py` is provided for testing purposes. The layout, display, and birthdays should be setup here. After defining these, you can import them in `main.py` and run the script.

This `main.py` file is a proof of concept.

## TODO
* Graceful shutdown
* Show images (https://github.com/bk1285/rpi_wordclock/blob/master/wordclock_tools/wordclock_display.py#L196)
* Tests
* Fix indices for words (make them half open instead of closed)
