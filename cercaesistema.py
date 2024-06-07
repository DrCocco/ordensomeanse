from pathlib import Path
from PIL import ExifTags, Image
import os
import shutil
import ffmpeg
import re

# Source and Destination directory
src_dir = "/home/fede/Documents/python/foto/"
dst_dir = "/home/fede/Documents/python/ordered/"

# Funzione per spostare i file senza data nei metadati nella cartella "unsorted"
def move2unsorted(path):
    filename = Path(path).name
    print(f"Moving {filename} to /unsorted")

    dst_unsorted = os.path.join(dst_dir, "unsorted")
    dst_path = os.path.join(dst_unsorted, filename)
    print(dst_path)

    if not os.path.exists(dst_unsorted):
        os.makedirs(dst_unsorted)

    if not os.path.exists(dst_path):
        shutil.move(path, dst_path)

# Creare la directory di destinazione se non esiste
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

# Funzione per ottenere la data di creazione del video
def get_creation_date(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        creation_time = None
        for stream in probe['streams']:
            if 'tags' in stream and 'creation_time' in stream['tags']:
                creation_time = stream['tags']['creation_time']
                break
        return creation_time
    except ffmpeg.Error as e:
        print(f"Error getting creation date for {video_path}: {e}")
        return None

# Funzione per ottenere la data di scatto della foto
def get_photo_date(photo_path):
    try:
        img = Image.open(photo_path)
        exif = img.getexif()
        shootdate = exif.get(306)  # Il tag 306 corrisponde alla data di creazione
        return shootdate
    except Exception as e:
        print(f"Error getting photo date for {photo_path}: {e}")
        return None

# Funzione per estrarre la data dal nome del file
def extract_date_from_filename(filename):
    date_pattern = re.compile(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})')
    match = date_pattern.search(filename)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"
    return None

# Funzione principale per processare i file
def process_file(path):
    filename = Path(path).name  # Nome del file per costruire il percorso di destinazione

    # Determinare il tipo di file (foto o video)
    is_photo = path.suffix.lower() in [".jpeg", ".png", ".jpg"]
    is_video = path.suffix.lower() in [".mp4", ".mov", ".avi", ".mkv"]

    if is_photo:
        creation_date = get_photo_date(path)
    elif is_video:
        creation_date = get_creation_date(path)
    else:
        creation_date = None

    if not creation_date:
        creation_date = extract_date_from_filename(filename)

    if creation_date:
        year = creation_date[:4]
        month = creation_date[5:7]

        # Costruire il percorso di destinazione
        dst_year_dir = os.path.join(dst_dir, year)
        dst_month_dir = os.path.join(dst_year_dir, month)
        dst_path = os.path.join(dst_month_dir, filename)

        # Creare le directory di destinazione se non esistono
        if not os.path.exists(dst_year_dir):
            os.makedirs(dst_year_dir)
            print(f"Creating year directory {dst_year_dir}")

        if not os.path.exists(dst_month_dir):
            os.makedirs(dst_month_dir)
            print(f"Creating month directory {dst_month_dir}")

        if not os.path.exists(dst_path):
            shutil.move(path, dst_path)
            print(f"Moved {filename} to {dst_month_dir}")
    else:
        print(f"Creation date not found in {filename}")
        move2unsorted(path)

# Iterare su tutti i file nella directory di origine
for path in Path(src_dir).rglob('*'):
    if path.is_file():
        process_file(path)

    # Rimuovere le directory vuote
    if path.is_dir() and len(os.listdir(path)) == 0:
        print(f"{path} is an empty directory")
        os.rmdir(path)

print("done")
