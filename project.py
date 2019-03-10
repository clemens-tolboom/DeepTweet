import os
import gbif
import pandas as pd

data_dir = ''


def get_project_dir():
    return os.path.dirname(__file__) + '/'


def set_data_dir(directory):
    global data_dir
    data_dir = directory

    os.makedirs(data_dir, exist_ok=True)

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
    return get_data_dir() + 'xc/'


def get_fragments_dir():
    return get_data_dir() + 'fragments/'


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


def get_sample_path(df, xc_id):
    """
    We want to map the GBIF taxonomy into a directory tree

    {kingdom}/{phylum}/{class}/{order}/{family}/{genus}/{species}
    """
    row = df[df['XC_ID'] == xc_id].iloc[0]
    path = '{kingdom}/{phylum}/{class}/{order}/{family}/{genus}/{species}/'.format(**row)
    return get_fragments_dir() + path


def main():
    print(get_project_dir())
    set_data_dir(get_project_dir() + 'data/')
    print_stats()

    gbif.set_gbif_dir(get_gbif_dir())
    df = pd.read_csv(gbif.get_data(), sep='\t')
    fix_gbif_df(df)

    xc_id = df['XC_ID'].iloc[0]
    print(get_sample_path(df, xc_id))


if __name__ == '__main__':
    main()
