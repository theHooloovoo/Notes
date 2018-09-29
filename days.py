#!/usr/bin/env python3
import datetime
import re
import sys

today = datetime.datetime.today()

# Matches YYYY-MM-DD as whole string
re_date = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Matches HH:MM[am|pm] as whole string
re_time = re.compile(r"^\d{1,2}:\d{1,2}(?:am|pm)$")

# Open file, and load it, line-by-line into the list 'lines'
file_name = "resources/records"
if len(sys.argv) >= 2:
    file_name = sys.argv[1]
f_in = open(file_name)

lines = []
n = 0   # Original line number from file
for line in f_in.readlines():
    n = n + 1
    # Ignore comments (denoted by '#')
    # Ignore Emtpy lines
    if len(line) == 0:
        continue
    else:
        words = line.split()
        z = []
        # We know that lines with less than 3 words are of bad form
        if len(words) >= 2:
            if re_date.match(words[0]):
                z.append(words[0])
            else:
                continue
            # join all but the first two elements of words to z
            z.append(' '.join(words[-(len(words)-1):]))
        if len(z) == 2:
            z.append(n)
            lines.append(z)

# Now that we have a list of data to work with, let's
# process it into datetime objects!
data = []
for n in lines:
    z = []
    # Add the date
    event = datetime.datetime.strptime(n[0], "%Y-%m-%d").date() 
    z.append(event)
    # Add the days until the event
    delta = event - today.date()
    z.append(delta.days)
    # Add the event description
    z.append(n[1])
    # Add the line number
    z.append(n[2])
    data.append(z)

# Sort the list before I convert it into
# strings, because fuck fidling with that
data.sort(key=lambda x: x[0])

# print( "Today is:", today.date() )

# Construct list of strings to be padded
print_list = []
for n in data:
    s1 = ""
    if n[1] == 1:
        s1 = str(n[1]) + " Day until:"  # Let's be proper about this!
    else:
        s1 = str(n[1]) + " Days until:"
    # Only append if event hasn't yet passed
    if n[1] > 0:
        print_list.append([s1, n[1], n[2], n[3]])

# Pad each string to the same length, and print
max_length = 0
for n in print_list:
    max_length = max(map(lambda x: len(x[0]), print_list))

for n in print_list:
    n[0] = n[0].rjust(max_length + 1)
    print(n[0], n[2])

