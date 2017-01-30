"""
 * bitmaskros.py, ported from https://github.com/flosse/linuxconsole/blob/master/utils/bitmaskros.h
 *
 * Helper macros for large bit masks management
 *
 * Copyright (C) 2008 Jean-Philippe Meuret
 * Copyright (c) 2017 ASL97 <asl97@openmailbox.org>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import ctypes

SOUC = ctypes.sizeof(ctypes.c_ubyte)

#Number of bits for 1 unsigned char
nBitsPerUchar = SOUC * 8

# Number of unsigned chars to contain a given number of bits
def nUcharsForNBits(nBits):
    return ((((nBits)-1)//nBitsPerUchar)+1)

# Index=Offset of given bit in 1 unsigned char
def bitOffsetInUchar(bit):
    return ((bit)%nBitsPerUchar)

# Index=Offset of the unsigned char associated to the bit
# at the given index=offset
def ucharIndexForBit(bit):
    return ((bit)//nBitsPerUchar)

# Value of an unsigned char with bit set at given index=offset
def ucharValueForBit(bit):
    return (ctypes.c_ubyte(1)<<bitOffsetInUchar(bit))

# Test the bit with given index=offset in an unsigned char array
def testBit(bit, array):
    return ((array[ucharIndexForBit(bit)] >> bitOffsetInUchar(bit)) & 1)
