#!/usr/bin/env python3

import sys
from components.data_processing import processCSV

input = sys.argv[1]
output = sys.argv[2]

print("Starting data cleaning...")
processCSV(input, output)
print("Completed data cleaning!")