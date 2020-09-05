## Introduction
This code is broken up into several components in order to keep things modular (composition over inheritance).

The `displays` directory contains files for displaying the state of the clock. Currently, there is support for the APA102 led strip and displaying to the console. The `ConsoleDisplay` is helpful for development. If you would like to use another chipset, you can implement your own display class.

The `models.py` file contains all the knowledge about how to update the clock. The `service.py` file contains the logic for how to use the models.

## Setup
Configuration should go in the `settings.py` file. The following must be defined:

* `display_cls` determines which sort of display to use. There is currently support for the `APA102` strip as well and `ConsoleDisplay` for development purposes. If you wish to use a different chipset, you can implement your own display class and import it.
* `words`. A mapping between words on the clock, start/stop indices, and optionally display values for non-led displays. The default values are setup to work with the supplied designs.
* `birthdays`. An array of `Birthday` instances.

Once this is setup, you can run `python service.py`


## TODO
* ABC for displays
* Think about where the birthday logic should live
* Button handlers