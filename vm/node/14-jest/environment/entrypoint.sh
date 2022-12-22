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

npx $test_cmd --detectOpenHandles --json --outputFile report.json
echo { \
    \"success\": $(cat report.json | jq .success), \
    \"numTotalTests\": $(cat report.json | jq .numTotalTests), \
    \"numFailedTests\": $(cat report.json | jq .numFailedTests), \
    \"numPassedTests\": $(cat report.json | jq .numPassedTests) \
}
