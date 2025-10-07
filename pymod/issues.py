from __future__ import annotations

from typing import TYPE_CHECKING

from .restresource import RestResourceItem, RestResourceList

if TYPE_CHECKING:
    from .reports import Report


class Issues(object):
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
        args = {"date": self._parent._parent._period._start_date.strftime('%Y-%m-%d')}
        if self._status != "":
            args["filter"] = self._status
        return args


class EndpointIssue(IssueBase):
    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value


class EndpointIssues(IssuesBase):
    def _fetch_route(self):
        return "get_endpoint_issues"

    def _create_child(self, data: dict):
        return EndpointIssue(self, data)


class MetricIssue(IssueBase):
    pass


class MetricIssues(IssuesBase):
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
