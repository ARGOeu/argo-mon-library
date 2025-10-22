import json
import unittest

from httmock import HTTMock

from pymod import (ArgoMonitoringService, EndpointIssueMetricDetails,
                   EndpointIssues, MetricIssues)

from .monmocks import IssueMocks, ReportMocks


class TestIssues(unittest.TestCase):
    def setUp(self):
        self.mon = ArgoMonitoringService("localhost", "s3cr3t")
        self.ReportMocks = ReportMocks()
        self.IssueMocks = IssueMocks()

    def _validateEndpointIssuesData(self, issues: EndpointIssues):
        self.assertEqual(len(list(issues)), 2)

        self.assertEqual(str(issues[0].timestamp), "2025-10-05T00:00:00Z")
        self.assertEqual(str(issues[0].endpoint_group), "ARGO_MON")
        self.assertEqual(str(issues[0].service), "www.example.com-example.api")
        self.assertEqual(str(issues[0].endpoint), "www.example.com_01-234567-890ABC")
        self.assertEqual(str(issues[0].status), "CRITICAL")
        self.assertEqual(str(issues[0].id), "01-234567-890ABC")
        self.assertEqual(str(issues[0].url), "https://www.example.com/api")
        self.assertEqual(str(issues[0].groupname), "ARGO_MON")

        self.assertEqual(str(issues[1].timestamp), "2025-10-05T00:00:00Z")
        self.assertEqual(str(issues[1].endpoint_group), "ARGO_MON")
        self.assertEqual(str(issues[1].service), "www.example.com-web")
        self.assertEqual(str(issues[1].endpoint), "www.example.com_ABCD")
        self.assertEqual(str(issues[1].status), "WARNING")
        self.assertEqual(str(issues[1].id), "ABCD")
        self.assertEqual(str(issues[1].url), "https://www.example.com")
        self.assertIsNone(issues[1].groupname)

    def _validateMetricIssuesData(self, issues: MetricIssues):
        self.assertEqual(len(list(issues)), 2)

        self.assertEqual(str(issues[0].service), "www.example.com-example.web")
        self.assertEqual(str(issues[0].hostname), "www.example.com_01-234567-890ABC")
        self.assertEqual(str(issues[0].metric), "generic.certificate.validity")
        self.assertEqual(str(issues[0].status), "WARNING")
        self.assertEqual(str(issues[0].id), "01-234567-890ABC")
        self.assertEqual(str(issues[0].url), "https://www.example.com")

        self.assertEqual(str(issues[1].service), "www.example.com-example.api")
        self.assertEqual(str(issues[1].hostname), "api.example.com_EFGH")
        self.assertEqual(str(issues[1].metric), "generic.http.connect")
        self.assertEqual(str(issues[1].status), "CRITICAL")
        self.assertEqual(str(issues[1].id), "EFGH")
        self.assertEqual(str(issues[1].url), "https://api.example.com")

    def _validateEndpointIssueMetricDetailsData(self, issue_details: EndpointIssueMetricDetails):
        self.assertEqual(len(list(issue_details)), 1)

        for i in [0, "2025-10-05T02:23:16Z"]:
            self.assertEqual(str(issue_details[i].timestamp), "2025-10-05T02:23:16Z")
            self.assertEqual(str(issue_details[i].value), "CRITICAL")
            self.assertEqual(str(issue_details[i].summary), "Cannot connect to www.example.com on port 443")
            self.assertEqual(str(issue_details[i].message), "''")

    def testListEndpointIssues(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.IssueMocks.list_testreport_endpoint_issues_mock
        ):
            issues = self.mon.reports[0].issues.by_endpoint()
            self.assertIsNotNone(issues)
            self._validateEndpointIssuesData(issues)

    def testListEndpointIssuesFilter(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.IssueMocks.list_testreport_endpoint_issues_mock
        ):
            issues = self.mon.reports[0].issues.by_endpoint("CRITICAL")
            self.assertIsNotNone(issues)
            self.assertEqual(len(list(issues)), 1)

    def testListEndpointIssuesJSON(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.IssueMocks.list_testreport_endpoint_issues_mock
        ):
            issues = self.mon.reports[0].issues.by_endpoint()
            self.assertIsNotNone(issues)
            jsons = str(issues[0])
            try:
                j = json.loads(jsons)
            except json.decoder.JSONDecodeError:
                self.fail("Invalid JSON representation")
            self.assertIsNotNone(j)
            self.assertTrue('"timestamp": "2025-10-05T00:00:00Z"' in jsons)
            self.assertTrue('"endpoint_group": "ARGO_MON"' in jsons)
            self.assertTrue('"service": "www.example.com-example.api"' in jsons)
            self.assertTrue('"endpoint": "www.example.com_01-234567-890ABC"' in jsons)
            self.assertTrue('"status": "CRITICAL"' in jsons)
            self.assertTrue('"id": "01-234567-890ABC"' in jsons)
            self.assertTrue('"url": "https://www.example.com/api"' in jsons)
            self.assertTrue('"groupname": "ARGO_MON"' in jsons)

    def testListMetricIssues(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.IssueMocks.list_testreport_metric_issues_mock
        ):
            issues = self.mon.reports[0].issues.by_metric("ARGO_MON")
            self.assertIsNotNone(issues)
            self._validateMetricIssuesData(issues)

    def testListMetricIssuesFilter(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.IssueMocks.list_testreport_metric_issues_mock
        ):
            issues = self.mon.reports[0].issues.by_metric("ARGO_MON", "CRITICAL")
            self.assertIsNotNone(issues)
            self.assertEqual(len(list(issues)), 1)

    def testListMetricIssuesJSON(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.IssueMocks.list_testreport_metric_issues_mock
        ):
            issues = self.mon.reports[0].issues.by_metric("ARGO_MON")
            self.assertIsNotNone(issues)
            jsons = str(issues[0])
            try:
                j = json.loads(jsons)
            except json.decoder.JSONDecodeError:
                self.fail("Invalid JSON representation")
            self.assertIsNotNone(j)
            self.assertTrue('"service": "www.example.com-example.web"' in jsons)
            self.assertTrue('"hostname": "www.example.com_01-234567-890ABC"' in jsons)
            self.assertTrue('"status": "WARNING"' in jsons)
            self.assertTrue('"metric": "generic.certificate.validity"' in jsons)
            self.assertTrue('"id": "01-234567-890ABC"' in jsons)
            self.assertTrue('"url": "https://www.example.com"' in jsons)

    def testListEndpointIssueMetricDetails(self):
        with HTTMock(
            self.ReportMocks.list_reports_mock,
            self.IssueMocks.list_testreport_endpoint_issues_mock,
            self.IssueMocks.get_endpoint_metric_result_mock,
            self.IssueMocks.get_endpoint_metric_result_metric_mock
        ):
            issues = self.mon.period("2025-10-05T00:00:00Z").reports[0].issues.by_endpoint()
            self.assertIsNotNone(issues)
            self._validateEndpointIssuesData(issues)
            self.assertEqual(len(list(issues)), 2)
            self.assertEqual(len(list(issues[1].metrics)), 1)
            self.assertEqual(len(list(issues[1].metrics[0].details)), 1)

            for i in [0, "generic.http.connect"]:
                self._validateEndpointIssueMetricDetailsData(issues[1].metrics[0].details)
                self.assertEqual(issues[1].metrics[i].service, "www.example.com-web")
