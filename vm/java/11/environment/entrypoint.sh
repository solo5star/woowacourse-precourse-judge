#!/bin/bash

# Copy all codes and overrides
mkdir -p /judge/
cp -r /code/* /judge/
cp -r /environment/* /judge/
cp -r /overrides/* /judge/
cd /judge

gradle test --rerun-tasks \
            --info \
            --offline \
            --no-daemon \
            1>&2

report_file="build/reports/tests/test/index.html"
echo { \
    \"numTotalTests\": $(xmllint $report_file --xpath 'string(//*[@id="tests"]/div)'), \
    \"numFailedTests\": $(xmllint $report_file --xpath 'string(//*[@id="failures"]/div)'), \
    \"numIgnoredTests\": $(xmllint $report_file --xpath 'string(//*[@id="ignored"]/div)') \
}
