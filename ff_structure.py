import ctypes

#
# System-dependent timing definitions.  Linux version.
#  Copyright (C) 1996-2016 Free Software Foundation, Inc.
#  This file is part of the GNU C Library.
#
#  The GNU C Library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  The GNU C Library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with the GNU C Library; if not, see
#  <http://www.gnu.org/licenses/>.  */
#
# Ported from include/bits/time.h
#

class timeval(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_long),
        ("tv_usec", ctypes.c_long),
    ]

class input_event(ctypes.Structure):
    _fields_ = [
        ("time", timeval),
        ("type", ctypes.c_ushort),
        ("code", ctypes.c_ushort),
        ("value", ctypes.c_uint),
    ]

#
# Copyright (c) 1999-2002 Vojtech Pavlik
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# Ported from include/linux/input.h
#
class ff_replay(ctypes.Structure):
    _fields_ = [
        ('length', ctypes.c_ushort),
        ('delay',  ctypes.c_ushort),
    ]

class ff_trigger(ctypes.Structure):
    _fields_ = [
        ('button', ctypes.c_ushort),
        ('interval',  ctypes.c_ushort),
    ]

class ff_envelope(ctypes.Structure):
    _fields_ = [
        ('attack_length', ctypes.c_ushort),
        ('attack_level', ctypes.c_ushort),
        ('fade_length', ctypes.c_ushort),
        ('fade_level', ctypes.c_ushort),
    ]

class ff_constant_effect(ctypes.Structure):
    _fields_ = [
        ('level', ctypes.c_short),
        ('envelope', ff_envelope),
    ]

class ff_ramp_effect(ctypes.Structure):
    _fields_ = [
        ('start_level', ctypes.c_short),
        ('end_level', ctypes.c_short),
        ('envelope', ff_envelope),
    ]

class ff_condition_effect(ctypes.Structure):
    _fields_ = [
        ('right_saturation', ctypes.c_ushort),
        ('left_saturation', ctypes.c_ushort),
        ('right_coeff', ctypes.c_short),
        ('left_foeff', ctypes.c_short),
        ('deadband', ctypes.c_ushort),
        ('center', ctypes.c_short),
    ]

class ff_periodic_effect(ctypes.Structure):
    _fields_ = [
        ('waveform', ctypes.c_ushort),
        ('period', ctypes.c_ushort),
        ('magnitude', ctypes.c_short),
        ('offset', ctypes.c_short),
        ('phase', ctypes.c_ushort),
        ('envelope', ff_envelope),
        ('custom_len', ctypes.c_uint),
        ('custom_data', ctypes.POINTER(ctypes.c_short)),
    ]


class ff_rumble_effect(ctypes.Structure):
    _fields_ = [
        ('strong_magnitude', ctypes.c_ushort),
        ('weak_magnitude', ctypes.c_ushort),
    ]

class ff_effect_union(ctypes.Union):
    _fields_ = [
        ('constant', ff_constant_effect),
        ('ramp', ff_ramp_effect),
        ('periodic', ff_periodic_effect),
        ('condition', ff_condition_effect * 2),  # one for each axis
        ('rumble', ff_rumble_effect),
    ]

class ff_effect(ctypes.Structure):
    _fields_ = [
        ('type', ctypes.c_ushort),
        ('id', ctypes.c_short),
        ('direction', ctypes.c_ushort),
        ('trigger', ff_trigger),
        ('replay', ff_replay),
        ('u', ff_effect_union),
    ]

