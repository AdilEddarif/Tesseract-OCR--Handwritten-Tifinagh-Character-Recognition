import os
import random
from collections import defaultdict

# Input file containing all .lstmf file paths
list_file = r"C:\Users\adile\tesstrain\data\tifinagh\lstmf_list.txt"

# Output files for training and evaluation
train_list_file = r"C:\Users\adile\tesstrain\data\tifinagh\list.train"
eval_list_file = r"C:\Users\adile\tesstrain\data\tifinagh\list.eval"



# Percentage of files to use for evaluation
eval_percentage = 20  # Example: 20%

# Read all .lstmf file paths from the input list
with open(list_file, "r") as f:
    lstmf_files = f.read().splitlines()

# Group .lstmf files by character (assuming filenames contain the character label)
# Example filename: "yu_633.lstmf"
character_groups = defaultdict(list)
for file_path in lstmf_files:
    # Extract character label from filename (modify regex or logic as needed)
    filename = os.path.basename(file_path)  # Get the file name without path
    character_label = filename.split("_")[0]  # Extract character label before '_'
    character_groups[character_label].append(file_path)

# Split each group into training and evaluation
train_files = []
eval_files = []

for character, files in character_groups.items():
    random.shuffle(files)  # Shuffle files for randomness
    split_idx = int(len(files) * eval_percentage / 100)  # Calculate split index
    eval_files.extend(files[:split_idx])  # Add to eval list
    train_files.extend(files[split_idx:])  # Add to train list

# Write the training and evaluation file lists
with open(train_list_file, "w") as f:
    f.write("\n".join(train_files))

with open(eval_list_file, "w") as f:
    f.write("\n".join(eval_files))

print(f"Split completed: {len(train_files)} training files and {len(eval_files)} evaluation files.")
