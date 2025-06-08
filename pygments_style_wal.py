# -*- coding: utf-8 -*-
"""
    pygments_style_wal
    ~~~~~~~~~~~~~~~~~~~~~~~

    The Wal highlighting style.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from dataclasses import dataclass
from os import environ
from re import match
from warnings import warn
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace

"""
FG  BG   Name            VGA
30  40   Black           0,   0,   0
31  41   Red             170, 0,   0
32  42   Green           0,   170, 0
33  43   Yellow          170, 85,  0
34  44   Blue            0,   0,   170
35  45   Magenta         170, 0,   170
36  46   Cyan            0,   170, 170
37  47   White           170, 170, 170
90  100  Bright Black    85,  85,  85
91  101  Bright Red      255, 85,  85
92  102  Bright Green    85,  255, 85
93  103  Bright Yellow   255, 255, 85
94  104  Bright Blue     85,  85,  255
95  105  Bright Magenta  255, 85,  255
96  106  Bright Cyan     85,  255, 255
97  107  Bright White    255, 255, 255
"""

_VALUE_0_3 = 255 * 0 // 3
_VALUE_1_3 = 255 * 1 // 3
_VALUE_2_3 = 255 * 2 // 3
_VALUE_3_3 = 255 * 3 // 3

_SHORT_COLOR_HEX = r"^#[a-fA-F0-9]{3}$"
_LONG_COLOR_HEX = r"^#[a-fA-F0-9]{6}$"

@dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int

    @staticmethod
    def from_str(hex: str) -> "Color":
        if match(_SHORT_COLOR_HEX, hex):
            return Color(int(hex[1], 16), int(hex[2], 16), int(hex[3], 16))
        elif match(_LONG_COLOR_HEX, hex):
            return Color(int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:7], 16))
        else:
            raise ValueError('Unknown color format {hex!r}')

    def __str__(self) -> str:
        return f"#{self.red:02x}{self.green:02x}{self.blue:02x}"

@dataclass(frozen=True)
class ColorPalette16:
    black: Color = Color(_VALUE_0_3,  _VALUE_0_3,  _VALUE_0_3)
    red: Color = Color(_VALUE_2_3,_VALUE_0_3,  _VALUE_0_3)
    green: Color = Color(_VALUE_0_3,  _VALUE_2_3,_VALUE_0_3)
    yellow: Color = Color(_VALUE_2_3,_VALUE_1_3, _VALUE_0_3)
    blue: Color = Color(_VALUE_0_3,  _VALUE_0_3,  _VALUE_2_3)
    magenta: Color = Color(_VALUE_2_3,_VALUE_0_3,  _VALUE_2_3)
    cyan: Color = Color(_VALUE_0_3,  _VALUE_2_3,_VALUE_2_3)
    white: Color = Color(_VALUE_2_3,_VALUE_2_3,_VALUE_2_3)
    br_black: Color = Color(_VALUE_1_3, _VALUE_1_3, _VALUE_1_3)
    br_red: Color = Color(_VALUE_3_3,_VALUE_1_3, _VALUE_1_3)
    br_green: Color = Color(_VALUE_1_3, _VALUE_3_3,_VALUE_1_3)
    br_yellow: Color = Color(_VALUE_3_3,_VALUE_3_3,_VALUE_1_3)
    br_blue: Color = Color(_VALUE_1_3, _VALUE_1_3, _VALUE_3_3)
    br_magenta: Color = Color(_VALUE_3_3,_VALUE_1_3, _VALUE_3_3)
    br_cyan: Color = Color(_VALUE_1_3, _VALUE_3_3,_VALUE_3_3)
    br_white: Color = Color(_VALUE_3_3,_VALUE_3_3,_VALUE_3_3)

    @staticmethod
    def from_str(colors_: str) -> "ColorPalette16":
        colors = [Color.from_str(i) for i in colors_.splitlines()[0:16]]

        if len(colors) < 16:
            raise ValueError('There are less than 16 colors')

        return ColorPalette16(*colors)

try:
    XDG_CACHE_HOME = environ.get('XDG_CACHE_HOME', None)
    HOME = environ.get('HOME', None)

    if XDG_CACHE_HOME is None:
        if HOME is None:
            raise EnvironmentError('Neither XDG_CACHE_HOME nor HOME is defined')

        XDG_CACHE_HOME = HOME + '/.cache'

    WAL_CACHE_HOME = XDG_CACHE_HOME + '/wal'
    WAL_CACHE_COLORS = WAL_CACHE_HOME + '/colors'

    with open(WAL_CACHE_COLORS, 'r') as f:
        WAL = ColorPalette16.from_str(f.read())
except:
    warn('Could not fetch the color from pywal. Using the default VGA theme.', RuntimeWarning)
    WAL = ColorPalette16()

class WalStyle(Style):
    """
    The Wal highlighting style (ported from the default style).
    """

    background_color = f"{WAL.br_white}" # "#f8f8f8"
    default_style = ""

    styles = {
        Whitespace:                f"{WAL.br_black}", # "#bbbbbb",
        Comment:                   f"italic {WAL.cyan}", # "italic #408080",
        Comment.Preproc:           f"noitalic {WAL.yellow}", # "noitalic #BC7A00",

        Keyword:                   f"bold {WAL.green}", # "bold #008000",
        Keyword.Pseudo:            f"nobold", # "nobold",
        Keyword.Type:              f"nobold {WAL.red}", # "nobold #B00040",

        Operator:                  f"{WAL.br_black}", # "#666666",
        Operator.Word:             f"bold {WAL.br_magenta}", # "bold #AA22FF",

        Name.Builtin:              f"{WAL.green}", # "#008000",
        Name.Function:             f"{WAL.blue}", # "#0000FF",
        Name.Class:                f"bold {WAL.blue}", # "bold #0000FF",
        Name.Namespace:            f"bold {WAL.blue}", # "bold #0000FF",
        Name.Exception:            f"bold {WAL.br_red}", # "bold #D2413A",
        Name.Variable:             f"{WAL.blue}", # "#19177C",
        Name.Constant:             f"{WAL.red}", # "#880000",
        Name.Label:                f"{WAL.br_yellow}", # "#A0A000",
        Name.Entity:               f"bold {WAL.br_black}", # "bold #999999",
        Name.Attribute:            f"{WAL.br_yellow}", # "#7D9029",
        Name.Tag:                  f"bold {WAL.green}", # "bold #008000",
        Name.Decorator:            f"{WAL.br_magenta}", # "#AA22FF",

        String:                    f"{WAL.red}", # "#BA2121",
        String.Doc:                f"italic", # "italic",
        String.Interpol:           f"bold {WAL.br_red}", # "bold #BB6688",
        String.Escape:             f"bold {WAL.yellow}", # "bold #BB6622",
        String.Regex:              f"{WAL.br_red}", # "#BB6688",
        String.Symbol:             f"{WAL.blue}", # "#19177C",
        String.Other:              f"{WAL.green}", # "#008000",
        Number:                    f"{WAL.br_black}", # "#666666",

        Generic.Heading:           f"bold {WAL.blue}", # "bold #000080",
        Generic.Subheading:        f"bold {WAL.magenta}", # "bold #800080",
        Generic.Deleted:           f"{WAL.red}", # "#A00000",
        Generic.Inserted:          f"{WAL.green}", # "#00A000",
        Generic.Error:             f"{WAL.br_red}", # "#FF0000",
        Generic.Emph:              f"italic", # "italic",
        Generic.Strong:            f"bold", # "bold",
        Generic.Prompt:            f"bold {WAL.blue}", # "bold #000080",
        Generic.Output:            f"{WAL.br_black}", # "#888",
        Generic.Traceback:         f"{WAL.br_blue}", # "#04D",

        Error:                     f"border:{WAL.br_red}" # "border:#FF0000"
    }
