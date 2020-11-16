import re
from dataclasses import dataclass
from textwrap import fill

from noteeds.util.string import box
from noteeds.engine import FileEntry, Query


@dataclass(frozen=True)
class SearchResult:
    name_prefix: set[FileEntry]
    name_anywhere: set[FileEntry]

    contents_word: set[FileEntry]
    contents_word_prefix: set[FileEntry]
    contents_anywhere: set[FileEntry]

    def short_dump(self):
        def dump_set(caption, result_set):
            print()
            print("==== %s ====" % caption)
            names = (entry.absolute_path.stem for entry in result_set)
            text = ", ".join(sorted(names))
            print(fill(text, width = 120))

        dump_set("File name - prefix"    , self.name_prefix)
        dump_set("File name - anywhere"  , self.name_anywhere)
        dump_set("Contents - word"       , self.contents_word)
        dump_set("Contents - word prefix", self.contents_word_prefix)
        dump_set("Contents - anywhere"   , self.contents_anywhere)

    def long_dump(self, query: Query):
        def dump_set(caption, result_set):
            print()
            print(box(caption, "*"))
            print()

            for entry in sorted(result_set):
                print(entry.absolute_path.stem)

        def dump_set_and_grep(caption, result_set):
            print(box(caption, "*"))

            for entry in sorted(result_set):
                print()
                print(f"{entry.absolute_path.stem}:")
                for line in entry.contents().splitlines():
                    if query.anywhere_pattern.search(line):
                        print(f"    {line}")
            print()

        dump_set("File name - prefix"    , self.name_prefix)
        dump_set("File name - anywhere"  , self.name_anywhere)
        dump_set_and_grep("Contents - word"       , self.contents_word)
        dump_set_and_grep("Contents - word prefix", self.contents_word_prefix)
        dump_set_and_grep("Contents - anywhere"   , self.contents_anywhere)
