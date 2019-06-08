import argparse
import os
import zxing
from pathlib import Path

import gcposm.utils


def get_qr_codes(processing_files):
    for file in processing_files:

        # zxing doesn't like windows separator and other strange characters, so we just change it
        file = Path(file)
        file = file.absolute().as_uri()

        reader = zxing.BarCodeReader()
        barcode = reader.decode(file)
        # does not handle exceptions yet, when the file is NOT an image

        if barcode is not None:
            print("decoding", file)
            print(barcode.format)
            print(barcode.type)
            print(barcode.raw)
            print(barcode.parsed)
            print(barcode.points)
            print()


def main(filename):
    if os.path.isdir(args.file):
        print("loading in all files in folder:", filename)
        processing_files = gcposm.utils.get_all_files(filename)

    elif os.path.isfile(args.file):
        print("loading in this file:", filename)
        processing_files = gcposm.utils.get_one_file(filename)
    else:
        print("neither file nor folder. ending programm.")
        return

    get_qr_codes(processing_files)


def getArgs():
    """
    defining the input parameters by the arguments.

    src: https://pymotw.com/2/argparse/

    :return: args
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--from', action='store', default="/",
                        dest='file',
                        help='load in the file or folder')

    # parser.add_argument('--version', action='version', version='0.0')

    return parser.parse_args()


if __name__ == '__main__':
    args = getArgs()

    main(args.file)
