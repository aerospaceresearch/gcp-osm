import argparse
import os

def parse_arguments():
    """
    Argument parsing is implemented with https://pymotw.com/2/argparse/

    Currently only one argument is required:
    -f or --file to provide the file(s) that should be parsed
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', action='store', default=os.sep,
                        dest='file',
                        help='load in the file or folder',
                        required=True)

    parser.add_argument('-o', '--output-file', action='store', default='gcp_list.txt',
                        dest='output_file',
                        help='name of the output file (default: gcp-list.txt)')

    parser.add_argument('--debug', action='store_true',
                        dest='is_debug',
                        help='Show processed images for debugging purposes')

    return parser.parse_args()

if __name__ == '__main__':
    '''imported'''
