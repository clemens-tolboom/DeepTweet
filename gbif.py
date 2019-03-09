import os
import wget
import zipfile

# 'http://api.gbif.org/v1/occurrence/download/request/0025627-181108115102211.zip'

gbif_url = 'http://api.gbif.org/v1/occurrence/download/request/{}.zip'

_gbif_dir = ''
_gbif_id = '0025627-181108115102211'

def set_gbif_dir(gbif_dir):
    global _gbif_dir
    _gbif_dir = gbif_dir

def get_gbif_dir():
    global _gbif_dir
    return _gbif_dir

def set_gbif_id(gbif_id):
    global _gbif_id
    _gbif_id = gbif_id

def get_gbif_id():
    global _gbif_id
    return _gbif_id

def get_path_zip():
    return get_gbif_dir() + '{}.zip'.format(get_gbif_id())

def get_path_csv():
    return get_gbif_dir() + '{}.csv'.format(get_gbif_id())

def download():
    if not os.path.isdir(get_gbif_dir()):
        print( 'Trying to create', get_gbif_dir())
        os.mkdir(get_gbif_dir())

    zip_file = get_path_zip()

    if not os.path.exists(zip_file):
        url = gbif_url.format(get_gbif_id())
        print('Downloading', url, get_gbif_id())
        wget.download(url, out=dir)
    else:
        print('Already downloaded zip', get_gbif_id())
        return False

def unzip():
    gbif_zip = get_gbif_dir() + '{}.zip'.format(get_gbif_id())

    zip_ref = zipfile.ZipFile(gbif_zip, 'r')
    zip_ref.extractall(get_gbif_dir())
    zip_ref.close()

def get_data():
    download()
    unzip()
    return get_path_csv()

def print_stats():
    print("GBIF ID:", get_gbif_id())
