import os
import time
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ExifTags
import argparse

def get_metadata(file_path):
    metadata = {}
    try:
        with Image.open(file_path) as img:
            metadata["file_name"] = os.path.basename(file_path)
            metadata["mime_type"] = Image.MIME.get(img.format, "Unknown")
            metadata["file_size"] = os.path.getsize(file_path)
            metadata["dimensions"] = img.size
            metadata["creation_date"] = time.ctime(os.path.getctime(file_path))

            exif_data = img._getexif()
            if exif_data:
                metadata["exif_data"] = {
                    ExifTags.TAGS.get(tag_id, tag_id): value
                    for tag_id, value in exif_data.items()
                    if tag_id in ExifTags.TAGS
                }
            else:
                metadata["exif_data"] = "No EXIF data found."

    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
        metadata = None
    return metadata



def open_tabs(file_paths, root):
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    
    for file_path in file_paths:
        metadata = get_metadata(file_path)
        if not metadata:
            continue
        
        try:
            
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)

            frame = Frame(notebook)
            label = Label(frame, image=photo)
            label.image = photo  # Keep a reference to avoid garbage collection
            label.pack(padx=10, pady=10, anchor="w")
         
            exif_text = Text(frame, wrap="word", width=80)
            exif_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            exif_text.insert(END, f"File Name: {metadata['file_name']}\n")
            exif_text.insert(END, f"MIME Type: {metadata['mime_type']}\n")
            exif_text.insert(END, f"File Size: {metadata['file_size']} bytes\n")
            exif_text.insert(END, f"Dimensions: {metadata['dimensions'][0]}x{metadata['dimensions'][1]}\n")
            exif_text.insert(END, f"Creation Date: {metadata['creation_date']}\n")
        
            if isinstance(metadata["exif_data"], dict) and metadata["exif_data"]:
                exif_text.insert(END, "\nEXIF Data:\n")
                for tag, value in metadata["exif_data"].items():
                    exif_text.insert(END, f"{tag}: {value}\n")
            else:
                exif_text.insert(END, "No EXIF data found.\n")

            notebook.add(frame, text=file_path.split("/")[-1])  # Use the file name as the tab title
        except Exception as e:
            print(f"Error opening {file_path}: {e}")



def main():
    parser = argparse.ArgumentParser(description="Scorpion: EXIF data modifier")
    parser.add_argument("file_paths", nargs="+", type=str, help="Path of the image")
    args = parser.parse_args()

    # Create the main window "root"
    root = Tk()
    root.title("Scorpion")
    root.geometry("1080x720")
    root.resizable(False, False)
    exit_button = Button(root, text="Exit", command=root.destroy)
    exit_button.pack(side="bottom", pady=10)
    # Put images in tabs
    open_tabs(args.file_paths, root)

    root.mainloop()

if __name__ == "__main__":
    main()
