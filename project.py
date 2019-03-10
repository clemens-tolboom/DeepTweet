import os
import gbif
import pandas as pd
import XenoCanto as xc
import split

data_dir = ''


def get_project_dir():
    return os.path.dirname(__file__) + '/'


def set_data_dir(directory):
    global data_dir
    data_dir = directory

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(get_gbif_dir(), exist_ok=True)
    os.makedirs(get_sample_dir(), exist_ok=True)
    os.makedirs(get_fragments_dir(), exist_ok=True)

    xc.set_dir(get_sample_dir)


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


def get_fragments_path(df, xc_id):
    """
    We want to map the GBIF taxonomy into a directory tree

    {kingdom}/{phylum}/{class}/{order}/{family}/{genus}/{species}
    """
    row = df[df['XC_ID'] == xc_id].iloc[0]
    path = '{kingdom}/{phylum}/{class}/{order}/{family}/{genus}/{species}/'.format(**row)
    return get_fragments_dir() + path


def build_fragments(df, args):
    xc_id = '100113'

    xc.convert_mp3_to_wav(xc_id)

    in_file = xc.get_wav_file(xc_id)

    out_path = get_fragments_path(df, xc_id)
    os.makedirs(out_path, exist_ok=True)

    print(in_file, 'file://' + out_path)

    args['output_dir'] = out_path
    split.split(in_file, args)


def main():
    print(get_project_dir())
    set_data_dir(get_project_dir() + 'data/')
    print_stats()

    gbif.set_gbif_dir(get_gbif_dir())
    df = pd.read_csv(gbif.get_data(), sep='\t')
    fix_gbif_df(df)

    xc_id = df['XC_ID'].iloc[0]
    print(get_fragments_path(df, xc_id))

    args = dict(split.defaults)

    args['silence_threshold'] = 0.01
    args['min_silence_length'] = 1.0
    args['dry_run'] = False

    build_fragments(df, args)


if __name__ == '__main__':
    main()
