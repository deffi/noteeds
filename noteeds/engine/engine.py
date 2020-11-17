from typing import Optional, Pattern


from noteeds.util import ProgressMonitor
from noteeds.engine import Repository, SearchResult, FileEntry, Query


class Engine:
    def __init__(self, repositories: list[Repository]):
        self._repositories = repositories
        self._entries: Optional[set[FileEntry]] = None

    def load_all(self, progress_monitor: Optional[ProgressMonitor]):
        if progress_monitor is None:
            progress_monitor = ProgressMonitor()

        self._entries = set.union(*(repo.entries() for repo in self._repositories))

        entry: FileEntry
        for entry in self._entries:
            entry.contents()

        #progress_monitor.range(0, len(self._entries))
        # for i, entry in enumerate(self._entries):
        #     progress_monitor.value(i)
        #     entry.
        #     self._files[file_path] = read_file(file_path)
        # progress_monitor.value(len(self._file_paths))

    def find(self, query: Query) -> SearchResult:
        """Finds all entries 
        Some of the result sets are, by their respective definitions, subsets of
        other result sets. For example, any file in the "file name begins with x"
        set is also (expected to be) in the "file name contains x" set.

        In such a case, there is no use in listing the file twice, and the the
        duplicate entries are not included in the less specific set (i. e., the
        superset).

        This does not, however, apply to a set that is not a superset of the
        other, such as "file name contains x" and "file content contains x".
        """

        def find_by_name(entries: set[FileEntry], pattern: Pattern):
            return set(e for e in entries if pattern.search(e.absolute_path.stem))

        def find_by_contents(entries: set[FileEntry], pattern: Pattern):
            return set(e for e in entries if pattern.search(e.contents()))

        name_anywhere = find_by_name(self._entries, query.anywhere_pattern)
        name_prefix   = find_by_name(name_anywhere, query.beginning_pattern)

        contents_anywhere    = find_by_contents(self._entries,        query.anywhere_pattern)
        contents_word_prefix = find_by_contents(contents_anywhere,    query.word_prefix_pattern)
        contents_word        = find_by_contents(contents_word_prefix, query.word_pattern)

        return SearchResult(
            name_prefix=name_prefix,
            name_anywhere=name_anywhere-name_prefix,
            contents_word=contents_word,
            contents_word_prefix=contents_word_prefix-contents_word,
            contents_anywhere=contents_anywhere-contents_word_prefix)
