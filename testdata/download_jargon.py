from dataclasses import dataclass
from pathlib import Path
import re
import io
import textwrap as wrap

from bs4 import BeautifulSoup
import requests
import requests_cache
import tarfile

version = "4.4.7"


@dataclass()
class TarFile:
    content: bytes

    def entries(self):
        tar_io = io.BytesIO(self.content)
        tar = tarfile.open(fileobj=tar_io)
        for member in tar.getmembers():
            if match := re.fullmatch(f"jargon-{re.escape(version)}/html/./(.*).html", member.name):
                name = match.group(1)
                yield Entry(name, tar.extractfile(member).read())


def simplify_whitespace(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()


@dataclass()
class Entry:
    name: str
    content: bytes

    def to_text(self):
        # Fails for tables etc.
        soup = BeautifulSoup(self.content, features="html.parser")

        term = simplify_whitespace(soup.find("dt").text)
        definitions = [simplify_whitespace(tag.text) for tag in soup.findAll("dd")]
        definitions = [wrap.fill(d, width=80, initial_indent="    ", subsequent_indent="    ") for d in definitions]

        return "\n\n".join([term, *definitions])


def main():
    requests_cache.install_cache('cache')
    url = f"http://www.catb.org/jargon/jargon-{version}.tar.gz"
    print(f"Fetching {url}")
    r = requests.get(url)
    assert r.status_code == 200

    tar_file = TarFile(r.content)
    entries = list(tar_file.entries())

    output_path = Path(__file__).parent / "jargon"
    output_path.mkdir(parents=True, exist_ok=True)

    for entry in entries:
        file_path = (output_path / entry.name)
        print(file_path)
        text = entry.to_text()
        file_path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
