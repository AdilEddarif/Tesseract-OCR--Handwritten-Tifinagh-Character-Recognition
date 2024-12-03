import os
import subprocess
import logging
from datetime import datetime

# Configure logging
log_file = "generate_boxes_log.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# Paths
ground_truth_dir = r"C:\Users\adile\tesstrain\data\tifinagh-ground-truth"
generate_box_script = r"C:\Users\adile\tesstrain\generate_line_box.py"

# Supported image formats
image_extensions = ['.png', '.jpg', '.jpeg', '.tif']

tifinagh_dict = {
    "ya": "ⴰ",
    "yab": "ⴱ",
    "yach": "ⵛ",
    "yad": "ⴷ",
    "yadd": "ⴹ",
    "yae": "ⵄ",
    "yaf": "ⴼ",
    "yag": "ⴳ",
    "yagh": "ⵖ",
    "yagw": "ⴳⵯ",
    "yah": "ⵀ",
    "yahh": "ⵃ",
    "yaj": "ⵊ",
    "yak": "ⴽ",
    "yakw": "ⴽⵯ",
    "yal": "ⵍ",
    "yam": "ⵎ",
    "yan": "ⵏ",
    "yaq": "ⵇ",
    "yar": "ⵔ",
    "yarr": "ⵕ",
    "yas": "ⵙ",
    "yass": "ⵚ",
    "yat": "ⵜ",
    "yatt": "ⵟ",
    "yaw": "ⵡ",
    "yax": "ⵅ",
    "yay": "ⵢ",
    "yaz": "ⵣ",
    "yazz": "ⵥ",
    "yey": "ⴻ",
    "yi": "ⵉ",
    "yu": "ⵓ"
}


# Default box dimensions
default_box_dimensions = "0 0 128 128 0\n"

# Process each image
all_files_processed = 0
files_skipped = 0
default_boxes_created = 0

for file in os.listdir(ground_truth_dir):
    if any(file.endswith(ext) for ext in image_extensions):
        base_name = os.path.splitext(file)[0]
        image_path = os.path.join(ground_truth_dir, file)
        gt_text_path = os.path.join(ground_truth_dir, base_name + ".gt.txt")
        box_path = os.path.join(ground_truth_dir, base_name + ".box")

        # Identify the Tifinagh character from the dictionary
        prefix = base_name.split("_")[0]  # Extract the prefix (e.g., "ya" from "ya_1")
        tifinagh_char = tifinagh_dict.get(prefix, "DEFAULT")

        if os.path.exists(gt_text_path):
            try:
                logging.info(f"Processing file: {file}")
                logging.debug(f"Generating box file for {file}...")

                # Execute the command to generate the box
                command = [
                    "python", generate_box_script,
                    "-i", image_path,
                    "-t", gt_text_path
                ]
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Check for successful box generation
                if result.returncode == 0 and "Mismatch" not in result.stdout:
                    with open(box_path, 'w', encoding='utf-8') as box_file:
                        box_file.write(result.stdout)
                    logging.debug(f"Box file successfully created: {box_path}")
                    all_files_processed += 1
                else:
                    # Handle contour mismatch by creating a default box file
                    logging.warning(f"Contour mismatch or error for {file}. Writing default box.")
                    with open(box_path, 'w', encoding='utf-8') as box_file:
                        box_file.write(f"{tifinagh_char} {default_box_dimensions}")
                    logging.debug(f"Default box file created: {box_path}")
                    default_boxes_created += 1
            except Exception as e:
                logging.error(f"Exception occurred while processing {file}: {e}")
                files_skipped += 1
        else:
            logging.warning(f"Ground truth file missing for {file}, skipping.")
            files_skipped += 1

# Summary
logging.info(f"Box file generation completed. Processed: {all_files_processed}, Skipped: {files_skipped}, Default Boxes Created: {default_boxes_created}")
