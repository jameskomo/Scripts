import os
import glob
import zipfile
from zipfile import ZipFile


def extract_zip():
    for dir in glob.iglob('/home/komo/Pictures/*', recursive=True):
        # Extracting zip file name to allow extracting to same file name in same path
        # file_name=dir.split('/').pop().split('.')[0]
        file_name=os.path.basename(dir).split('.')[0]
        # Check if file is zip file as zipfile module complains if not
        if not zipfile.is_zipfile(dir):
            continue
        with ZipFile(dir, 'r') as zipObj:
            print(file_name)
            zipObj.extractall(path=f"/home/komo/Pictures/{file_name}")
            os.remove(dir)
extract_zip()