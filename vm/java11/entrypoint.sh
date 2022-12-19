#!/bin/bash

# Copy all codes to mirror directory
cp -r /code /code-mirror

gradle test --rerun-tasks --info --offline --no-daemon --project-dir /code-mirror 1>&2

cat /code-mirror/build/reports/tests/test/index.html \
    | pup '.summaryGroup tr td .counter text{}' \
    | head -3 \
    | xargs printf '{"numTotalTests":%d,"numFailedTests":%d,"numIgnoredTests":%d}'
