from urllib.parse import parse_qs

from httmock import response, urlmatch


class TrendMocks(object):
    GET_FLAPPING_GROUPS_RESPONSE = (
        """{"status": {"message": "Success", "code": "200"}, "data": [{"endpoint_group": "ARGO_MON", "flapping": 5},"""
        """ {"endpoint_group": "ARGO_MON2", "flapping": 1 }]}"""
    )

    get_flapping_groups_urlmatch = dict(
        netloc="localhost", path="/api/v2/trends/REPORT01/flapping/groups", method="GET"
    )

    @urlmatch(**get_flapping_groups_urlmatch)
    def get_flapping_groups_mock(self, url, request):
        assert url.path == "/api/v2/trends/REPORT01/flapping/groups"
        assert request.method == "GET"
        return response(200, self.GET_FLAPPING_GROUPS_RESPONSE, None, None, 5, request)

    GET_FLAPPING_SERVICES_RESPONSE = (
        """{"status": {"message": "Success", "code": "200"}, "data": [{"endpoint_group": "ARGO_MON", "service":"""
        """ "www.example.com-web", "flapping": 5}, {"endpoint_group": "ARGO_MON2", "service":"""
        """ "www.example.com-api", "flapping": 1 }]}"""
    )

    get_flapping_services_urlmatch = dict(
        netloc="localhost", path="/api/v2/trends/REPORT01/flapping/services", method="GET"
    )

    @urlmatch(**get_flapping_services_urlmatch)
    def get_flapping_services_mock(self, url, request):
        assert url.path == "/api/v2/trends/REPORT01/flapping/services"
        assert request.method == "GET"
        return response(200, self.GET_FLAPPING_SERVICES_RESPONSE, None, None, 5, request)

    GET_FLAPPING_ENDPOINTS_RESPONSE = (
        """{"status": {"message": "Success", "code": "200"}, "data": [{"endpoint_group": "ARGO_MON", "service":"""
        """ "www.example.com-web", "endpoint": "https://www.example.com", "flapping": 5}, {"endpoint_group": """
        """ "ARGO_MON2", "service": "www.example.com-api", "endpoint": "https://api.example.com", "flapping": 1 }]}"""
    )

    get_flapping_endpoints_urlmatch = dict(
        netloc="localhost", path="/api/v2/trends/REPORT01/flapping/endpoints", method="GET"
    )

    @urlmatch(**get_flapping_endpoints_urlmatch)
    def get_flapping_endpoints_mock(self, url, request):
        assert url.path == "/api/v2/trends/REPORT01/flapping/endpoints"
        assert request.method == "GET"
        return response(200, self.GET_FLAPPING_ENDPOINTS_RESPONSE, None, None, 5, request)

    GET_FLAPPING_METRICS_RESPONSE = (
        """{"status": {"message": "Success", "code": "200"}, "data": [{"endpoint_group": "ARGO_MON", "service":"""
        """ "www.example.com-web", "endpoint": "https://www.example.com", "metric": "generic.http.connect","""
        """ "flapping": 5}, {"endpoint_group": "ARGO_MON2", "service": "www.example.com-api", "endpoint":"""
        """ "https://api.example.com", "metric": "generic.http.connect", "flapping": 1 }]}"""
    )

    get_flapping_metrics_urlmatch = dict(
        netloc="localhost", path="/api/v2/trends/REPORT01/flapping/metrics", method="GET"
    )

    @urlmatch(**get_flapping_metrics_urlmatch)
    def get_flapping_metrics_mock(self, url, request):
        assert url.path == "/api/v2/trends/REPORT01/flapping/metrics"
        assert request.method == "GET"
        return response(200, self.GET_FLAPPING_METRICS_RESPONSE, None, None, 5, request)

    GET_FLAPPING_METRIC_TAGS_RESPONSE = (
        """{"status": {"message": "Success", "code": "200"}, "data": ["""
        """ {"tag": "http", "top": ["""
        """ {"endpoint_group": "ARGO_MON", "service":"""
        """ "www.example.com-web", "endpoint": "https://www.example.com", "metric": "generic.http.connect","""
        """ "flapping": 5}, {"endpoint_group": "ARGO_MON2", "service": "www.example.com-api", "endpoint":"""
        """ "https://api.example.com", "metric": "generic.http.connect", "flapping": 1 }"""
        """ ]},"""
        """ {"tag": "network", "top": ["""
        """ {"endpoint_group": "ARGO_MON", "service":"""
        """ "www.example.com-web", "endpoint": "https://www.example.com", "metric": "generic.http.connect","""
        """ "flapping": 5}, {"endpoint_group": "ARGO_MON2", "service": "www.example.com-api", "endpoint":"""
        """ "https://api.example.com", "metric": "generic.http.connect", "flapping": 1 }"""
        """ ]}"""
        """]}"""
    )

    get_flapping_metric_tags_urlmatch = dict(
        netloc="localhost", path="/api/v2/trends/REPORT01/flapping/metrics/tags", method="GET"
    )

    @urlmatch(**get_flapping_metric_tags_urlmatch)
    def get_flapping_metric_tags_mock(self, url, request):
        assert url.path == "/api/v2/trends/REPORT01/flapping/metrics/tags"
        assert request.method == "GET"
        return response(200, self.GET_FLAPPING_METRIC_TAGS_RESPONSE, None, None, 5, request)


