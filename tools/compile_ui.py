from pathlib import Path
from subprocess import run

import PySide2

uic = Path(PySide2.__file__).parent / "uic"


def auto_compile(base_path: Path = Path.cwd()):
    for ui_file in base_path.rglob("*.ui"):
        py_file = ui_file.with_name(f"ui_{ui_file.stem}.py")
        print(f"Compile {ui_file} to {py_file}")
        run([uic, "-g", "python", "-o", py_file, ui_file])


if __name__ == "__main__":
    auto_compile(Path(__file__).parent.parent / "noteeds" / "gui")
