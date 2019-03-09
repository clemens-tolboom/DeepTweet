import os

data_dir = ''

def get_project_dir():
    return os.path.dirname(__file__) + '/'

def set_data_dir(directory):
    global data_dir
    data_dir = directory
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)

    if not os.path.isdir(get_gbif_dir()):
        os.mkdir(get_gbif_dir())

    if not os.path.isdir(get_sample_dir()):
        os.mkdir(get_sample_dir())

    if not os.path.isdir(get_fragments_dir()):
        os.mkdir(get_fragments_dir())

def get_data_dir():
    global data_dir
    return data_dir

def get_gbif_dir():
    global data_dir

    return get_data_dir() + 'gbif/'

def get_sample_dir():
    return get_data_dir() + 'samples/'

def get_fragments_dir():
    return get_sample_dir() + 'fragments/'

def print_stats():
    print('Project   :', get_project_dir())
    print('Data      :', get_data_dir())
    print('GBIF      :', get_gbif_dir())
    print('sample    :', get_sample_dir())
    print('fragments :', get_fragments_dir())

def fix_gbif_df(df):
    # We can now follow this link which redirects to XC site page.
    #df['occurrenceID'].astype('|S')
    #df['occurrenceID'].head()

    # So we better do this redirect outself by adding the XC_ID
    df['XC_ID'] = df['occurrenceID']
    df['XC_ID'] = df['XC_ID'].map(lambda x: x.rsplit('/', 1)[1]
                             .replace('XC', '')
                             .lstrip('0'))

