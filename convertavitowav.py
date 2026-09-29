

import subprocess

def avi_to_wav(input_avi, output_wav):
    subprocess.check_output(['ffmpeg', '-i', input_avi, '-vn', '-acodec', 'pcm_s16le', output_wav], stderr=subprocess.DEVNULL)
