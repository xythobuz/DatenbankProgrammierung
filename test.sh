#!/usr/bin/env bash

./main.py quiet initialize

rm -rf test1_stdout.txt test1_stderr.txt
./main.py quiet test > test1_stdout.txt 2> test1_stderr.txt &

rm -rf test2_stdout.txt test2_stderr.txt
./main.py quiet test > test2_stdout.txt 2> test2_stderr.txt

