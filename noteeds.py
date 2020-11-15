#!/usr/bin/env python

from pathlib import Path
import sys

from noteeds.engine import Repository, Engine
from noteeds.util.timing import stopwatch

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} root text")
    exit(1)

root = Path(sys.argv[1])
text = sys.argv[2]

repository = Repository(root)
engine = Engine([repository])

with stopwatch("loading"):
    engine.load_all(None)

with stopwatch("searching"):
    result = engine.find(text, is_regex=False)

with stopwatch("dumping"):
    result.short_dump()
    # result.long_dump(text, is_regex=False)
