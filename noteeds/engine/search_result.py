from dataclasses import dataclass

from noteeds.util.string import box, grep, prefix_lines
from noteeds.util.iterable import sequence_join
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
            return [f"==== {caption} ====",
                    ", ".join(sorted(entry.absolute_path.stem for entry in result_set))]

        return sequence_join([""], [dump_set("File name - prefix"    , self.name_prefix),
                                    dump_set("File name - anywhere"  , self.name_anywhere),
                                    dump_set("Contents - word"       , self.contents_word),
                                    dump_set("Contents - word prefix", self.contents_word_prefix),
                                    dump_set("Contents - anywhere"   , self.contents_anywhere)])

    def long_dump(self, query: Query):
        def dump_set(caption, result_set):
            return [*box(caption, "*"),
                    "",
                    *(entry.absolute_path.stem for entry in result_set)]

        def grep_entry(entry: FileEntry):
            return [f"{entry.absolute_path.stem}:",
                    *prefix_lines(grep(query.anywhere_pattern, entry.contents().splitlines()), "    "), ""]

        def dump_set_and_grep(caption, result_set):
            return [*box(caption, "*"),
                    "",
                    # *sequence_join([""], [grep_entry(entry) for entry in sorted(result_set)])]
                    *sum((grep_entry(entry) for entry in sorted(result_set)), [])]

        return sequence_join([""], [
            dump_set         ("File name - prefix"    , self.name_prefix),
            dump_set         ("File name - anywhere"  , self.name_anywhere),
            dump_set_and_grep("Contents - word"       , self.contents_word),
            dump_set_and_grep("Contents - word prefix", self.contents_word_prefix),
            dump_set_and_grep("Contents - anywhere"   , self.contents_anywhere),
        ])
