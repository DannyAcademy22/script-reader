import sys
import os
import csv
import json
import pickle

# Base class
class FileHandler:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.data = []

    def read(self):
        pass

    def apply_changes(self, changes):
        for change in changes:
            try:
                col, row, value = change.split(",")
                row = int(row)
                col = int(col)
                if row >= len(self.data) or col >= len(self.data[row]):
                    print(f"Change out of range: {change}")
                    continue
                self.data[row][col] = value
            except Exception:
                print(f"Invalid format or error in change: {change}")

    def display(self):
        print("\nUpdated content:")
        for row in self.data:
            print(",".join(row))

    def save(self):
        pass

# CSV handler
class CSVHandler(FileHandler):
    def read(self):
        with open(self.src, newline="") as f:
            reader = csv.reader(f)
            self.data = list(reader)

    def save(self):
        with open(self.dst, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

# JSON handler
class JSONHandler(FileHandler):
    def read(self):
        with open(self.src) as f:
            self.data = json.load(f)

    def save(self):
        with open(self.dst, "w") as f:
            json.dump(self.data, f)

# Pickle handler
class PickleHandler(FileHandler):
    def read(self):
        with open(self.src, "rb") as f:
            self.data = pickle.load(f)

    def save(self):
        with open(self.dst, "wb") as f:
            pickle.dump(self.data, f)

# Detect file type based on extension
def get_handler(src, dst):
    if src.endswith(".csv") and dst.endswith(".csv"):
        return CSVHandler(src, dst)
    elif src.endswith(".json") and dst.endswith(".json"):
        return JSONHandler(src, dst)
    elif src.endswith(".pickle") and dst.endswith(".pickle"):
        return PickleHandler(src, dst)
    else:
        print("Unsupported file format or mismatched extensions.")
        sys.exit(1)

# Read command-line arguments
args = sys.argv
if len(args) < 4:
    print("Usage: python reader.py <src> <dst> <change1> <change2> ...")
    sys.exit(1)

src = args[1]
dst = args[2]
changes = args[3:]

# Check if source file exists
if not os.path.isfile(src):
    print(f"Error: The file '{src}' does not exist or is not a valid file.")
    print("Files in this directory:")
    for f in os.listdir():
        print(f" - {f}")
    sys.exit(1)

# Get appropriate file handler
handler = get_handler(src, dst)

# Process file
handler.read()
handler.apply_changes(changes)
handler.display()
handler.save()

print(f"\nFile saved successfully as '{dst}'")
