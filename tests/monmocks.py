from httmock import urlmatch, response
import json

class ReportMocks(object):
    LIST_REPORTS_RESPONSE = """{"status": {"message": "Success", "code": "200"}, "data": [{"id": "efd48668-e24a-4a2c-a53f-3f388664b691", "tenant": "TENANT01", "disabled": false, "info": {"name": "REPORT01", "description": "REPORT01 A/R report", "created": "2025-03-06 12:53:27", "updated": "2025-03-06 12:53:27"}, "computations": {"ar": true, "status": true, "trends": ["flapping", "status", "tags"]}, "thresholds": {"availability": 80, "reliability": 90, "uptime": 0.8, "unknown": 0.1, "downtime": 0.1}, "topology_schema": {"group": {"type": "PROJECT", "group": {"type": "SERVICEGROUPS"}}}, "profiles": [{"id": "5c3218ea-3f67-4d4c-b3ce-f650b8ed8e68", "name": "ARGO_MON", "type": "metric"}, {"id": "ede2a9f7-e754-47fa-8e76-449e3925fbd4", "name": "core", "type": "aggregation"}, {"id": "be1fbf37-77f3-4a9e-b268-a6a9a0830ef5", "name": "ops", "type": "operations"}], "filter_tags": [{"name": "FT1", "value": "val", "context": "cntx"}]}]}"""

    LIST_REPORTS_RESPONSE2 = """{"status": {"message": "Success", "code": "200"}, "data": [{"id": "efd48668-e24a-4a2c-a53f-3f388664b692", "tenant": "TENANT02", "disabled": false, "info": {"name": "REPORT02", "description": "REPORT02 A/R report", "created": "2025-03-06 12:53:27", "updated": "2025-03-06 12:53:27"}, "computations": {"ar": true, "status": true, "trends": ["flapping", "status", "tags"]}, "thresholds": {"availability": 80, "reliability": 90, "uptime": 0.8, "unknown": 0.1, "downtime": 0.1}, "topology_schema": {"group": {"type": "PROJECT", "group": {"type": "SERVICEGROUPS"}}}, "profiles": [{"id": "5c3218ea-3f67-4d4c-b3ce-f650b8ed8e68", "name": "ARGO_MON", "type": "metric"}, {"id": "ede2a9f7-e754-47fa-8e76-449e3925fbd4", "name": "core", "type": "aggregation"}, {"id": "be1fbf37-77f3-4a9e-b268-a6a9a0830ef5", "name": "ops", "type": "operations"}], "filter_tags": [{"name": "FT1", "value": "val", "context": "cntx"}]}]}"""

    GET_REPORT_RESPONSE = LIST_REPORTS_RESPONSE

    GET_REPORT_STATUS_RESPONSE = """{"groups": [{"name": "ARGO_MON", "type": "SERVICEGROUPS", "statuses": [{"timestamp": "2025-06-01T00:00:00Z", "value": "OK"}, {"timestamp": "2025-06-01T23:59:59Z", "value": "OK"}], "endpoints": [{"hostname": "www.example.com", "service": "www.example.com-example.api", "info": {"ID": "EXAMPLE01", "URL": "https://www.example.com/api/action?foo=bar"}, "statuses": [{"timestamp": "2025-06-01T00:00:00Z", "value": "OK"}, {"timestamp": "2025-06-01T23:59:59Z", "value": "OK"}]}]}]}"""

    GET_REPORT_RESULTS_RESPONSE = """{"results": [{"name": "TENANT01", "type": "PROJECT", "results": [{"date": "2025-06-01", "availability": "100", "reliability": "100"}], "groups": [{"name": "ARGO_MON", "type": "SERVICEGROUPS", "results": [{"date": "2025-06-01", "availability": "100", "reliability": "100", "unknown": "0", "uptime": "1", "downtime": "0"}]}]}]}"""

    list_reports_urlmatch = dict(
        netloc="localhost",
        path="/api/v2/reports",
        method="GET"
    )

    list_reports_urlmatch2 = dict(
        netloc="127.0.0.1",
        path="/api/v2/reports",
        method="GET"
    )

    get_report_urlmatch = dict(
        netloc="localhost",
        path="/api/v2/reports/efd48668-e24a-4a2c-a53f-3f388664b691",
        method="GET"
    )

    get_report_status_urlmatch = dict(
        netloc="localhost",
        path="/api/v3/status/REPORT01",
        method="GET"
    )

    get_report_results_urlmatch = dict(
        netloc="localhost",
        path="/api/v3/results/REPORT01",
        method="GET"
    )

    @urlmatch(**list_reports_urlmatch)
    def list_reports_mock(self, url, request):
        assert url.path == "/api/v2/reports"
        assert request.method == "GET"
        return response(200, self.LIST_REPORTS_RESPONSE, None, None, 5, request)

    @urlmatch(**list_reports_urlmatch2)
    def list_reports_mock2(self, url, request):
        assert url.path == "/api/v2/reports"
        assert request.method == "GET"
        return response(200, self.LIST_REPORTS_RESPONSE2, None, None, 5, request)

    @urlmatch(**get_report_urlmatch)
    def get_report_mock(self, url, request):
        assert url.path == "/api/v2/reports/efd48668-e24a-4a2c-a53f-3f388664b691"
        assert request.method == "GET"
        return response(200, self.GET_REPORT_RESPONSE, None, None, 5, request)

    @urlmatch(**get_report_status_urlmatch)
    def get_report_status_mock(self, url, request):
        assert url.path == "/api/v3/status/REPORT01"
        assert request.method == "GET"
        return response(200, self.GET_REPORT_STATUS_RESPONSE, None, None, 5, request)

    @urlmatch(**get_report_results_urlmatch)
    def get_report_results_mock(self, url, request):
        assert url.path == "/api/v3/results/REPORT01"
        assert request.method == "GET"
        return response(200, self.GET_REPORT_RESULTS_RESPONSE, None, None, 5, request)
