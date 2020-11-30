import shutil
from pathlib import Path


def main():
    source = Path("/") / "usr" / "share" / "games" / "fortunes"
    target = Path(__file__).parent / "fortunes"

    target.mkdir(parents=True, exist_ok=True)
    for source_file in source.glob("*"):
        if "." not in source_file.name:
            target_file = target / source_file.name
            print(target_file)
            shutil.copy(source_file, target_file)


if __name__ == "__main__":
    main()