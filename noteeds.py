#!/usr/bin/env python3

from pathlib import Path
import sys
from noteeds.util.string import join_lines

from noteeds.engine import Repository, Engine, Query
from noteeds.util.timing import stopwatch
from noteeds.util.progress import Tracker, BarMonitor

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} root text")
    exit(1)

root = Path(sys.argv[1])
text = sys.argv[2]

repository = Repository(root)
engine = Engine([repository])
query = Query(text, False, None)

with stopwatch("loading"):
    # tracker = Tracker(TextMonitor(" ", "\n"), steps=10)
    tracker = Tracker(BarMonitor(50), steps=50)
    engine.load_all(tracker)

with stopwatch("searching"):
    result = engine.find(query)

with stopwatch("dumping"):
    print(join_lines(result.short_dump(), width=120))
    # print(join_lines(result.long_dump(query), width=120))
