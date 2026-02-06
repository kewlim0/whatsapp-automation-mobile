#!/usr/bin/env python3
# Script to remove duplicate names from chat_name.txt

input_file = r"C:\Users\BDC Computer ll\Documents\Appium-test\txt\chat_name.txt"
output_file = r"C:\Users\BDC Computer ll\Documents\Appium-test\txt\chat_name_no_duplicates.txt"

# Read all lines from the input file
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Track seen names and keep order
seen = set()
unique_lines = []
duplicates_removed = 0

for line in lines:
    name = line.strip()
    if name and name not in seen:
        seen.add(name)
        unique_lines.append(line)
    elif name in seen:
        duplicates_removed += 1

# Write unique lines to output file
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(unique_lines)

print(f"Original lines: {len(lines)}")
print(f"Unique lines: {len(unique_lines)}")
print(f"Duplicates removed: {duplicates_removed}")
print(f"\nOutput saved to: {output_file}")
print(f"\nTo replace the original file, run:")
print(f'move /Y "{output_file}" "{input_file}"')
