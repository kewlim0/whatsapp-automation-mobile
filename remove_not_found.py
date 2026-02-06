#!/usr/bin/env python3
# Script to remove names from chat_name.txt that appear in not_found_chats.txt

import re

chat_name_file = r"C:\Users\BDC Computer ll\Documents\Appium-test\txt\chat_name.txt"
not_found_file = r"C:\Users\BDC Computer ll\Documents\Appium-test\txt\not_found_chats_20251211.txt"
output_file = r"C:\Users\BDC Computer ll\Documents\Appium-test\txt\chat_name_cleaned.txt"

# Read not_found_chats.txt and extract all chat names (excluding timestamps)
print(f"Reading not found chats from: {not_found_file}")
not_found_names = set()
with open(not_found_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        # Skip empty lines and timestamp lines (those starting with '[')
        if line and not line.startswith('['):
            not_found_names.add(line)

print(f"Found {len(not_found_names)} unique not-found chat names")

# Read chat_name.txt
print(f"\nReading chat names from: {chat_name_file}")
with open(chat_name_file, 'r', encoding='utf-8') as f:
    all_chat_names = [line.rstrip('\n') for line in f]

print(f"Total chat names: {len(all_chat_names)}")

# Filter out names that are in the not_found list
kept_names = []
removed_count = 0

for name in all_chat_names:
    if name.strip() in not_found_names:
        removed_count += 1
    else:
        kept_names.append(name + '\n')

# Write the cleaned list
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(kept_names)

print(f"\n=== Summary ===")
print(f"Original chat names: {len(all_chat_names)}")
print(f"Removed (not found): {removed_count}")
print(f"Remaining names: {len(kept_names)}")
print(f"\nCleaned file saved to: {output_file}")
print(f"\nTo replace the original file, run:")
print(f'move /Y "{output_file}" "{chat_name_file}"')
