import os
from PIL import Image
import time

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')

dataset_dir = r'C:\Users\angel\OneDrive\Desktop\NUTRITION_DEFICIENCY (3)\dataset\nutretion\archive (7)\dataset'

removed = 0
skipped = 0

for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        file_path = os.path.join(root, file)

        # Remove non-image files
        if not file.lower().endswith(IMAGE_EXTENSIONS):
            try:
                os.remove(file_path)
                print("Removed non-image:", file_path)
                removed += 1
            except PermissionError:
                print("Skipped (locked):", file_path)
                skipped += 1
            continue

        # Check corrupted images
        try:
            img = Image.open(file_path)
            img.verify()
            img.close()
        except Exception:
            try:
                time.sleep(0.1)  # allow Windows to release file
                os.remove(file_path)
                print("Removed corrupted image:", file_path)
                removed += 1
            except PermissionError:
                print("Skipped corrupted (locked):", file_path)
                skipped += 1

print("\nDataset cleaning complete")
print("Total removed:", removed)
print("Total skipped (locked):", skipped)
