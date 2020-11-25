#!/usr/bin/env python3

import subprocess
import shutil

if __name__ == "__main__":
    if shutil.which("inkscape"):
        subprocess.run(["convert", "-verbose", "-background", "transparent", "icon.svg", "-define",
                        "icon:auto-resize=256,48,32,16", "icon.ico"])
    else:
        print("You need inkscape or the quality will be low")
