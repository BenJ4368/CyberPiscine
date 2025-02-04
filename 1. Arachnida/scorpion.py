import os
import argparse
from PIL import Image
import piexif

# Target image extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}

# Check if the file is a valid image
def is_valid_image(file_path):
    return os.path.splitext(file_path)[1].lower() in ALLOWED_EXTENSIONS

# Parse EXIF and other metadata
def parse_exif_and_metadata(file_path):
    try:
        with Image.open(file_path) as img:

            print(f"\n====== {file_path}")
            print(f"[Basic data]")
            print(f"    Format : {img.format}")
            print(f"    Mode : {img.mode}")
            print(f"    Size : {img.size} (width x height)")
            
            # EXIF data extraction
            exif_data = img.getexif()
            print("\n[EXIF Data]:")
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = piexif.TAGS.get(tag_id, {}).get("name", tag_id)
                    print(f"  {tag_name}: {value}")
            else:
                print(f"    No EXIF data found.")

            # Other metadata extraction
            if img.info:
                print("\n[Other]:")
                for key, value in img.info.items():
                    print(f"  {key}: {value}")

    except Exception as e:
        print(f"Error while analysing {file_path} : {e}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Scoprion")
    parser.add_argument("files", type=str, nargs="+", help="Files to parse")
    args = parser.parse_args()

    for file_path in args.files:
        if os.path.exists(file_path) and is_valid_image(file_path):
            parse_exif_and_metadata(file_path)
        else:
            print(f"\n{file_path} is not a valid image file.")

if __name__ == "__main__":
    main()