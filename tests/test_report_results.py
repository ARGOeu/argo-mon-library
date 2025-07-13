import unittest
from httmock import HTTMock
from pymod import ArgoMonitoringService, Reports, Report, ReportResults
from datetime import datetime
import json
from .monmocks import ReportMocks

class TestReportResults(unittest.TestCase):
    def setUp(self):
        self.mon = ArgoMonitoringService("localhost", "s3cr3t")
        self.ReportMocks = ReportMocks()

    def _validateReportResultsData(self, results: ReportResults):
        self.assertEqual(results.name, "TENANT01")
        self.assertEqual(results.type, "PROJECT")
        self.assertIsNotNone(results.results)
        self.assertEqual(len(results.results), 1)
        self.assertEqual(str(results.results[0].date), "2025-06-01 00:00:00")
        self.assertEqual(results.results[0].availability, "100")
        self.assertEqual(results.results[0].reliability, "100")
        self.assertIsNotNone(results.groups)
        self.assertEqual(len(results.groups), 1)
        self.assertEqual(results.groups[0].name, "ARGO_MON")
        self.assertEqual(results.groups[0].type, "SERVICEGROUPS")
        self.assertIsNotNone(results.groups[0].results)
        self.assertEqual(len(results.groups[0].results), 1)
        self.assertEqual(str(results.groups[0].results[0].date), "2025-06-01 00:00:00")
        self.assertEqual(results.groups[0].results[0].availability, "100")
        self.assertEqual(results.groups[0].results[0].reliability, "100")
        self.assertEqual(results.groups[0].results[0].unknown, "0")
        self.assertEqual(results.groups[0].results[0].uptime, "1")
        self.assertEqual(results.groups[0].results[0].downtime, "0")

    def testGetReportResults(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.ReportMocks.get_report_results_mock
        ):
            results = self.mon.reports[0].results
            self.assertIsNotNone(results)
            self._validateReportResultsData(results)

    def testGetReportResultsJSON(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.ReportMocks.get_report_results_mock
        ):
            results = self.mon.reports[0].results
            self.assertIsNotNone(results)
            jsons = str(results)
            try:
                j = json.loads(jsons)
            except:
                pass
            self.assertIsNotNone(j)
            self.assertTrue('"name": "TENANT01"' in jsons)
            self.assertTrue('"type": "PROJECT"' in jsons)
            self.assertTrue('"date": "2025-06-01"' in jsons)
            self.assertTrue('"availability": "100"' in jsons)
            self.assertTrue('"reliability": "100"' in jsons)
            self.assertTrue('"unknown": "0"' in jsons)
            self.assertTrue('"uptime": "1"' in jsons)
            self.assertTrue('"downtime": "0"' in jsons)
