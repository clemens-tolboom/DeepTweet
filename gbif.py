import os
import wget
import zipfile

# 'http://api.gbif.org/v1/occurrence/download/request/0025627-181108115102211.zip'

gbif_url = 'http://api.gbif.org/v1/occurrence/download/request/{}.zip'

default_id = '0025627-181108115102211'

def get_path_zip(dir, id):
    return dir + '{}.zip'.format(id)

def get_path_csv(dir, id):
    return dir + '{}.csv'.format(id)

def download(dir, id):
    if not os.path.isdir(dir):
        print( 'Trying to create', dir)
        os.mkdir(dir)

    zip_file = get_path_zip(dir, id)

    if not os.path.exists(zip_file):
        print('Downloading', url, id)
        url = gbif_url.format(id)
        wget.download(url, out=dir)
    else:
        print('Already downloaded zip', id)
        return False

def unzip(dir, id):
    gbif_zip = dir + '{}.zip'.format(id)

    zip_ref = zipfile.ZipFile(gbif_zip, 'r')
    zip_ref.extractall(dir)
    zip_ref.close()

def get_data(dir, id):
    download(dir, id)
    unzip(dir,id)
    return get_path_csv(dir,id)
