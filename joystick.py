# TEST
import inputs
import time
import numpy as np


class Joystick:
    def __init__(self, __event__, init=True):
        global op_durations
        self.valid = False
        self.buttons = [{'BTN_TRIGGER': 'A'}, {'BTN_THUMB': 'B'}, {'BTN_THUMB2': 'C'}, {'BTN_TOP': 'X'},
                        {'BTN_TOP2': 'Y'}, {'BTN_PINKIE': 'Z'}, {'BTN_BASE': 'Left Trigger'},
                        {'BTN_BASE2': 'Right Trigger'}, {'BTN_BASE3': 'Select'}]
        self.axes = [{'ABS_X': 'Left x-axe'}, {'ABS_Y': 'Left y-axe'},
                     {'ABS_RZ': 'Right x-axe'}, {'ABS_THROTTLE': 'Right y-axe'}]
        self.hats = [{'ABS_HAT0X': 'Hat x-axe'}, {'ABS_HAT0Y': 'Hat y-axe'}]
        self.codes = ['Misc', 'Sync', 'SYN_REPORT']
        self.__event__ = __event__
        if Joystick.check_valid(self) and init:
            self.start = float(time.time())
            Joystick.check_action(self)

    def __del__(self):
        if self.valid:
            op_durations.append((time.time() - self.start) * 1000)  # in ms

    def check_valid(self):
        if self.__event__.code not in self.codes and \
                (not 125 <= self.__event__.state <= 135 or self.__event__.state in [-1, 1])\
                and not self.__event__.state == 0:
            self.valid = True
            return True

    def check_action(self):
        if any(self.__event__.code in e for e in self.buttons):
            Joystick.btn_trigger(self)

        elif any(self.__event__.code in e for e in self.hats):
            Joystick.hat_trigger(self)

        elif any(self.__event__.code in e for e in self.axes):
            Joystick.joy_trigger(self)

    def btn_trigger(self):
        index, _dict_ = next((place, dict_) for place, dict_ in enumerate(self.buttons) if self.__event__.code in dict_)
        print('{} pressed'.format(self.buttons[index][self.__event__.code]))

    def hat_trigger(self):
        index, _dict_ = next((place, dict_) for place, dict_ in enumerate(self.hats) if self.__event__.code in dict_)
        # Invert Y axe from hat
        if self.__event__.code == list(self.hats[1].keys())[0]:
            self.__event__.state *= -1
        print('{} value: {}'.format(self.hats[index][self.__event__.code], self.__event__.state))

    def joy_trigger(self):
        index, _dict_ = next((place, dict_) for place, dict_ in enumerate(self.axes) if self.__event__.code in dict_)
        self.__event__.state = (self.__event__.state - 127.5) / 127.5
        # Invert Y axe from joys
        if self.__event__.code in [list(self.axes[1].keys())[0], list(self.axes[3].keys())[0]]:
            self.__event__.state *= -1
        print('{} value: {}'.format(self.axes[index][self.__event__.code], self.__event__.state))


print('Controller used: {}'.format(inputs.devices.gamepads[0]))
op_durations = []
while True:
    try:
        events_ = inputs.get_gamepad()
        for event_ in events_:
            Joystick(event_)
    except KeyboardInterrupt:
        print('\nAverage op duration: {} ms'.format(round(np.sum(np.array(op_durations)) / len(op_durations), 4)))
        break
