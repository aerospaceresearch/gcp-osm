from dataclasses import dataclass

# see https://docs.python.org/3/library/dataclasses.html
# @dataclass automatically generates 
#   - a constructor containing all class attributes as parameters
#   - an implementation of __repr__() which makes the class printable,
#       i.e. "GeoLocation(longitude=1, latitude=2, altitude=0.3)" instead of just
#       "<__main__.GeoLocation object at 0x7f65a53565b0>"
@dataclass
class GeoLocation:
    longitude: float
    latitude: float
    altitude: float

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
    centerGeoLocation: GeoLocation
    mapObject: MapObjectId
