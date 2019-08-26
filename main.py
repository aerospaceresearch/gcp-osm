import argparse
import os
import zxing
from pathlib import Path
import utm
import cv2
#from PIL import Image
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

import gcposm.utils


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def load_your_gcp_list(file):

    gcp_list = []
    if os.path.exists(file):
        with open(file, 'r') as infile:
            for line in infile:
                gcp_list.append(line.split("*")[0].split(";"))


    return gcp_list


def two_step_detection(im_thresh, code):
    tmp_path = "tmp" + os.sep
    create_dir(tmp_path)
    tmp_file_name = tmp_path + "temporary_file.jpg"

    # zbar and boundaries generation
    edge_1 = int(code.rect.height * 0.08)
    corner_top = code.rect.top - edge_1
    if corner_top < 0:
        corner_top = 0

    corner_bottom = code.rect.top + code.rect.height + edge_1
    if corner_bottom >= len(im_thresh):
        corner_bottom = len(im_thresh) - 1

    edge_2 = int(code.rect.width * 0.08)
    corner_left = code.rect.left - edge_2
    if corner_left < 0 :
        corner_left = 0

    corner_right = code.rect.left + code.rect.width + edge_2
    if corner_right >= len(im_thresh[0]):
        corner_right = len(im_thresh[0]) - 1


    # zxing needs an image file, so we store one temporary one for it
    cv2.imwrite(tmp_file_name, im_thresh[corner_top : corner_bottom, corner_left : corner_right])

    # zxing doesn't like windows separator and other strange characters, so we just change it
    tmp_file_name = Path(tmp_file_name)
    tmp_file_name = tmp_file_name.absolute().as_uri()
    reader = zxing.BarCodeReader()
    barcode = reader.decode(tmp_file_name, True) # filename, try_harder, does not handle exceptions yet, when the file is NOT an image

    if barcode.format is not None:
        valid = barcode.format is not None and barcode.format == "QR_CODE"
        content = barcode.parsed
        point = [corner_left + barcode.points[1][0], corner_top + barcode.points[1][1]]
        return [valid, content, point]
    else:
        return [False,None,None]

    

def get_qr_codes(file):

    # todo here we could implement more color manipulation to search again in the same image with different threshold
    im_color = cv2.imread(file, cv2.IMREAD_COLOR)
    im_gray = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)
    image_threshold = 128 #  int(np.max(im_gray))-25
    ret, im_thresh = cv2.threshold(im_gray, image_threshold, 255, cv2.THRESH_BINARY)  #, 255, cv2.THRESH_BINARY)

    code_detection = decode(im_thresh, symbols=[ZBarSymbol.QRCODE])
    # https://github.com/NaturalHistoryMuseum/pyzbar/issues/29
    # when symbols=[ZBarSymbol.QRCODE], it checks for all code formats, including barcodes
    # instead of im_thresh, also Image.open(file)


    found_qr_codes = []
    if len(code_detection) > 0:
        for code in code_detection:
            found_qr_codes.append(two_step_detection(im_thresh, code))
        return found_qr_codes

    else:
        print("haven't found any qr-codes in the whole image")
        return [[False, None, None]]



def main(filename):

    print("Hello, starting GCP-OSM...")
    print("")

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
        found_qr_codes = get_qr_codes(file)


        for found_qr_code in found_qr_codes:
            valid, parsed, point = found_qr_code

            if valid:
                print("qr found in", file, parsed,point)

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
                    #print("gcp id", my_gcp_id, "in the local my_gcp_list.txt")


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
                                + str(point[0]) + " "  + str(point[1]) + " "  + file.split(os.sep)[-1])  + "\n")


            else:
                print("qr not found in", file)


    f.close()
    print("")
    print("GCP-OSM is finished, Good Bye!")


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
