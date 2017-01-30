#!/bin/python3

#
# Based upon linuxconsole/utils/fftest.c
#
# Tests the force feedback driver
# Copyright 2001-2002 Johann Deneux <deneux@ifrance.com>
# Copyright 2017 ASL97 <asl97@openmailbox.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA.
#
# You can contact the author by email at this address:
# ASL97 <asl97@openmailbox.org>
#

import ctypes
import struct
import array
import fcntl
import sys
import os

from ff_structure import *
from bitmaskros import *
from input import *
from ioctl import *

relFeatures = array.array("B", [0] * (1 + REL_MAX//8//SOUC))
absFeatures = array.array("B", [0] * (1 + ABS_MAX//8//SOUC))
ffFeatures = array.array("B", [0] * (1 + FF_MAX//8//SOUC))
n_effects = array.array("B", [0])

ABS = [
    ("X", ABS_X),
    ("Y", ABS_Y),
    ("Z", ABS_Z),
    ("RX", ABS_RX),
    ("RY", ABS_RY),
    ("RZ", ABS_RZ),
    ("Throttle", ABS_THROTTLE),
    ("Rudder", ABS_RUDDER),
    ("Wheel", ABS_WHEEL),
    ("Gas", ABS_GAS),
    ("Brake", ABS_BRAKE),
    ("Hat 0 X", ABS_HAT0X),
    ("Hat 0 Y", ABS_HAT0Y),
    ("Hat 1 X", ABS_HAT1X),
    ("Hat 1 Y", ABS_HAT1Y),
    ("Hat 2 X", ABS_HAT2X),
    ("Hat 2 Y", ABS_HAT2Y),
    ("Hat 3 X", ABS_HAT3X),
    ("Hat 3 Y", ABS_HAT3Y),
    ("Pressure", ABS_PRESSURE),
    ("Distance", ABS_DISTANCE),
    ("Tilt X", ABS_TILT_X),
    ("Tilt Y", ABS_TILT_Y),
    ("Tool width", ABS_TOOL_WIDTH),
    ("Volume", ABS_VOLUME),
    ("Misc", ABS_MISC),
]

REL = [
    ("X", REL_X),
    ("Y", REL_Y),
    ("Z", REL_Z),
    ("RX", REL_RX),
    ("RY", REL_RY),
    ("RZ", REL_RZ),
    ("HWheel", REL_HWHEEL),
    ("Dial", REL_DIAL),
    ("Wheel", REL_WHEEL),
    ("Misc", REL_MISC),
]

FF = [
    ("Constant", FF_CONSTANT),
    ("Periodic", FF_PERIODIC),
    ("Ramp", FF_RAMP),
    ("Spring", FF_SPRING),
    ("Friction", FF_FRICTION),
    ("Damper", FF_DAMPER),
    ("Rumble", FF_RUMBLE),
    ("Inertia", FF_INERTIA),
    ("Gain", FF_GAIN),
    ("Autocenter", FF_AUTOCENTER),
]

effect_names = [
    "Sine vibration",
    "Constant Force",
    "Spring Condition",
    "Damping Condition",
    "Strong Rumble",
    "Weak Rumble",
]

EFFECT = [
    ("Square", FF_SQUARE),
    ("Triangle", FF_TRIANGLE),
    ("Sine", FF_SINE),
    ("Saw up", FF_SAW_UP),
    ("Saw down", FF_SAW_DOWN),
#    ("Custom", FF_CUSTOM), # no idea what to do with this
]

def perror(*args, **kwargs):
    # Piping to sys.stderr seem to mess up formatting
    print(*args, **kwargs) # file=sys.stderr,

def main():
    print("Force feedback test program.")
    print("HOLD FIRMLY YOUR WHEEL OR JOYSTICK TO PREVENT DAMAGES\n")

    device_file_name = None

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage: %s /dev/input/eventXX" % sys.argv[0])
            print("Tests the force feedback driver")
            return

        # Check if it's an device number
        if sys.argv[1].isdigit():
            device_file_name = "/dev/input/event"+sys.argv[1]
        # Assume device path is passed, path exists check below
        else:
            device_file_name =  sys.argv[1]

    if device_file_name is None:
        device_file_name = "/dev/input/event0"

    if not os.path.exists(device_file_name):
        perror("Open device file: No such file or directory")
        return

    try:
        fd = os.open(device_file_name, os.O_RDWR)
    except Exception as e:
        perror(e)
        return

    print("Device %s opened" % device_file_name);

    # Query device
    print("Features:")


    # Absolute axes
    try:
        fcntl.ioctl(fd, EVIOCGBIT(EV_ABS, len(absFeatures)*SOUC), absFeatures)
    except Exception as e:
        perror("Ioctl absolute axes features query", e)
        return

    print("  * Absolute axes: "+", ".join(name for name, i in ABS if testBit(i, absFeatures)))
    print("    [%s]" % " ".join("%02X" % feature for feature in absFeatures))


    # Relative axes
    try:
        fcntl.ioctl(fd, EVIOCGBIT(EV_REL, len(relFeatures)*SOUC), relFeatures)
    except Exception as e:
        perror("Ioctl relative axes features query", e)
        return

    print("  * Relative axes: "+", ".join(name for name, i in REL if testBit(i, relFeatures)))
    print("    [%s]" % " ".join("%02X" % feature for feature in relFeatures))


    # Force feedback effects
    try:
        fcntl.ioctl(fd, EVIOCGBIT(EV_FF, len(ffFeatures)*SOUC), ffFeatures)
    except Exception as e:
        perror("Ioctl force feedback features query", e)
        return

    print("  * Force feedback effects types: "+", ".join(name for name, i in FF if testBit(i, ffFeatures)))
    print("    Force feedback periodic effects: "+", ".join(name for name, i in EFFECT if testBit(i, ffFeatures)));
    print("    [%s]" % " ".join("%02X" % feature for feature in ffFeatures))

    try:
        fcntl.ioctl(fd, EVIOCGEFFECTS, n_effects)
    except Exception as e:
        perror("Ioctl number of effects", e)
        return

    print("  * Number of simultaneous effects: %d\n" % n_effects[0])


    # Set master gain to 75% if supported
    if testBit(FF_GAIN, ffFeatures):
        gain = input_event()

        gain.type = EV_FF
        gain.code = FF_GAIN
        gain.value = 0xC000 # [0, 0xFFFF])

        print("Setting master gain to %d%% ... " % (gain.value*100//0xFFFF), end="")
        if os.write(fd, gain) != ctypes.sizeof(gain):
          perror("Error:")
        else:
          print("OK")


    # Effect tracking functions
    effects = {}
    ids = {}
    i = 1

    def upload_effect(name, effect):
        nonlocal i
        print("Uploading effect #%d (%s) ... " % (i, name), end="")
        try:
            fcntl.ioctl(fd, EVIOCSFF, effect)
        except Exception as e:
            perror("Error:", e)
        else:
            print("OK (id %d)" % effect.id)
            effects[name] = effect
        ids[i] = name
        i+=1

    # input.py doesn't provide EVIOCSFF so we define our own.
    EVIOCSFF = IOC(IOC_WRITE, 'E', 0x80, ctypes.sizeof(ff_effect))

    # Upload a periodic sinusoidal effect
    for name, wave in EFFECT:
        effect = ff_effect()
        effect.type = FF_PERIODIC
        effect.id = -1
        effect.direction = 0x4000 # Along X axis
        effect.trigger.button = 0
        effect.trigger.interval = 0
        effect.replay.length = 20000 # 20 seconds
        effect.replay.delay = 1000
        effect.u.periodic.waveform = wave
        effect.u.periodic.period = 100 # 0.1 second
        effect.u.periodic.magnitude = 0x7fff # 0.5 * Maximum magnitude
        effect.u.periodic.offset = 0
        effect.u.periodic.phase = 0
        effect.u.periodic.envelope.attack_length = 1000
        effect.u.periodic.envelope.attack_level = 0x7fff
        effect.u.periodic.envelope.fade_length = 1000
        effect.u.periodic.envelope.fade_level = 0x7fff

        upload_effect("Periodic sinusoidal [%s]" %name, effect)


    # Upload a constant effect
    effect = ff_effect()
    effect.type = FF_CONSTANT
    effect.id = -1
    effect.direction = 0x6000 # 135 degrees
    effect.trigger.button = 0
    effect.trigger.interval = 0
    effect.replay.length = 20000 # 20 seconds
    effect.replay.delay = 0
    effect.u.constant.level = 0x2000 # Strength : 25 %
    effect.u.constant.envelope.attack_length = 1000
    effect.u.constant.envelope.attack_level = 0x1000
    effect.u.constant.envelope.fade_length = 1000
    effect.u.constant.envelope.fade_level = 0x1000

    upload_effect("Constant", effect)


    # Upload a condition spring effect
    effect = ff_effect()
    effect.type = FF_SPRING
    effect.id = -1
    effect.trigger.button = 0
    effect.trigger.interval = 0
    effect.replay.length = 20000 # 20 seconds
    effect.replay.delay = 0
    effect.u.condition[0].right_saturation = 0x7fff
    effect.u.condition[0].left_saturation = 0x7fff
    effect.u.condition[0].right_coeff = 0x2000
    effect.u.condition[0].left_coeff = 0x2000
    effect.u.condition[0].deadband = 0x0
    effect.u.condition[0].center = 0x0
    effect.u.condition[1] = effect.u.condition[0]

    upload_effect("Spring", effect)


    # Upload a condition damper effect
    effect = ff_effect()
    effect.type = FF_DAMPER
    effect.id = -1
    effect.trigger.button = 0
    effect.trigger.interval = 0
    effect.replay.length = 20000 # 20 seconds
    effect.replay.delay = 0
    effect.u.condition[0].right_saturation = 0x7fff
    effect.u.condition[0].left_saturation = 0x7fff
    effect.u.condition[0].right_coeff = 0x2000
    effect.u.condition[0].left_coeff = 0x2000
    effect.u.condition[0].deadband = 0x0
    effect.u.condition[0].center = 0x0
    effect.u.condition[1] = effect.u.condition[0]

    upload_effect("Damper", effect)


    # Upload a strong rumbling effect
    effect = ff_effect()
    effect.type = FF_RUMBLE
    effect.id = -1
    effect.replay.length = 5000
    effect.replay.delay = 1000
    effect.u.rumble.strong_magnitude = 0x8000
    effect.u.rumble.weak_magnitude = 0

    upload_effect("Strong rumble, with heavy motor", effect)


    # Upload a weak rumbling effect
    effect = ff_effect()
    effect.type = FF_RUMBLE
    effect.id = -1
    effect.u.rumble.strong_magnitude = 0
    effect.u.rumble.weak_magnitude = 0xc000
    effect.replay.length = 5000
    effect.replay.delay = 0

    upload_effect("Weak rumble, with light motor", effect)


    def stop():
        for name, effect in effects.items():
            stop = input_event()
            stop.type = EV_FF;
            stop.code =  effect.id;
            stop.value = 0;

            if os.write(fd, stop) != ctypes.sizeof(stop):
                perror("")
                return

    # Ask user what effects to play
    while True:
        num = input("Enter effect number, 0 to stop, -1 to exit\n")
        try:
            num = int(num)
        except:
            continue

        if num == 0:
            stop()
        elif i > num >= 1:
            if ids[num] in effects:
                play = input_event()
                play.type = EV_FF
                play.code = effects[ids[num]].id
                play.value = 1

                if os.write(fd, play) != ctypes.sizeof(play):
                    perror("Play effect")
                    return

                print("Now Playing: %s" % ids[num])
            else:
                print("Effect '%s' unavailable" % ids[num])
        elif num == -1:
            break
        else:
            print("No such effect")

    # Stop the effects
    print("Stopping effects")
    stop()

if __name__ == "__main__":
    main()
