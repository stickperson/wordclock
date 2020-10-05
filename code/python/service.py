import signal
import sys

from animations import ColorCycle, Pulse, Rainbow
from models import Clock, Timer
from settings import birthdays, display_cls, words
from buttons import ButtonStateManager, MockButton


class WordClock:
    def __init__(self):
        self.displayer = display_cls(rows=10, columns=13, max_brightness=25)
        self.clock = Clock(displayer=self.displayer, words=words, birthdays=birthdays)
        self.birthday_animation = Rainbow(
            self.displayer, self.displayer.pixels, speed=.1, words=[words['HAPPY'], words['BIRTHDAY']]
        )

        self.button_animations = []
        self.button = None
        self.timers = []

        self._startup()

    def cleanup(self, *args, exit=True, **kwargs):
        """
        Cleanup the display (turns off LEDs etc) and exits the program by default
        """
        self.displayer.cleanup()
        if exit:
            sys.exit(0)

    def _startup(self):
        """
        Immediately fetch the time and setup button/timers
        """
        self.clock.update()
        self._setup_button_handlers()
        self._setup_timers()

    def reset_display_and_clock(self):
        """
        Resets the display to default values and updates the clock. If showing the time is moved to a "animation"
        or "plugin" then self.clock.update could be removed.
        """
        self.displayer.reset()
        self.clock.update()

    # TODO. Stop hardcoding this. Possible put it into some sort of configuration file.
    def _setup_button_handlers(self):
        pulse = Pulse(self.clock, self.displayer, self.displayer.pixels, speed=0.05, period=3)
        pulse.run_alone = False
        color_cycle = ColorCycle(self.clock, self.displayer, self.displayer.pixels, speed=0.05)
        rainbow = Rainbow(
            self.displayer, self.displayer.pixels, speed=0.1, words=[words['ALL']])

        self.button_animations = [pulse, color_cycle, rainbow]
        button_manager = ButtonStateManager(
            len(self.button_animations), on_reset=self.reset_display_and_clock
        )
        self.button = MockButton(4, button_manager, hold_time=0.5)

    def _setup_timers(self):
        check_birthday_timer = Timer(60000, self.clock.check_birthday)  # update every minute
        update_clock_timer = Timer(60000, self.clock.update)  # update every minute

        self.timers = [check_birthday_timer, update_clock_timer]

    # TODO. Figure out how to turn off displaying the birthday animation if another animation should overwrite it.
    def tick(self):
        """
        Runs timers, checks if the birthday message should be displayed, and runs any animations
        """
        for timer in self.timers:
            timer.tick()

        if self.clock.is_birthday and self.birthday_animation:
            self.birthday_animation.animate()

        # Check the state of the button
        current_state = self.button.current_state
        if current_state:
            button_animation = self.button_animations[current_state - 1]
            # Some animations will only be run if the button is currently pressed down. If it should be run after
            # release until the button is pressed, add `continue_after_button_pressed = True` to the animation
            # instance
            if self.button.is_held or getattr(button_animation, 'continue_after_button_pressed', False):
                button_animation.animate()

        # And refresh the display
        self.displayer.display()


if __name__ == '__main__':
    # Setup clock and display
    wordclock = WordClock()
    signal.signal(signal.SIGTERM, wordclock.cleanup)

    while True:
        cleanup = False
        exception = None
        try:
            wordclock.tick()
        except Exception:
            wordclock.cleanup(exit=False)
            raise
