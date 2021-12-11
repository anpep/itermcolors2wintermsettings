#!/usr/bin/env python3
# coding: utf8

import sys
import math
import plistlib
import json

KEY_MAPPINGS = {
    "Ansi 0 Color": "black",
    "Ansi 1 Color": "red",
    "Ansi 2 Color": "green",
    "Ansi 3 Color": "yellow",
    "Ansi 4 Color": "blue",
    "Ansi 5 Color": "purple",
    "Ansi 6 Color": "cyan",
    "Ansi 7 Color": "white",
    "Ansi 8 Color": "brightBlack",
    "Ansi 9 Color": "brightRed",
    "Ansi 10 Color": "brightGreen",
    "Ansi 11 Color": "brightYellow",
    "Ansi 12 Color": "brightBlue",
    "Ansi 13 Color": "brightPurple",
    "Ansi 14 Color": "brightCyan",
    "Ansi 15 Color": "brightWhite",
    "Background Color": "background",
    "Cursor Color": "cursorColor",
    "Foreground Color": "foreground",
    "Selection Color": "selectionBackground",
}


def srgb_float_to_int(r: float, g: float, b: float) -> int:
    r = (int(math.ceil(r * 255.0)) & 0xFF) << 16
    g = (int(math.ceil(g * 255.0)) & 0xFF) << 8
    b = (int(math.ceil(b * 255.0)) & 0xFF) << 0
    return r | g | b


def main(args: list[str]) -> int:
    if len(args) != 2:
        print("usage: itermcolors2wintermsettings.py SCHEME_NAME ITERMCOLORS_FILE")
        return 1

    with open(args[1], "rb") as itermcolors:
        plist = plistlib.load(itermcolors, fmt=plistlib.FMT_XML)
        scheme = {"name": args[0]}

        for key, value in plist.items():
            if key not in KEY_MAPPINGS or "Color Space" not in value:
                continue
            rgb = srgb_float_to_int(
                value["Red Component"],
                value["Green Component"],
                value["Blue Component"],
            )
            scheme[KEY_MAPPINGS[key]] = f"#{rgb:06X}"

        print(json.dumps(scheme))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
