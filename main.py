import os

import gcposm.utils
import argument_parser
import qr_code_extractor


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
        found_qr_codes = qr_code_extractor.get_qr_data(file, debug_show_image=args.is_debug)
        print(found_qr_codes)

    print("")
    print("GCP-OSM is finished, Good Bye!")


if __name__ == '__main__':
    args = argument_parser.parse_arguments()

    main(args.file)
