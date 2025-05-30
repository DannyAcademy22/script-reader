import sys
import os
import csv

# Commands
args = sys.argv
if len(args) < 4:
    print("Usage: python reader.py <src> <dst> <change1> <change2> ...")
    sys.exit(1)

src = args[1]
dst = args[2]
changes = args[3:]

if not os.path.isfile(src):
    print(f"Error: The file '{src}' does not exist or is not a valid file.")
    print("Files in this directory:")
    for f in os.listdir():
        print(f" - {f}")
    sys.exit(1)

with open(src) as f: #reading the file
    reader = csv.reader(f)
    data = list(reader)

for change in changes: #changes
    try:
        col, row, value = change.split(",")
        row = int(row)
        col = int(col)
        if row >= len(data) or col >= len(data[row]):
            print(f"Change out of range: {change}")
            continue
        data[row][col] = value
    except Exception:
        print(f"Invalid format or error in change: {change}")

print("\nUpdated content:") #updating info
for row in data:
    print(",".join(row))

# Save the updated CSV file
with open(dst, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

print(f"\nFile saved successfully as '{dst}'")
