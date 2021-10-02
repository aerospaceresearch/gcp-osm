#!/usr/bin/env python3

import os
from typing import Callable

from gcposm import utils
from gcposm import model

from gcposm.gcp_url_parser import GCPURLParser, GeoLocationResolver, GeoLocationDecoder

import argument_parser
import qr_code_extractor


def load_your_gcp_list(file):
    gcp_list = []
    if os.path.exists(file):
        with open(file, 'r') as infile:
            for line in infile:
                gcp_list.append(line.split("*")[0].split(";"))

    return gcp_list

def init_gcp_url_parser(lookup: Callable[[str], model.GeoLocation]):
    geo_location_resolver = GeoLocationResolver(lookup)
    geo_location_decoder = GeoLocationDecoder()

    return GCPURLParser(geo_location_resolver, geo_location_decoder)

def main(filename):
    gcp_lookup_table = load_your_gcp_list("my_gcp_list.txt")

    def lookup_geo_location_in_lookup_table(id: str):
        for entry in gcp_lookup_table:
            [entry_id, latitude, longitude, altitude_in_meters] = entry
            if id != entry_id:
                continue

            return model.GeoLocation(latitude, longitude, altitude_in_meters)

        raise Exception("Id not found in lookup table: " + id)

    gcp_url_parser = init_gcp_url_parser(lookup_geo_location_in_lookup_table)

    print("Hello, starting GCP-OSM...")
    print("")

    # now working time
    if os.path.isdir(args.file):
        print("loading in all files in folder:", filename)
        processing_files = utils.get_all_files(filename)

    elif os.path.isfile(args.file):
        print("loading in this file:", filename)
        processing_files = utils.get_one_file(filename)

    else:
        print("neither file nor folder. ending programm.")
        return

    for file in processing_files:
        found_qr_codes = qr_code_extractor.get_qr_data(file, debug_show_image=args.is_debug)
        print(str(found_qr_codes) + " -> ", end='')

        [gcp_url, upper_left_position_marker_pixel_coordinates] = found_qr_codes
        print(gcp_url_parser.parse(gcp_url))

    print("")
    print("GCP-OSM is finished, Good Bye!")


if __name__ == '__main__':
    args = argument_parser.parse_arguments()

    main(args.file)
