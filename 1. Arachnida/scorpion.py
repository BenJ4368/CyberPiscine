from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ExifTags
import argparse

def open_tabs(file_paths, root):
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    for file_path in file_paths:
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
            
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    exif_text.insert(END, f"{tag}: {value}\n")
            else:
                exif_text.insert(END, "No EXIF data found.")

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
