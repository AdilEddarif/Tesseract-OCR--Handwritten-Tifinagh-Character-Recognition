#!/usr/bin/env python3

import argparse
import io
import unicodedata
from PIL import Image
import cv2
import numpy as np

def main():
    #
    # Command line arguments
    #
    arg_parser = argparse.ArgumentParser(
        """Creates tesseract box files for given (line) image text pairs"""
    )

    # Text ground truth
    arg_parser.add_argument(
        '-t',
        '--txt',
        nargs='?',
        metavar='TXT',
        help='Line text (GT)',
        required=True,
    )

    # Image file
    arg_parser.add_argument(
        '-i',
        '--image',
        nargs='?',
        metavar='IMAGE',
        help='Image file',
        required=True,
    )

    args = arg_parser.parse_args()

    #
    # Main
    #

    # Load the image
    image = Image.open(args.image).convert("L")  # Convert to grayscale
    np_image = np.array(image)

    # Apply Otsu's thresholding
    _, binary_image = cv2.threshold(np_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invert the binary image if needed
    if np.mean(binary_image) > 127:
        binary_image = cv2.bitwise_not(binary_image)

    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Load ground truth
    with io.open(args.txt, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        if len(lines) != 1:
            raise ValueError(
                f'ERROR: {args.txt}: Ground truth text file should contain exactly one line, not {len(lines)}'
            )
        line = unicodedata.normalize('NFC', lines[0].strip())

    if line:
        # Check if the number of characters matches the contours
        if len(line) != len(contours):
            print(f"WARNING: Mismatch between characters ({len(line)}) and contours ({len(contours)}). Skipping.")
            return

        # Sort contours from left to right
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        sorted_boxes = sorted(zip(bounding_boxes, line), key=lambda b: b[0][0])

        # Generate box file content
        box_file = args.image.replace(".png", ".box")
        with open(box_file, 'w', encoding='utf-8') as box_out:
            for (x, y, w, h), char in sorted_boxes:
                if not char.strip():
                    print(f"Skipping empty character in {args.image}")
                    continue  # Skip empty characters
                box_out.write(f'{char} {x} {image.height - (y + h)} {x + w} {image.height - y} 0\n')
                print(f"Written: {char} {x} {image.height - (y + h)} {x + w} {image.height - y}")

        print(f"Successfully generated box file: {box_file}")

if __name__ == "__main__":
    main()
