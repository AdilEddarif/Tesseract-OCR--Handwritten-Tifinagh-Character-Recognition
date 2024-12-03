#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import sys
from collections import defaultdict


def split_file_by_character(input_file, ratio):
    """
    Splits a text file into list.train and list.eval with a specified ratio for each character.
    Each character group is split proportionally.
    """
    if not isinstance(input_file, pathlib.Path):
        input_file = pathlib.Path(input_file)
    if not input_file.exists():
        print(f"'{input_file}' does not exist!")
        return False

    # Read all lines from the input file
    lines = input_file.read_text().splitlines()

    # Group lines by character (e.g., "yu", "yab" from filenames)
    character_groups = defaultdict(list)
    for line in lines:
        # Extract character from the filename (modify as needed based on your filename format)
        filename = pathlib.Path(line).name
        character_label = filename.split("_")[0]  # Example: "yu" from "yu_633.lstmf"
        character_groups[character_label].append(line)

    # Prepare output files
    output_dir = input_file.resolve().parent
    train_list = pathlib.Path(output_dir, "list.train")
    eval_list = pathlib.Path(output_dir, "list.eval")

    # Write train and eval files
    with open(train_list, "w", newline="\n") as f_train, open(eval_list, "w", newline="\n") as f_eval:
        for character, files in character_groups.items():
            split_point = int(ratio * len(files))  # Calculate split point for each group
            f_train.write("\n".join(files[:split_point]) + "\n")
            f_eval.write("\n".join(files[split_point:]) + "\n")

    print(f"Split completed: Train list: {train_list}, Eval list: {eval_list}")
    return True


# Default ratio and input file
ratio = 0.95
input_file = None

# Parse command-line arguments
if len(sys.argv) > 1:
    input_file = sys.argv[1]
if len(sys.argv) > 2:
    ratio = float(sys.argv[2])

# Call the function
if input_file:
    split_file_by_character(input_file, ratio)
else:
    print("Usage: script.py <input_file> [ratio]")
