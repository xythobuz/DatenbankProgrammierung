#!/usr/bin/env bash

rm -rf test1_stdout.txt test1_stderr.txt
./main.py quiet test initialize > test1_stdout.txt 2> test1_stderr.txt &

rm -rf test2_stdout.txt test2_stderr.txt
./main.py quiet test > test2_stdout.txt 2> test2_stderr.txt

