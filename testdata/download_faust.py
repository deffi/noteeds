from dataclasses import dataclass
from urllib.parse import urljoin
from pathlib import Path
import re

from bs4 import BeautifulSoup
import requests
import requests_cache


requests_cache.install_cache('cache')

index_url = "https://www.projekt-gutenberg.org/goethe/faust1/index.html"


@dataclass()
class Chapter:
    number: int
    title: str
    url: str

    def get_text(self, session: requests.Session):
        result = []

        print(f"Fetching {self.url}")
        response = session.get(self.url)
        assert response.status_code == 200
        chapter = BeautifulSoup(response.content, features="html.parser")

        paragraphs = [p for p in chapter.select("body p h3, body p p")]

        for p in paragraphs:
            result.append(p.text)

        return "\n\n".join(result)

    def file_name(self):
        title = re.sub(r'[^\w()., ]', '', self.title)
        return f"{self.number:02d} - {title}.txt"


def main():
    with requests.Session() as session:
        index_response = session.get(index_url)
        assert index_response.status_code == 200

        index = BeautifulSoup(index_response.content, features="html.parser")

        links = index.select("body li a")
        chapters = [Chapter(index + 1, link.text, urljoin(index_response.url, link["href"]))
                    for index, link in enumerate(links)]

        path = Path(__file__).parent / "faust"
        path.mkdir(parents=True, exist_ok=True)
        for chapter in chapters:
            chapter_path = path / chapter.file_name()
            chapter_text = chapter.get_text(session)
            print(f"Writing {chapter_path}")
            chapter_path.write_text(chapter_text)


if __name__ == "__main__":
    main()
