from unittest import TestCase
from unittest.mock import MagicMock

from gcposm.model import GeoLocation

from gcposm.model import OSMAreaId
from gcposm.model import OSMRelationId
from gcposm.model import OSMNodeId
from gcposm.model import OSMWayId
from gcposm.model import OSMGroundControlPointId

from gcposm.model import ClassicGroundControlPoint
from gcposm.model import OSMGroundControlPoint

from gcposm.utils import encode_id_as_base64

from gcposm.gcp_url_parser import GCPURLParser

class GCPURLParser_Generic_Test(TestCase):
    def setUp(self):
        self.geo_location_resolver_stub = MagicMock()
        self.geo_location_decoder_stub = MagicMock()

        self.gcp_url_parser = GCPURLParser(self.geo_location_resolver_stub, self.geo_location_decoder_stub)

    def test_reports_error_on_invalid_schema(self):
        with self.assertRaises(Exception, msg="did not raise an exception for foreign schemas"):
            self.gcp_url_parser.parse("ftp://")

    def test_succeeds_with_missing_schema(self): 
        result = self.gcp_url_parser.parse("l/42")

        self.assertIsInstance(result, ClassicGroundControlPoint, "failed to parse gcp url without schema")

class GCPURLParser_LocalId_Test(TestCase):
    def setUp(self):
        self.geo_location_decoder_stub = MagicMock()

    def test_returns_ground_control_point_at_geo_location_specified_by_lookup_table(self):
        parameters = [
            { 'url': 'gcp://l/42' },
            { 'url': 'https://osm.to/l/42' } ]

        expected_geo_location = GeoLocation(longitude=12, latitude=34, altitude=56)
        expected_ground_control_point = ClassicGroundControlPoint(expected_geo_location, map_object=None)

        geo_location_resolver_spy = MagicMock()
        geo_location_resolver_spy.resolve_from_local_lookup_table = MagicMock(return_value=expected_geo_location)

        for p in parameters:
            gcp_url_parser = GCPURLParser(geo_location_resolver_spy, self.geo_location_decoder_stub)

            result = gcp_url_parser.parse(p['url'])

            geo_location_resolver_spy.resolve_from_local_lookup_table.assert_called_with('42')
            self.assertEqual(expected_ground_control_point, result, "did not return the correct GeoLocation")


class GCPURLParser_EncodedGeoLocation_Test(TestCase):
    def setUp(self):
        self.geo_location_resolver_stub = MagicMock()
        self.geo_location_decoder_spy = MagicMock()

    def test_returns_ground_control_point_at_geo_location_specified_by_lookup_table(self):
        parameters = [
            { 'url': 'gcp://osm/g/specialBase64EncodedGeoLocation' },
            { 'url': 'https://osm.to/g/specialBase64EncodedGeoLocation' } ]

        expected_geo_location = GeoLocation(longitude=12, latitude=34, altitude=56)
        expected_ground_control_point = ClassicGroundControlPoint(expected_geo_location, map_object=None)

        self.geo_location_decoder_spy.decode = MagicMock(return_value=expected_geo_location)

        for p in parameters:
            gcp_url_parser = GCPURLParser(self.geo_location_resolver_stub, self.geo_location_decoder_spy)

            result = gcp_url_parser.parse(p['url'])

            self.geo_location_decoder_spy.decode.assert_called_with('specialBase64EncodedGeoLocation')
            self.assertEqual(expected_ground_control_point, result, "did not return the correct GeoLocation")


