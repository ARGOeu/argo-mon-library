from __future__ import annotations

from typing import TYPE_CHECKING

from .restresource import RestResourceItem, RestResourceList

if TYPE_CHECKING:
    from .reports import Report


class Issues(object):
    """Helper class for endpoint and metric issues"""

    def __init__(self, parent: Report):
        self._parent = parent

    def by_endpoint(self, status: str = ""):
        return EndpointIssues(self, status)

    def by_metric(self, group_name: str, status: str = ""):
        return MetricIssues(self, group_name, status)


class IssueBase(RestResourceItem):
    """Endpoint issue representation class"""

    def __init__(self, parent, data={}):
        super().__init__(parent, data)
        if data is not None:
            self.id = data.get("info").get("ID")
            self.url = data.get("info").get("URL")
            self.groupname = data.get("info").get("groupname")
            delattr(self, "info")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def groupname(self):
        return self._groupname

    @groupname.setter
    def groupname(self, value):
        self._groupname = value

    def _fetch_route(self):
        return ""

    def _fetch_args(self):
        return []


class IssuesBase(RestResourceList):
    """Base class for endpoint and metric issues"""

    def __init__(self, parent: Issues, status: str = ""):
        self._status = status
        super().__init__(parent)
        self._parent = parent._parent._parent
        self._report = parent._parent

    @property
    def id_name(self):
        return "endpoint"

    def _fetch_args(self):
        return [self._report.name]

    def _fetch_params(self):
        args = {"date": self._parent._parent._period._start_date.strftime("%Y-%m-%d")}
        if self._status != "":
            args["filter"] = self._status
        return args


class EndpointIssue(IssueBase):
    """Endpoint issue representation class"""
    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value

    @property
    def metrics(self):
        return EndpointIssueMetrics(self, {"__fetch__": self.endpoint})


class EndpointIssues(IssuesBase):
    """Collection class for endpoint issues"""
    def _fetch_route(self):
        return "get_endpoint_issues"

    def _create_child(self, data: dict):
        return EndpointIssue(self, data)


class MetricIssue(IssueBase):
    """Metric issue representation class"""
    pass


class MetricIssues(IssuesBase):
    """Collection class for metric issues"""
    def __init__(self, parent: Issues, group_name: str, status: str = ""):
        self._group_name = group_name
        super().__init__(parent, status)

    @property
    def id_name(self):
        return ["metric", "info.ID"]

    def _fetch_route(self):
        return "get_metric_issues"

    def _fetch_args(self):
        return [self._report.name, self._group_name]

    def _create_child(self, data: dict):
        return MetricIssue(self, data)


class EndpointIssueMetricDetail(RestResourceItem):
    """Metric result details representation class for endpoint issues"""

    def __init__(self, parent, data={}):
        super().__init__(parent, data)
        if data is not None:
            self.timestamp = data.get("Timestamp")
            self.summary = data.get("Summary")
            self.value = data.get("Value")
            self.message = data.get("Message")
        delattr(self, "id")
        delattr(self, "Timestamp")
        delattr(self, "Summary")
        delattr(self, "Value")
        delattr(self, "Message")

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    def _fetch_route(self):
        return ""

    def _fetch_args(self):
        return []


class EndpointIssueMetricDetails(RestResourceList):
    """Collection class for metric result details of endpoint issues"""

    def __init__(self, parent: EndpointIssueMetric):
        super().__init__(parent, 1)
        self._fetch()

    def _fetch(self):
        for i in self._parent._x_details_data:
            self.update({i["Timestamp"]: EndpointIssueMetricDetail(self, i)})
            self._pageCount = 1
            self._current_page = 1

    def _fetch_route(self):
        return ""

    def _fetch_args(self) -> list:
        return []

    def _create_child(self, data: dict):
        if data is not None and not (
            len(data) == 1 and (data.get("__fetch__") is not None)
        ):
            return EndpointIssueMetricDetail(self, data)
        elif data is not None and (
            len(data) == 1 and (data.get("__fetch__") is not None)
        ):
            raise KeyError(data.get("__fetch__"))
        else:
            raise ValueError("Argument 'data' cannot be None")


class EndpointIssueMetric(RestResourceItem):
    """Metric representation class for endpoint issues"""

    def __init__(self, parent, data={}):
        super().__init__(parent, data)
        if data is not None and not (
            len(data) == 1 and (data.get("__fetch__") is not None)
        ):
            self.name = self.Name
            self.service = self.Service
            self._x_details_data = self.Details
            delattr(self, "id")
            delattr(self, "Name")
            delattr(self, "Service")
            delattr(self, "Details")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, value):
        self._service = value

    @property
    def details(self):
        return EndpointIssueMetricDetails(self)

    def _fetch_route(self):
        return "get_endpoint_metric_results_metric"

    def _fetch_args(self):
        return [self._parent._parent.endpoint, self.id]

    def _fetch_params(self):
        args = {
            "exec_time": self._parent._parent._parent._parent._parent._period._start_date.strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        }
        if self._parent._status != "":
            args["filter"] = self._parent._status
        return args


class EndpointIssueMetrics(RestResourceList):
    """Collection class for metrics of endpoint issues"""
    def __init__(self, parent: EndpointIssue, data={}):
        self._status = parent._parent._status
        super().__init__(parent)

    @property
    def id_name(self):
        return "Name"

    @property
    def data_root(self):
        return "root.Metrics"

    def _fetch_route(self):
        return "get_endpoint_metric_results"

    def _fetch_args(self):
        return [self._parent.endpoint]

    def _fetch_params(self):
        args = {
            "exec_time": self._parent._parent._parent._parent._period._start_date.strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        }
        if self._status != "":
            args["filter"] = self._status
        return args

    def _create_child(self, data: dict):
        return EndpointIssueMetric(self, data)
