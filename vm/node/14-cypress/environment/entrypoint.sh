#!/bin/bash

# Copy all codes and overrides
mkdir -p /judge/
cp -r /code/* /judge/
cp -r /environment/* /judge/
cp -r /overrides/* /judge/
cd /judge

test_cmd=$(cat package.json | jq -r .scripts.test)

if [ "$test_cmd" == "null" ]; then
    echo "No test command defined!"
    exit 1
fi

npx $test_cmd --reporter junit --reporter-options "mochaFile=report.xml" 1>&2
echo { \
    \"numTotalTests\": $(xmllint report.xml --xpath 'string(//testsuites/@tests)'), \
    \"numFailedTests\": $(xmllint report.xml --xpath 'string(//testsuites/@failures)') \
}
