from io import TextIOWrapper
from pyproj import Transformer
from typing import Iterable

from .model import GeoLocation

def write_gcp_list_file(file_name, tuples: Iterable[tuple[str, GeoLocation, int, int]], encoding='utf-8', errors=None, newline=None):
    """Writes tuples of geo-locations and pixel coordinates into a gcp_list.txt file. Before writing the geo-locations
    a projection is applied:
        +proj=utm +zone=10 +ellps=WGS84 +datum=WGS84 +units=m +no_defs
        ( see https://pyproj4.github.io/pyproj/stable/api/proj.html#pyproj-proj )

    See GCP file format: https://docs.opendronemap.org/gcp/

    Keyword arguments:
        file_name -- (path) and name of the target file
        tuples -- iterable (i.e. list) of tuples
            (
                image filename: str, 
                geo location: GeoLocation, 
                image x coordinate: int, 
                image y coordinate: int
            )
        encoding -- see https://docs.python.org/3/library/functions.html#open
        errors -- see https://docs.python.org/3/library/functions.html#open
        newline -- see https://docs.python.org/3/library/functions.html#open"""

    file = open(file_name, mode='w', encoding=encoding, errors=errors, newline=newline)

    # prepare projection
    proj_string = "+proj=utm +zone=10 +ellps=WGS84 +datum=WGS84 +units=m +no_defs\n"
    transformer = Transformer.from_crs(crs_from="+proj=latlon", crs_to="+proj=utm +zone=10 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

    # write information about projection that was applied to the geo coordinates
    file.write(proj_string)

    for (image_file_name, geo_location, image_x, image_y) in tuples:
        [ (geo_x, geo_y, geo_z) ] = transformer.itransform( [(geo_location.latitude, geo_location.longitude, geo_location.altitude_in_meters)] )

        file.write(
            " ".join(
                map(lambda v: str(v),
                    [ geo_x, geo_y, geo_z, image_x, image_y, image_file_name ] )
            ) + "\n" )

    file.close()

