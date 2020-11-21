#!/usr/bin/env python

from pathlib import Path
import sys
from noteeds.util.string import join_lines

from noteeds.engine import Repository, Engine, Query
from noteeds.util.timing import stopwatch
from noteeds.util.progress_monitor import TextProgressMonitor

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} root text")
    exit(1)

root = Path(sys.argv[1])
text = sys.argv[2]

repository = Repository(root)
engine = Engine([repository])
query = Query(text, False, None)

with stopwatch("loading"):
    # monitor = TextProgressMonitor(increment=200)
    monitor = TextProgressMonitor(dt = 1/25)
    engine.load_all(monitor)

with stopwatch("searching"):
    result = engine.find(query)

with stopwatch("dumping"):
    print(join_lines(result.short_dump(), width=120))
    # print(join_lines(result.long_dump(query), width=120))
