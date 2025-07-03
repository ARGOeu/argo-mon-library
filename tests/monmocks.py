from httmock import urlmatch, response
import json

class ReportMocks(object):
    LIST_REPORTS_RESPONSE = """{"status": {"message": "Success", "code": "200"}, "data": [{"id": "efd48668-e24a-4a2c-a53f-3f388664b691", "tenant": "TENANT01", "disabled": false, "info": {"name": "REPORT01", "description": "REPORT01 A/R report", "created": "2025-03-06 12:53:27", "updated": "2025-03-06 12:53:27"}, "computations": {"ar": true, "status": true, "trends": ["flapping", "status", "tags"]}, "thresholds": {"availability": 80, "reliability": 90, "uptime": 0.8, "unknown": 0.1, "downtime": 0.1}, "topology_schema": {"group": {"type": "PROJECT", "group": {"type": "SERVICEGROUPS"}}}, "profiles": [{"id": "5c3218ea-3f67-4d4c-b3ce-f650b8ed8e68", "name": "ARGO_MON", "type": "metric"}, {"id": "ede2a9f7-e754-47fa-8e76-449e3925fbd4", "name": "core", "type": "aggregation"}, {"id": "be1fbf37-77f3-4a9e-b268-a6a9a0830ef5", "name": "ops", "type": "operations"}], "filter_tags": [{"name": "FT1", "value": "val", "context": "cntx"}]}]}"""

    GET_REPORT_RESPONSE = LIST_REPORTS_RESPONSE

    list_reports_urlmatch = dict(
        netloc="localhost",
        path="/api/v2/reports",
        method="GET"
    )

    get_report_urlmatch = dict(
        netloc="localhost",
        path="/api/v2/reports/efd48668-e24a-4a2c-a53f-3f388664b691",
        method="GET"
    )

    @urlmatch(**list_reports_urlmatch)
    def list_reports_mock(self, url, request):
        assert url.path == "/api/v2/reports"
        assert request.method == "GET"
        return response(200, self.LIST_REPORTS_RESPONSE, None, None, 5, request)

    @urlmatch(**get_report_urlmatch)
    def get_report_mock(self, url, request):
        assert url.path == "/api/v2/reports/efd48668-e24a-4a2c-a53f-3f388664b691"
        assert request.method == "GET"
        return response(200, self.GET_REPORT_RESPONSE, None, None, 5, request)