class IssueMocks(object):
    GET_ENDPOINT_METRIC_RESULT_RESPONSE = (
        """{"root": [{"Name": "www.example.com_ABCD","info": {"ID": "ABCD","URL":"""
        """ "https://www.example.com"},"Metrics": [{"Name": "generic.http.connect","Service":"""
        """ "www.example.com-web","Details": [{"Timestamp": "2025-10-05T02:23:16Z","Value":"""
        """ "CRITICAL","Summary":"""
        """ "Cannot connect to www.example.com on port 443","Message": "''"}]}]}]}"""
    )

    get_endpoint_metric_result_urlmatch = dict(
        netloc="localhost", path="/api/v2/metric_result/www.example.com_ABCD", method="GET"
    )

    @urlmatch(**get_endpoint_metric_result_urlmatch)
    def get_endpoint_metric_result_mock(self, url, request):
        assert url.path == "/api/v2/metric_result/www.example.com_ABCD"
        assert request.method == "GET"
        return response(200, self.GET_ENDPOINT_METRIC_RESULT_RESPONSE, None, None, 5, request)

    GET_ENDPOINT_METRIC_RESULT_METRIC_RESPONSE = (
        """{"root": [{"Name": "www.example.com_ABCD","info": {"ID": "ABCD","URL":"""
        """ "https://www.example.com"},"Metrics": [{"Name": "generic.http.connect","Service":"""
        """ "www.example.com-web","Details": [{"Timestamp": "2025-10-05T02:23:16Z","Value":"""
        """ "CRITICAL","Summary":"""
        """ "Cannot connect to www.example.com on port 443","Message": "''"}]}]}]}"""
    )

    get_endpoint_metric_result_metric_urlmatch = dict(
        netloc="localhost", path="/api/v2/metric_result/www.example.com_ABCD/generic.http.connect", method="GET"
    )

    @urlmatch(**get_endpoint_metric_result_metric_urlmatch)
    def get_endpoint_metric_result_metric_mock(self, url, request):
        assert url.path == "/api/v2/issues/www.example.com_ABCD/generic.http.connect"
        assert request.method == "GET"
        return response(200, self.GET_ENDPOINT_METRIC_RESULT_METRIC_RESPONSE, None, None, 5, request)

    LIST_TESTREPORT_ENDPOINT_ISSUES_RESPONSE = (
        """{ "status": { "message": "Success", "code": "200" }, "data": [ { "timestamp": "2025-10-05T00:00:00Z","""
        """ "endpoint_group": "ARGO_MON", "service": "www.example.com-example.api", "endpoint": """
        """ "www.example.com_01-234567-890ABC", "status": "CRITICAL", "info": { "ID": "01-234567-890ABC", "URL": """
        """ "https://www.example.com/api", "groupname": "ARGO_MON" } }, { "timestamp": "2025-10-05T00:00:00Z", """
        """ "endpoint_group": "ARGO_MON", "service": "www.example.com-web", "endpoint": "www.example.com_ABCD", """
        """ "status": "WARNING", "info": { "ID": "ABCD", "URL": "https://www.example.com" } } ] }"""
    )

    LIST_TESTREPORT_ENDPOINT_ISSUES_RESPONSE_CRITICAL = (
        """{ "status": { "message": "Success", "code": "200" }, "data": [ { "timestamp": "2025-10-05T00:00:00Z","""
        """ "endpoint_group": "ARGO_MON", "service": "www.example.com-example.api", "endpoint": """
        """ "www.example.com_01-234567-890ABC", "status": "CRITICAL", "info": { "ID": "01-234567-890ABC", "URL": """
        """ "https://www.example.com/api", "groupname": "ARGO_MON" } } ] }"""
    )

    list_testreport_endpoint_issues_urlmatch = dict(
        netloc="localhost", path="/api/v2/issues/REPORT01/endpoints", method="GET"
    )

    @urlmatch(**list_testreport_endpoint_issues_urlmatch)
    def list_testreport_endpoint_issues_mock(self, url, request):
        assert url.path == "/api/v2/issues/REPORT01/endpoints"
        assert request.method == "GET"
        qs = parse_qs(url.query)
        if 'filter' in qs and 'CRITICAL' in qs.get("filter"):
            return response(200, self.LIST_TESTREPORT_ENDPOINT_ISSUES_RESPONSE_CRITICAL, None, None, 5, request)
        else:
            return response(200, self.LIST_TESTREPORT_ENDPOINT_ISSUES_RESPONSE, None, None, 5, request)

    LIST_TESTREPORT_METRIC_ISSUES_RESPONSE = (
        """{ "status": { "message": "Success", "code": "200" }, "data": [ { "service": "www.example.com-example.web","""
        """ "hostname": "www.example.com_01-234567-890ABC", "metric": "generic.certificate.validity", "status":"""
        """ "WARNING", "info": { "ID": "01-234567-890ABC", "URL": "https://www.example.com" } }, { "service":"""
        """ "www.example.com-example.api", "hostname": "api.example.com_EFGH", "metric": "generic.http.connect","""
        """ "status": "CRITICAL", "info": { "ID": "EFGH", "URL": "https://api.example.com" } } ] }"""
    )

    LIST_TESTREPORT_METRIC_ISSUES_RESPONSE_CRITICAL = (
        """{ "status": { "message": "Success", "code": "200" }, "data": [ { "service":"""
        """ "www.example.com-example.api", "hostname": "api.example.com_EFGH", "metric": "generic.http.connect","""
        """ "status": "CRITICAL", "info": { "ID": "EFGH", "URL": "https://api.example.com" } } ] }"""
    )

    list_testreport_metric_issues_urlmatch = dict(
        netloc="localhost", path="/api/v2/issues/REPORT01/groups/ARGO_MON/metrics", method="GET"
    )

    @urlmatch(**list_testreport_metric_issues_urlmatch)
    def list_testreport_metric_issues_mock(self, url, request):
        assert url.path == "/api/v2/issues/REPORT01/groups/ARGO_MON/metrics"
        assert request.method == "GET"
        qs = parse_qs(url.query)
        if 'filter' in qs and 'CRITICAL' in qs.get("filter"):
            return response(200, self.LIST_TESTREPORT_METRIC_ISSUES_RESPONSE_CRITICAL, None, None, 5, request)
        else:
            return response(200, self.LIST_TESTREPORT_METRIC_ISSUES_RESPONSE, None, None, 5, request)


