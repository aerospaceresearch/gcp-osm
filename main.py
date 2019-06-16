import argparse
import os
import zxing
from pathlib import Path
import utm

import gcposm.utils


def load_your_gcp_list(file):

    gcp_list = []
    if os.path.exists(file):
        with open(file, 'r') as infile:
            for line in infile:
                gcp_list.append(line.split("*")[0].split(";"))


    return gcp_list


def get_qr_codes(file):
    # zxing doesn't like windows separator and other strange characters, so we just change it
    file = Path(file)
    file = file.absolute().as_uri()

    reader = zxing.BarCodeReader()
    barcode = reader.decode(file, True)
    # filename, try_harder = True
    # does not handle exceptions yet, when the file is NOT an image

    return barcode.format, barcode.type, barcode.raw, barcode.parsed, barcode.points


def main(filename):

    # preparation
    gcp_list = load_your_gcp_list("my_gcp_list.txt")
    f = open("gcp_list.txt", "w")
    odm_gcp_header = 0


    # now working time
    if os.path.isdir(args.file):
        print("loading in all files in folder:", filename)
        processing_files = gcposm.utils.get_all_files(filename)

    elif os.path.isfile(args.file):
        print("loading in this file:", filename)
        processing_files = gcposm.utils.get_one_file(filename)

    else:
        print("neither file nor folder. ending programm.")
        return

    for file in processing_files:
        format, type, raw, parsed, points = get_qr_codes(file)

        if format is not None:
            print("qr found in", file, parsed)

            #do stuff now...

            ## type indicator cases
            if parsed.find("/n/") > -1:
                print("type indicator: n/ = OSM Node ID with Basis 64")

            if parsed.find("/w/") > -1:
                print("type indicator: w/ = OSM Way ID with Basis 64")

            if parsed.find("/a/") > -1:
                print("type indicator: a/ = OSM Area ID with Basis 64")

            if parsed.find("/r/") > -1:
                print("type indicator: r/ = OSM Relation ID with Basis 64")

            if parsed.find("/g/") > -1:
                print("type indicator: g/ = OSM Shortlink quadtiles format")

            my_gcp_id = parsed
            # when the local id was found with a type indicator, it will be replaced.
            # otherwise the parsed text will directly be used in the next "simple locally defined payload" method.

            if parsed.find("/l/") > -1:
                print("type indicator: l/ = locally defined payload")
                my_gcp_id = parsed.split("l/")[1]
                print("gcp id", my_gcp_id, "in the local my_gcp_list.txt")


            ## simple locally defined payloads
            for item in gcp_list:
                if my_gcp_id == item[0]:
                    print("\t found a known gcp (", item[1] ,"/", item[2] ,"/", item[3] ,") from your list")
                    location_utm = utm.from_latlon(float(item[1]), float(item[2]))


                    # OpenDroneMap GCP
                    ## header
                    if odm_gcp_header == 0:
                        # this is still to understood, why ODM just allows one utm zone and that is in the header!
                        f.write("WGS84 UTM " + str(location_utm[2]) + str(location_utm[3]) + "\n")
                        odm_gcp_header = 1

                    ## line by line saving the coordinates
                    f.write((str(location_utm[0]) + " " + str(location_utm[1]) + " "  + item[3] + " "
                             + str(points[1][0]) + " "  + str(points[1][1]) + " "  + file.split(os.sep)[-1])  + "\n")


        else:
            print("qr not found in", file)


    f.close()


def getArgs():
    """
    defining the input parameters by the arguments.

    src: https://pymotw.com/2/argparse/

    :return: args
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--from', action='store', default=os.sep,
                        dest='file',
                        help='load in the file or folder',
                        required=True)

    # parser.add_argument('--version', action='version', version='0.0')

    return parser.parse_args()


if __name__ == '__main__':
    args = getArgs()


    main(args.file)