class GCPURLParser_OSMGroundControlPoint_Test(TestCase):
    def setUp(self):
        self.geo_location_decoder_stub = MagicMock()
        self.geo_location_resolver_spy = MagicMock()

        self.expected_geo_location = GeoLocation(longitude=12, latitude=34, altitude=56)
        self.expected_geo_locations_of_position_markers = [
            GeoLocation(longitude=11, latitude=11, altitude=11), # upper left position marker
            GeoLocation(longitude=22, latitude=22, altitude=22), # upper right position marker
            GeoLocation(longitude=33, latitude=33, altitude=33)  # lower left position marker
        ]

        self.geo_location_resolver_spy.resolve = MagicMock(return_value=self.expected_geo_location)
        self.geo_location_resolver_spy.resolve_position_markers_of_qr_code = MagicMock(return_value=self.expected_geo_locations_of_position_markers)

    def test_returns_ground_control_point_specified_by_OSMObject(self):
        parameters = [
            {   'map_object': OSMNodeId('42'),
                'url': 'gcp://osm/n/' + encode_id_as_base64(42),

                'expected_ground_control_point':
                    OSMGroundControlPoint(
                        self.expected_geo_location,
                        OSMNodeId('42'),
                        *self.expected_geo_locations_of_position_markers )
            },

            {   'map_object': OSMNodeId('42'),
                'url': 'https://osm.to/n/' + encode_id_as_base64(42),

                'expected_ground_control_point':
                    OSMGroundControlPoint(
                        self.expected_geo_location,
                        OSMNodeId('42'),
                        *self.expected_geo_locations_of_position_markers )
            },

            {   'map_object': OSMRelationId('42'),
                'url': 'gcp://osm/r/' + encode_id_as_base64(42),

                'expected_ground_control_point':
                    OSMGroundControlPoint(
                        self.expected_geo_location,
                        OSMRelationId('42'),
                        *self.expected_geo_locations_of_position_markers )
            },

            {   'map_object': OSMRelationId('42'),
                'url': 'https://osm.to/r/' + encode_id_as_base64(42),

                'expected_ground_control_point':
                    OSMGroundControlPoint(
                        self.expected_geo_location,
                        OSMRelationId('42'),
                        *self.expected_geo_locations_of_position_markers )
            },

            {   'map_object': OSMWayId('42'),
                'url': 'gcp://osm/w/' + encode_id_as_base64(42),

                'expected_ground_control_point':
                    OSMGroundControlPoint(
                        self.expected_geo_location,
                        OSMWayId('42'),
                        *self.expected_geo_locations_of_position_markers )
            },

            {   'map_object': OSMWayId('42'),
                'url': 'https://osm.to/w/' + encode_id_as_base64(42),

                'expected_ground_control_point':
                    OSMGroundControlPoint(
                        self.expected_geo_location,
                        OSMWayId('42'),
                        *self.expected_geo_locations_of_position_markers )
            },

            {   'map_object': OSMAreaId('42'),
                'url': 'gcp://osm/a/' + encode_id_as_base64(42),

                'expected_ground_control_point':
                    OSMGroundControlPoint(
                        self.expected_geo_location,
                        OSMAreaId('42'),
                        *self.expected_geo_locations_of_position_markers )
            },

            {   'map_object': OSMAreaId('42'),
                'url': 'https://osm.to/a/' + encode_id_as_base64(42),

                'expected_ground_control_point':
                    OSMGroundControlPoint(
                        self.expected_geo_location,
                        OSMAreaId('42'),
                        *self.expected_geo_locations_of_position_markers )
            },

            {   'map_object': OSMGroundControlPointId('42'),
                'url': 'gcp://osm/gcp/' + encode_id_as_base64(42),

                'expected_ground_control_point':
                    OSMGroundControlPoint(
                        self.expected_geo_location,
                        OSMGroundControlPointId('42'),
                        *self.expected_geo_locations_of_position_markers )
            },

            {   'map_object': OSMGroundControlPointId('42'),
                'url': 'https://osm.to/gcp/' + encode_id_as_base64(42),

                'expected_ground_control_point':
                    OSMGroundControlPoint(
                        self.expected_geo_location,
                        OSMGroundControlPointId('42'),
                        *self.expected_geo_locations_of_position_markers )
            } ]


        for p in parameters:
            gcp_url_parser = GCPURLParser(self.geo_location_resolver_spy, self.geo_location_decoder_stub)
            result = gcp_url_parser.parse(p['url'])

            self.geo_location_resolver_spy.resolve.assert_called_with(p['map_object'])
            self.geo_location_resolver_spy.resolve_position_markers_of_qr_code.assert_called_with(p['map_object'])
            self.assertEqual(p['expected_ground_control_point'], result, "did not return the correct GeoLocation")

