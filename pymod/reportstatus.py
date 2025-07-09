from .restresource import RestResourceList, RestResourceItem
from datetime import datetime
import json

class ReportStatusGroupStatus(RestResourceItem):
    timestamp = ""
    value = ""

    def __init__(self, parent, data = {}):
        if data is not None:
            self.timestamp = datetime.strptime(data.get("timestamp"), '%Y-%m-%dT%H:%M:%SZ')
            self.value = data.get("value")

    def _fetchRoute(self):
        return ""

    def _fetchArgs(self) -> list:
        return []


class ReportStatusGroupStatuses(RestResourceList):
    def __init__(self, parent):
        super().__init__(parent, 1)
        self._fetch()

    def _fetch(self):
        for i in self._parent._statuses:
            self.update({i["timestamp"]: ReportStatusGroupStatus(self, i)})
            self._pageCount = 1
            self._currentPage = 1


class ReportStatusGroupEndpoint(RestResourceItem):
    hostname = ""
    service = ""
    id = ""
    url = ""
    statuses = []

    def __init__(self, parent, data = {}):
        super().__init__(parent, data)
        if data is not None:
            self.name= data.get("hostname")
            self.service = data.get("service")
            self.id = data.get("info").get("ID")
            self.url = data.get("info").get("URL")
            self.statuses = data.get("statuses")

    @property
    def statuses(self):
        return ReportStatusGroupStatuses(self)

    @statuses.setter
    def statuses(self, value):
        self._statuses = value

    def _fetchRoute(self):
        return ""

    def _fetchArgs(self) -> list:
        return []


class ReportStatusGroupEndpoints(RestResourceList):
    def __init__(self, parent):
        super().__init__(parent, 1)
        self._fetch()

    def _fetch(self):
        for i in self._parent._endpoints:
            self.update({i["info"]["ID"]: ReportStatusGroupEndpoint(self, i)})
            self._pageCount = 1
            self._currentPage = 1

    def byName(self, name: str):
        for i in self:
            if i.name == name:
                return i
        return None


class ReportStatusGroup(RestResourceItem):
    name = ""
    type = ""

    def __init__(self, parent, data = {}):
        super().__init__(parent, data)
        if data is not None:
            self.name= data.get("name")
            self.type = data.get("type")
            self.statuses = data.get("statuses")
            self.endpoints = data.get("endpoints")

    @property
    def statuses(self):
        return ReportStatusGroupStatuses(self)

    @statuses.setter
    def statuses(self, value):
        self._statuses = value

    @property
    def endpoints(self):
        return ReportStatusGroupEndpoints(self)

    @endpoints.setter
    def endpoints(self, value):
        self._endpoints = value

    def _fetchRoute(self):
        return ""

    def _fetchArgs(self) -> list:
        return []


class ReportStatusGroups(RestResourceList):
    def __init__(self, parent):
        super().__init__(parent, 1)
        self._fetch()

    def _fetch(self):
        for i in self._parent._groups:
            self.update({i["name"]: ReportStatusGroup(self, i)})
            self._pageCount = 1
            self._currentPage = 1

    def byName(self, name: str):
        for i in self:
            if i.name == name:
                return i
        return None

class ReportStatus(RestResourceItem):
    @property
    def groups(self) -> ReportStatusGroups:
        return ReportStatusGroups(self)

    @groups.setter
    def groups(self, value):
        self._groups = value

    @property
    def dataRoot(self):
        return None

    def _fetchRoute(self):
        return "get_report_status"

    def _fetchArgs(self) -> list:
        return [self.id]

    def _fetchParams(self) -> dict:
        return {
            "start_time": (str(self._parent._parent._parent._period._startDate) + "Z").replace(" ", "T"),
            "end_time": (str(self._parent._parent._parent._period._endDate) + "Z").replace(" ", "T")
        }
