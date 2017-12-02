#!/usr/bin/env bash

year=$1
day=$2

if [ ! -d $year ]; then
    mkdir $year
fi
cd $year

if [ ! -d $day ]; then
    mkdir $day
fi
cd $day

touch input
touch main.py

