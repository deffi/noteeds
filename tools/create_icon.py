#!/usr/bin/env python3

from pathlib import Path
import subprocess
import shutil


def svg2ico(svg_path: Path, ico_path: Path, verbose: bool):
    print(f"Convert {svg_path} to {ico_path}")
    subprocess.run(["convert", "-background", "transparent", svg_path, "-define",
                    "icon:auto-resize=256,48,32,16", ico_path])


if __name__ == "__main__":
    if shutil.which("inkscape"):
        svg_paths = (Path(__file__).resolve().parent.parent / "images").glob("*.svg")
        print(Path(__file__))
        for svg in svg_paths:
            svg2ico(Path(svg), Path(svg).with_suffix(".ico"), verbose=False)
    else:
        print("You need inkscape or the quality will be low")
