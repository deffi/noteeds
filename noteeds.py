#!/usr/bin/env python

from pathlib import Path
import sys

from noteeds.engine import Repository, Engine, Query
from noteeds.util.timing import stopwatch

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} root text")
    exit(1)

root = Path(sys.argv[1])
text = sys.argv[2]

repository = Repository(root)
engine = Engine([repository])
query = Query(text, False, None)

with stopwatch("loading"):
    engine.load_all(None)

with stopwatch("searching"):
    result = engine.find(query)

with stopwatch("dumping"):
    result.short_dump()
    # result.long_dump(query)
