from pathlib import Path
from PIL import ExifTags, Image

for path in Path('./').rglob('*'):
  #  print(path)
    if path.suffix == ".jpg":
        try:
            img = Image.open (path)     
            exif = img.getexif() 
            shootdate = exif.get(306) #found 36867 in interner - 306 on my linux setup
            #print(exif)  # print all exif field to check where date is stored (after i will comment it)
            if not shootdate is None: #check if shootdata is valid
                print(shootdate)

        except:
            print("problemi problemi problemi")