class ReportMocks(object):
    LIST_REPORTS_RESPONSE = (
        """{"status": {"message": "Success", "code": "200"}, "data": [{"id": "efd48668-e24a-4a2c-a53f-3f388664b691","""
        """ "tenant": "TENANT01", "disabled": false, "info": {"name": "REPORT01", "description": "REPORT01 A/R """
        """report", "created": "2025-03-06 12:53:27", "updated": "2025-03-06 12:53:27"}, "computations": {"ar": true,"""
        """ "status": true, "trends": ["flapping", "status", "tags"]}, "thresholds": {"availability": 80, """
        """"reliability": 90, "uptime": 0.8, "unknown": 0.1, "downtime": 0.1}, "topology_schema": {"group": {"type":"""
        """ "PROJECT", "group": {"type": "SERVICEGROUPS"}}}, "profiles": [{"id": "5c3218ea-3f67-4d4c-b3ce-"""
        """f650b8ed8e68", "name": "ARGO_MON", "type": "metric"}, {"id": "ede2a9f7-e754-47fa-8e76-449e3925fbd4","""
        """ "name": "core", "type": "aggregation"}, {"id": "be1fbf37-77f3-4a9e-b268-a6a9a0830ef5", "name": "ops","""
        """ "type": "operations"}], "filter_tags": [{"name": "FT1", "value": "val", "context": "cntx"}]}]}"""
    )

    LIST_REPORTS_RESPONSE2 = (
        """{"status": {"message": "Success", "code": "200"}, "data": [{"id": "efd48668-e24a-4a2c-a53f-3f388664b692","""
        """ "tenant": "TENANT02", "disabled": false, "info": {"name": "REPORT02", "description": "REPORT02 A/R """
        """report", "created": "2025-03-06 12:53:27", "updated": "2025-03-06 12:53:27"}, "computations": {"ar": true,"""
        """ "status": true, "trends": ["flapping", "status", "tags"]}, "thresholds": {"availability": 80, """
        """"reliability": 90, "uptime": 0.8, "unknown": 0.1, "downtime": 0.1}, "topology_schema": {"group": {"type":"""
        """ "PROJECT", "group": {"type": "SERVICEGROUPS"}}}, "profiles": [{"id": "5c3218ea-3f67-4d4c-b3ce-"""
        """f650b8ed8e68", "name": "ARGO_MON", "type": "metric"}, {"id": "ede2a9f7-e754-47fa-8e76-449e3925fbd4","""
        """ "name": "core", "type": "aggregation"}, {"id": "be1fbf37-77f3-4a9e-b268-a6a9a0830ef5", "name": "ops","""
        """ "type": "operations"}], "filter_tags": [{"name": "FT1", "value": "val", "context": "cntx"}]}]}"""
    )

    GET_REPORT_RESPONSE = LIST_REPORTS_RESPONSE

    GET_REPORT_STATUS_RESPONSE = (
        """{"groups": [{"name": "ARGO_MON", "type": "SERVICEGROUPS", "statuses": """
        """[{"timestamp": "2025-06-01T00:00:00Z", "value": "OK"}, {"timestamp":"""
        """ "2025-06-01T23:59:59Z", "value": "OK"}], "endpoints": [{"hostname":"""
        """ "www.example.com", "service": "www.example.com-example.api", "info":"""
        """ {"ID": "EXAMPLE01", "URL": "https://www.example.com/api/action?foo=bar"},"""
        """ "statuses": [{"timestamp": "2025-06-01T00:00:00Z", "value": "OK"}, {"timestamp":"""
        """ "2025-06-01T23:59:59Z", "value": "OK"}]}]}]}"""
    )

    GET_REPORT_RESULTS_RESPONSE = (
        """{"results": [{"name": "TENANT01", "type": "PROJECT", "results": [{"date": "2025-06-01", "availability":"""
        """ "100", "reliability": "100"}], "groups": [{"name": "ARGO_MON", "type": "SERVICEGROUPS", "results":"""
        """ [{"date": "2025-06-01", "availability": "100", "reliability": "100", "unknown": "0", "uptime": "1","""
        """ "downtime": "0"}]}]}]}"""
    )

    list_reports_urlmatch = dict(
        netloc="localhost", path="/api/v2/reports", method="GET"
    )

    list_reports_urlmatch2 = dict(
        netloc="127.0.0.1", path="/api/v2/reports", method="GET"
    )

    get_report_urlmatch = dict(
        netloc="localhost",
        path="/api/v2/reports/efd48668-e24a-4a2c-a53f-3f388664b691",
        method="GET",
    )

    get_report_status_urlmatch = dict(
        netloc="localhost", path="/api/v3/status/REPORT01", method="GET"
    )

    get_report_results_urlmatch = dict(
        netloc="localhost", path="/api/v3/results/REPORT01", method="GET"
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
