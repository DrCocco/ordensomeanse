from pathlib import Path
from PIL import ExifTags, Image
import os
import shutil

#Source and Destination directory
src_dir = "/home/fede/Documents/python/foto/"
dst_dir = "/home/fede/Documents/python/ordered/"

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

for path in Path(src_dir).rglob('*'):
    #print(path)
    if path.suffix == ".jpeg" or path.suffix == ".png" or path.suffix == ".jpg":
        #try:
            filename = Path(path).name #used after to build complete dest path
            #print(filename)     

            #EXIF
            img = Image.open (path)
            exif = img.getexif() 
            shootdate = exif.get(306) #found 36867 in internet - 306 on my linux setup
            #print(exif)  # print all exif field to check where date is stored (after i will comment it)
            
            if not shootdate is None: #check if shootdate is valid
                
                year = shootdate[0:4] 
                month = shootdate[5:7]
                
               # print(year+" "+month) 

                #build dest path
                dst_year_dir = os.path.join(dst_dir,str(year))
                dst_month_dir = os.path.join(dst_year_dir,str(month))
                dst_path = os.path.join(dst_month_dir,filename)
                
                #create dest directory if no exist
                if not os.path.exists(dst_year_dir):
                    os.makedirs(dst_year_dir)
                    print("creating year directory "+yeadst_year_dir)

                if not os.path.exists(dst_month_dir):
                    os.makedirs(dst_month_dir)
                    print("creating month directory "+dst_month_dir)

                if not os.path.exists(dst_path):
                    shutil.move(path,dst_path)
                    print(f"Spostato {filename} in {dst_month_dir}")
            else:
                print(f"Non ho trovato EXIF nel file {filename}")
                print(f"sposto il file {filename} nella cartella Unsorted")

                dst_unsorted =os.path.join(dst_dir,str("unsorted"))
                dst_path = os.path.join(dst_unsorted,filename)
                print(dst_path)

                if not os.path.exists(dst_unsorted):
                    os.makedirs(dst_unsorted)

                if not os.path.exists(dst_path):
                    shutil.move(path,dst_path)



        #except:
        #    print("problemi problemi problemi")

print("done")
