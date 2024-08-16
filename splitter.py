from spleeter.separator import Separator
import os
import warnings

#filter out warnings (idk if it actually does filter out warnings though)
warnings.filterwarnings('ignore')

def separate_audio(input_file, output_dir):

    # 2 stems splits into vocal and accompaniment
    separator = Separator('spleeter:2stems')

    # Create an output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Perform separation
    separator.separate_to_file(input_file, output_dir)

if __name__ == "__main__":
    input = 'mammamia.mp3'
    output = 'output/'

    separate_audio(input, output)
