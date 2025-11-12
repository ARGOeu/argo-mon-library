import json
import unittest

from httmock import HTTMock

from pymod import ArgoMonitoringService, FlappingType

from .monmocks import ReportMocks, TrendMocks


class TestTrends(unittest.TestCase):
    def setUp(self):
        self.mon = ArgoMonitoringService("localhost", "s3cr3t")
        self.ReportMocks = ReportMocks()
        self.TrendMocks = TrendMocks()

    def _testGetFlappingTypes(self, typ: FlappingType, flaps):
        self.assertEqual(len(list(flaps)), 2)
        self.assertEqual(flaps[0].endpoint_group, "ARGO_MON")
        self.assertEqual(flaps[0].flapping, 5)
        self.assertEqual(flaps[1].endpoint_group, "ARGO_MON2")
        self.assertEqual(flaps[1].flapping, 1)
        if (typ >= FlappingType.SERVICES):
            self.assertEqual(flaps[0].service, "www.example.com-web")
            self.assertEqual(flaps[1].service, "www.example.com-api")
        if (typ >= FlappingType.ENDPOINTS):
            self.assertEqual(flaps[0].endpoint, "https://www.example.com")
            self.assertEqual(flaps[1].endpoint, "https://api.example.com")
        if (typ >= FlappingType.METRICS):
            self.assertEqual(flaps[0].metric, "generic.http.connect")
            self.assertEqual(flaps[1].metric, "generic.http.connect")

    def _testGetFlappingTypesJSON(self, typ: FlappingType, flaps):
        self.assertIsNotNone(flaps)
        jsons = str(flaps[0])
        try:
            j = json.loads(jsons)
        except json.decoder.JSONDecodeError:
            self.fail("Invalid JSON representation")
        self.assertIsNotNone(j)
        self.assertTrue('"endpoint_group": "ARGO_MON"' in jsons)

        if (typ >= FlappingType.SERVICES):
            self.assertTrue('"service": "www.example.com-web"' in jsons)
        if (typ >= FlappingType.ENDPOINTS):
            self.assertTrue('"endpoint": "https://www.example.com"' in jsons)
        if (typ >= FlappingType.METRICS):
            self.assertTrue('"metric": "generic.http.connect"' in jsons)

    def testGetFlappingGroups(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.TrendMocks.get_flapping_groups_mock
        ):
            typ = FlappingType.GROUPS
            self._testGetFlappingTypes(typ, self.mon.reports[0].trends.flapping(typ))

    def testGetFlappingGroupsJSON(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.TrendMocks.get_flapping_groups_mock
        ):
            typ = FlappingType.GROUPS
            self._testGetFlappingTypesJSON(typ, self.mon.reports[0].trends.flapping(typ))

    def testGetFlappingServices(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.TrendMocks.get_flapping_services_mock
        ):
            typ = FlappingType.SERVICES
            self._testGetFlappingTypes(typ, self.mon.reports[0].trends.flapping(typ))

    def testGetFlappingServicesJSON(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.TrendMocks.get_flapping_services_mock
        ):
            typ = FlappingType.SERVICES
            self._testGetFlappingTypesJSON(typ, self.mon.reports[0].trends.flapping(typ))

    def testGetFlappingEndpoints(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.TrendMocks.get_flapping_endpoints_mock
        ):
            typ = FlappingType.ENDPOINTS
            self._testGetFlappingTypes(typ, self.mon.reports[0].trends.flapping(typ))

    def testGetFlappingEndpointsJSON(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.TrendMocks.get_flapping_endpoints_mock
        ):
            typ = FlappingType.ENDPOINTS
            self._testGetFlappingTypesJSON(typ, self.mon.reports[0].trends.flapping(typ))

    def testGetFlappingMetrics(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.TrendMocks.get_flapping_metrics_mock
        ):
            typ = FlappingType.METRICS
            self._testGetFlappingTypes(typ, self.mon.reports[0].trends.flapping(typ))

    def testGetFlappingMetricsJSON(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.TrendMocks.get_flapping_metrics_mock
        ):
            typ = FlappingType.METRICS
            self._testGetFlappingTypesJSON(typ, self.mon.reports[0].trends.flapping(typ))

    def testgetflappingmetricTags(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.TrendMocks.get_flapping_metric_tags_mock
        ):
            flaps = self.mon.reports[0].trends.flapping(FlappingType.METRIC_TAGS)
            self.assertEqual(len(list(flaps)), 2)
            self.assertEqual(flaps[0].tag, "http")
            self.assertEqual(flaps[1].tag, "network")
            for flap in flaps:
                self._testGetFlappingTypes(FlappingType.METRICS, flap.metrics)

    def testgetflappingmetricTagsJSON(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.TrendMocks.get_flapping_metric_tags_mock
        ):
            flaps = self.mon.reports[0].trends.flapping(FlappingType.METRIC_TAGS)
            self.assertIsNotNone(flaps)
            jsons = str(flaps[0])
            try:
                j = json.loads(jsons)
            except json.decoder.JSONDecodeError:
                self.fail("Invalid JSON representation")
            self.assertIsNotNone(j)
            self.assertTrue('"tag": "http"' in jsons)

            for flap in flaps:
                self._testGetFlappingTypesJSON(FlappingType.METRICS, flap.metrics)
