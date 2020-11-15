from os import PathLike


def read_file(path: PathLike):
    """Reads the specified file, automatically detecting the encoding.

     Currently, it tries UTF-8 and falls back on latin1 if that fails.

     Returns a tuple consisting of:
       * The entire file contents as a string
       * The encoding that was used
    """
    # TODO use chardet to determine the encoding
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read(), "utf-8"
    except UnicodeDecodeError:
        with open(path, 'r', encoding='latin1') as file:
            return file.read(), "latin1"
