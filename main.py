import argparse
import os


def main(args):
    if os.path.isdir(args.file) == False and os.path.isfile(args.file) == False:
        print("neither file nor folder. ending programm.")

    if os.path.isdir(args.file) == True:
        print("loading in all files in folder:", args.file)

    elif os.path.isfile(args.file) == True:
        print("loading in this file:", args.file)


def getArgs():
    '''
    defining the input parameters by the arguments.

    src: https://pymotw.com/2/argparse/

    :return: args
    '''

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--from', action='store', default="/",
                        dest='file',
                        help='load in the file or folder')

    #parser.add_argument('--version', action='version', version='0.0')

    return parser.parse_args()

if __name__ == '__main__':
    args = getArgs()

    main(args)