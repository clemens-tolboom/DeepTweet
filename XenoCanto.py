import os
import wget
from pydub import AudioSegment

xc_url = 'https://www.xeno-canto.org/'
sample_dir = ''

def set_dir(samples):
    global sample_dir
    sample_dir=samples

def get_mp3_file(xc_id):
    return sample_dir() + '{}.mp3'.format(xc_id)

def get_wav_file(xc_id):
    return sample_dir() + '{}.wav'.format(xc_id)
    
def url_download(xc_id):
    return (xc_url + '{}/download').format(xc_id)

def get_remote_audio_file(xc_id):
    url = url_download(xc_id)
    file_name = get_mp3_file(xc_id)
    if not os.path.exists(file_name):
        print('Downloading', url, file_name)
        wget.download(url, file_name)
        return True
    else:
        print('Already downloaded', xc_id, file_name)
        return False
    # DO NOT USE: this would try to create 1/download
    #wget.download(url, out=sample_dir)

def convert_mp3_to_wav(xc_id):
    get_remote_audio_file(xc_id)
    file_wav = get_wav_file(xc_id)
    if not os.path.exists(file_wav):
        sound = AudioSegment.from_mp3(get_mp3_file(xc_id))
        sound.export(file_wav, format="wav")
        print('mp3 to wav', file_wav)
        return True
    else:
        print('Already converted', xc_id, file_wav)
        return False

def main():
    import tempfile
    test_dir = tempfile.mkdtemp() + '/'
    set_dir(test_dir)
    print('temp dir    :', test_dir)
    print('get_mp3_file:', get_mp3_file(1))
    print('get_wav_file:', get_wav_file(1))

if __name__ == "__main__":
    main()
