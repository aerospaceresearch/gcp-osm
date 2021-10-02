import os
from typing import Callable

from .model import MapObjectId
from .model import OSMAreaId
from .model import OSMNodeId
from .model import OSMRelationId
from .model import OSMWayId
from .model import OSMGroundControlPointId

from .model import GeoLocation

class GeoLocationResolver:
    def __init__(self, lookup: Callable[[str], GeoLocation]):
        """Keyword arguments:

        lookup -- callable which accepts one parameter local_id: str and returns a GeoLocation instance"""
        self.local_lookup = lookup

    def resolve_from_local_lookup_table(id: str) -> GeoLocation:
        """resolves the center gelocation of an OSM ground control point identified by a local lookup table id.
    
        Keyword arguments:
    
        id -- id to be searched for within the local lookup table"""
        return self.local_lookup(id)

    def resolve(map_object: MapObjectId) -> GeoLocation:
        """resolves the center gelocation of an OSM ground control point.
    
        Keyword arguments:
    
        map_object -- id of the map object associated to the ground control point"""
        raise NotImplementedError()

    def resolve_position_markers_of_qr_code(map_object: MapObjectId) ->  [GeoLocation, GeoLocation, GeoLocation]:
        """resolves the gelocations of an OSM ground control point.
    
        Keyword arguments:
    
        map_object -- id of the map object associated to the ground control point
    
        Returns:
            [   upper_left_position_mark: GeoLocation,
                upper_right_position_mark: GeoLocation, 
                lower_left_position_mark: GeoLocation ]"""
        raise NotImplementedError()

class GeoLocationDecoder:
    def __init__(self):
        None

    def decode(base64: str) -> GeoLocation:
        """Decodes a base64 string into a geo location (lon, lat, alt).

        Keyword arguments:
        base64 -- string to decode"""
        raise NotImplementedError()


class GCPURLParser:
    def __init__(self, geo_location_resolver: GeoLocationResolver):
        """Keyword arguments:
        
        geo_location_resolver -- instance of GeoLocationResolver"""
        self.geo_location_resolver = geo_location_resolver
    
    def parse(ground_control_point_url: str) -> GeoLocation:
        """Parses and resolves geo location information for a given ground control point url.

        Keyword arguments:

        ground_control_point_url -- gcp:// in one of the accpepted forms:
            gcp://l/[local id]
            gcp://osm/n/[base64 osm node id]
            gcp://osm/r/[base64 osm relation id]
            gcp://osm/w/[base64 osm way id]
            gcp://osm/a/[base64 osm area id]
            gcp://osm/gcp/[base64 ground control point id]"""
        raise NotImplementedError()


def get_all_files(filename):
    processing_files = []
    for root, dirs, files in os.walk(filename):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath):
                #print("file", filepath)
                processing_files.append(filepath)

    return processing_files


def get_one_file(filename):
    return [filename]

if __name__ == '__main__':
    '''nothn'''
