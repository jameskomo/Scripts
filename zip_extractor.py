import os
import glob
import zipfile
from zipfile import ZipFile


def extract_zip(dir):
    for dir in glob.iglob(f'{dir}/*', recursive=True):
        (dirname, filename) = os.path.split(dir)
        file_name=os.path.basename(dir).split('.')[0]
        # Check if file is zip file as zipfile module complains if other formats present
        if not zipfile.is_zipfile(dir):
            continue
        with ZipFile(dir, 'r') as zipObj:
            print("Extracted to: "+file_name)
            zipObj.extractall(path=f"{dirname}/{file_name}")
            os.remove(dir)