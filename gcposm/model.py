from dataclasses import dataclass

# see https://docs.python.org/3/library/dataclasses.html
# @dataclass automatically generates 
#   - a constructor containing all class attributes as parameters
#   - an implementation of __repr__() which makes the class printable,
#       i.e. "GeoLocation(latitude=1, longitude=2, altitude_in_meters=0.3)" instead of just
#       "<__main__.GeoLocation object at 0x7f65a53565b0>"
@dataclass
class GeoLocation:
    latitude: float
    longitude: float
    altitude_in_meters: float

@dataclass
class MapObjectId:
    id: str

@dataclass
class OSMAreaId(MapObjectId):
    None

@dataclass
class OSMNodeId(MapObjectId):
    None

@dataclass
class OSMRelationId(MapObjectId):
    None

@dataclass
class OSMWayId(MapObjectId):
    None

@dataclass
class OSMGroundControlPointId(MapObjectId):
    None

@dataclass
class GroundControlPoint:
    center_geo_location: GeoLocation
    map_object: MapObjectId

@dataclass
class ClassicGroundControlPoint(GroundControlPoint):
    None

@dataclass
class OSMGroundControlPoint(GroundControlPoint):
    upper_left_position_marker: GeoLocation
    upper_right_position_marker: GeoLocation
    lower_left_position_marker: GeoLocation

