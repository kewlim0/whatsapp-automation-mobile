#!/usr/bin/env python3
# Script to remove names from chat_name.txt that appear in processed_chats_2025-12-12.txt

import re

chat_name_file = r"C:\Users\BDC Computer ll\Documents\Appium-test\txt\chat_name.txt"
processed_file = r"C:\Users\BDC Computer ll\Documents\Appium-test\txt\processed_chats_2025-12-12.txt"
output_file = r"C:\Users\BDC Computer ll\Documents\Appium-test\txt\chat_name_cleaned.txt"

# Read processed_chats and extract all chat names (both successful and failed/not found)
print(f"Reading processed chats from: {processed_file}")
processed_names = set()
with open(processed_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            # Extract chat name from formats like:
            # "Row98: NepalWin🇳🇵Rabinkarki"
            # "NOT_FOUND Row86: NepalWin🇳🇵Ppkk9900"
            # "FAILED Row186: NepalWin🇳🇵Sujan2756"
            match = re.search(r'Row\d+:\s*(.+)', line)
            if match:
                chat_name = match.group(1).strip()
                processed_names.add(chat_name)

print(f"Found {len(processed_names)} unique processed chat names")

# Read chat_name.txt
print(f"\nReading chat names from: {chat_name_file}")
with open(chat_name_file, 'r', encoding='utf-8') as f:
    all_chat_names = [line.rstrip('\n') for line in f]

print(f"Total chat names: {len(all_chat_names)}")

# Filter out names that are in the processed list
kept_names = []
removed_count = 0

for name in all_chat_names:
    if name.strip() in processed_names:
        removed_count += 1
    else:
        kept_names.append(name + '\n')

# Write the cleaned list
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(kept_names)

print(f"\n=== Summary ===")
print(f"Original chat names: {len(all_chat_names)}")
print(f"Removed (processed): {removed_count}")
print(f"Remaining names: {len(kept_names)}")
print(f"\nCleaned file saved to: {output_file}")
print(f"\nTo replace the original file, run:")
print(f'move /Y "{output_file}" "{chat_name_file}"')
