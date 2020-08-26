#!/bin/bash

# run pylint
find . -name "*.py" -and -not -name "0*.py" | xargs pylint

# run flake8
flake8 .
