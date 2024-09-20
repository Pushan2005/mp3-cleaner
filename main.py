import os
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3
from tqdm import tqdm

mp3_files = []
skipped_files = []

def del_metadata(file_path):
    file_name = os.path.basename(file_path)    
    try:
        song = MP3(file_path, ID3=ID3)
        if song.tags is not None:
            song.delete()
        song.save()
    except HeaderNotFoundError:
        skipped_files.append(file_name)

def scan_folder(directory):
    total_files = sum([len(files) for _, _, files in os.walk(directory)])
    with tqdm(total=total_files, desc="Scanning files") as pbar:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.mp3'):
                    file_path = os.path.join(root, file)
                    mp3_files.append(file_path)
                pbar.update(1)
    
    with tqdm(total=len(mp3_files), desc="Cleaning files") as pbar:
        for file_path in mp3_files:        
            del_metadata(file_path)
            pbar.update(1)
    for skipped_file in skipped_files:
        print(f"Skipped {skipped_file}: not a valid MP3 file")
    print("Done!")

current_directory = os.path.dirname(os.path.abspath(__file__))
scan_folder(current_directory)