import os
import utm

import gcposm.utils
import argument_parser
import qr_code_detector

def load_your_gcp_list(file):
    gcp_list = []
    if os.path.exists(file):
        with open(file, 'r') as infile:
            for line in infile:
                gcp_list.append(line.split("*")[0].split(";"))

    return gcp_list

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
        found_qr_codes = qr_code_detector.get_qr_codes(file)


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



if __name__ == '__main__':
    args = argument_parser.parse_arguments()

    main(args.file)
