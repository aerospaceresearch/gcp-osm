from typing import Callable
from urllib.parse import urlparse

from .model import MapObjectId
from .model import OSMAreaId
from .model import OSMNodeId
from .model import OSMRelationId
from .model import OSMWayId
from .model import OSMGroundControlPointId

from .model import ClassicGroundControlPoint
from .model import OSMGroundControlPoint

from .model import GeoLocation

from .osm_shortlink import shortlinkToGeoLoc

from .utils import decode_base64_id


class GeoLocationResolver:
    def __init__(self, lookup: Callable[[str], GeoLocation]):
        """Keyword arguments:

        lookup -- callable which accepts one parameter local_id: str and returns a GeoLocation instance"""
        self.local_lookup = lookup

    def resolve_from_local_lookup_table(self, id: str) -> GeoLocation:
        """resolves the center gelocation of an OSM ground control point identified by a local lookup table id.
    
        Keyword arguments:
    
        id -- id to be searched for within the local lookup table"""
        return self.local_lookup(id)

    def resolve(self, map_object: MapObjectId) -> GeoLocation:
        """resolves the center gelocation of an OSM ground control point.
    
        Keyword arguments:
    
        map_object -- id of the map object associated to the ground control point"""
        raise NotImplementedError()

    def resolve_position_markers_of_qr_code(self, map_object: MapObjectId) -> [GeoLocation, GeoLocation, GeoLocation]:
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

    def decode(self, base64: str) -> GeoLocation:
        """Decodes a base64 string into a geo location (lon, lat, alt).

        Keyword arguments:
        base64 -- string to decode"""
    
        return shortlinkToGeoLoc(base64)


class GCPURLParser:
    def __init__(self, geo_location_resolver: GeoLocationResolver, geo_location_decoder: GeoLocationDecoder):
        """Keyword arguments:
        
        geo_location_resolver -- instance of GeoLocationResolver
        geo_location_decoder -- instance of GeoLocationDecoder"""
        self.geo_location_resolver = geo_location_resolver
        self.geo_location_decoder = geo_location_decoder
    
    def parse(self, ground_control_point_url: str) -> GeoLocation:
        """Parses and resolves geo location information for a given ground control point url.

        Keyword arguments:

        ground_control_point_url -- gcp:// in one of the accpepted forms:
            gcp://l/[local id]
            gcp://osm/n/[base64 osm node id]
            gcp://osm/r/[base64 osm relation id]
            gcp://osm/w/[base64 osm way id]
            gcp://osm/a/[base64 osm area id]
            gcp://osm/gcp/[base64 ground control point id]"""

        parsed_url = urlparse(ground_control_point_url)
        if parsed_url.scheme and not parsed_url.scheme in ['gcp', 'https']:
            raise Error("Unsupported URL scheme: " + parsed_url.scheme)

        assembled_path = parsed_url.path
        if parsed_url.netloc:
            # when the url schema is given the first part behind //: is treated as netloc / hostname
            # since gcp osm urls do not have a host we treat is as being part of the path
            assembled_path = parsed_url.netloc + assembled_path

        id_part = assembled_path.split('/')[-1]
        map_object = None

        if assembled_path.startswith('l/') or assembled_path.startswith('osm.to/l/'):
            # handle local id
            geo_location = self.geo_location_resolver.resolve_from_local_lookup_table(id_part)
            return ClassicGroundControlPoint(geo_location, map_object)

        if assembled_path.startswith('osm/g/') or assembled_path.startswith('osm.to/g/'):
            # handle encoded geo location
            geo_location = self.geo_location_decoder.decode(id_part)
            return ClassicGroundControlPoint(geo_location, map_object)


        # handle osm ground control points associated to OSM objects
        decoded_id = decode_base64_id(id_part)

        if assembled_path.startswith("osm/gcp/") or assembled_path.startswith('osm.to/gcp/'):
            map_object = OSMGroundControlPointId(decoded_id)

        if assembled_path.startswith("osm/a/") or assembled_path.startswith('osm.to/a/'):
            map_object = OSMAreaId(decoded_id)

        if assembled_path.startswith("osm/n/") or assembled_path.startswith('osm.to/n/'):
            map_object = OSMNodeId(decoded_id)

        if assembled_path.startswith("osm/r/") or assembled_path.startswith('osm.to/r/'):
            map_object = OSMRelationId(decoded_id)

        if assembled_path.startswith("osm/w/") or assembled_path.startswith('osm.to/w/'):
            map_object = OSMWayId(decoded_id)

        if map_object is None:
            raise Error("unsupported path format: " + path)

        geo_location = self.geo_location_resolver.resolve(map_object)
        position_marker_geo_locations = self.geo_location_resolver.resolve_position_markers_of_qr_code(map_object)
        return OSMGroundControlPoint(geo_location, map_object, *position_marker_geo_locations)


