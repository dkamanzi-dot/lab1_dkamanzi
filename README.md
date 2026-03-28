# Lab 1 - Grade Evaluator & Archiver

## What this project does
This project reads a student's grades from a CSV file,
calculates their GPA, and tells them if they passed or failed.
It also has a shell script that archives the grades file and
resets the workspace for the next batch.

## How to run the Python script
Make sure grades.csv is in the same folder, then run:

    python3 grade-evaluator.py

## How to run the shell script
Run this command:

    bash organizer.sh

This will:
- Move grades.csv to the archive folder with a timestamp
- Create a fresh empty grades.csv
- Log the action to organizer.log

## Files
- grade-evaluator.py — calculates grades and GPA
- organizer.sh — archives grades and resets workspace
- grades.csv — the student grade data
- organizer.log — log of every archive operation
