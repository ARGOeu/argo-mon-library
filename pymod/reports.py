from .restresource import RestResourceList, RestResourceItem
from datetime import datetime
import json

try:
    from typing import List
except ImportException:
    from typing_extensions import List

class ReportStatusGroupStatus(object):
    timestamp = ""
    value = ""

    def __init__(self, data = {}):
        if data is not None:
            self.timestamp = datetime.strptime(data.get("timestamp"), '%Y-%m-%dT%H:%M:%SZ')
            self.value = data.get("value")

    def __str__(self):
        return json.dumps(self.__dict__)


class ReportStatusGroupEndpoint(object):
    hostname = ""
    service = ""
    id = ""
    url = ""
    statuses = []

    def __init__(self, data = {}):
        if data is not None:
            self.name= data.get("hostname")
            self.service = data.get("service")
            self.id = data.get("info").get("ID")
            self.url = data.get("info").get("URL")
            self.statuses = data.get("statuses")

    @property
    def statuses(self) -> List[ReportStatusGroupStatus]:
        return [ReportStatusGroupStatus(x) for x in self._statuses]

    @statuses.setter
    def statuses(self, value):
        self._statuses = value

    def __str__(self):
        return json.dumps(self.__dict__)

class ReportStatusGroup(object):
    name = ""
    type = ""

    def __init__(self, data = {}):
        if data is not None:
            self.name= data.get("name")
            self.type = data.get("type")
            self.statuses = data.get("statuses")
            self.endpoints = data.get("endpoints")

    @property
    def statuses(self) -> List[ReportStatusGroupStatus]:
        return [ReportStatusGroupStatus(x) for x in self._statuses]

    @statuses.setter
    def statuses(self, value):
        self._statuses = value

    @property
    def endpoints(self) -> List[ReportStatusGroupEndpoint]:
        return [ReportStatusGroupEndpoint(x) for x in self._endpoints]

    @endpoints.setter
    def endpoints(self, value):
        self._endpoints = value

    def __str__(self):
        return json.dumps(self.__dict__)


class ReportStatus(RestResourceItem):
    @property
    def groups(self) -> List[ReportStatusGroup]:
        return [ReportStatusGroup(x) for x in self._groups]

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


class ReportResults(RestResourceItem):
    @property
    def dataRoot(self):
        return None

    def _fetchRoute(self):
        return "get_report_results"

    def _fetchArgs(self) -> list:
        return [self.id]

    def _fetchParams(self) -> dict:
        return {
            "start_time": (str(self._parent._parent._parent._period._startDate) + "Z").replace(" ", "T"),
            "end_time": (str(self._parent._parent._parent._period._endDate) + "Z").replace(" ", "T")
        }

class ReportThresholds(object):
    availability = 0
    reliability = 0
    uptime = 0.
    unknown = 0.
    downtime = 0.

    def __init__(self, data = {}):
        if data is not None:
            self.availability = data.get("availability")
            self.reliability = data.get("reliability")
            self.uptime = data.get("uptime")
            self.unknown = data.get("unknown")
            self.downtime = data.get("downtime")

    def __str__(self):
        return json.dumps(self.__dict__)


class ReportProfile(object):
    id = ""
    type = ""
    name = ""

    def __init__(self, data = {}):
        if data is not None:
            self.id = data.get("id")
            self.type = data.get("type")
            self.name = data.get("name")

    def __str__(self):
        return json.dumps(self.__dict__)

class ReportFilterTag(object):
    name = ""
    value = ""
    context = ""

    def __init__(self, data = {}):
        if data is not None:
            self.name = data.get("name")
            self.value = data.get("value")
            self.context = data.get("context")

    def __str__(self):
        return json.dumps(self.__dict__)

class ReportTopologySchemaGroup(object):
    type = ""
    group = None

    def __init__(self, data = {}):
        if data is not None:
            self.type = data.get("type")
            self.group = ReportTopologySchemaGroup(data.get("group"))

class ReportTopologySchema(object):
    group: ReportTopologySchemaGroup = None

    def __init__(self, data = {}):
        if data is not None:
            self.group = ReportTopologySchemaGroup(data.get("group"))

    def __str__(self):
        return json.dumps(self.__dict__)

class ReportComputations(object):
    ar = False
    status = False
    trends = []

    def __init__(self, data = {}):
        if data is not None:
            self.ar = data.get("ar")
            self.status = data.get("status")
            self.trends = data.get("trends")

    def __str__(self):
        return json.dumps(self.__dict__)

class Report(RestResourceItem):
    @property
    def name(self) -> str:
        return self.info["name"]

    @property
    def description(self) -> str:
        return self.info["description"]

    @property
    def createdOn(self) -> datetime:
        return datetime.strptime(self.info["created"], '%Y-%m-%d %H:%M:%S')

    @property
    def updatedOn(self) -> datetime:
        return datetime.strptime(self.info["updated"], '%Y-%m-%d %H:%M:%S')

    @property
    def computations(self) -> ReportComputations:
        return ReportComputations(self._computations)

    @computations.setter
    def computations(self, value):
        self._computations = value

    @property
    def thresholds(self) -> ReportThresholds:
        return ReportThresholds(self._thresholds)

    @thresholds.setter
    def thresholds(self, value):
        self._thresholds = value

    @property
    def profiles(self) -> list:
        return [ReportProfile(x) for x in self._profiles]

    @profiles.setter
    def profiles(self, value):
        self._profiles = value

    @property
    def filter_tags(self) -> list:
        return [ReportFilterTag(x) for x in self._filter_tags]

    @filter_tags.setter
    def filter_tags(self, value):
        self._filter_tags = value

    @property
    def topology_schema(self) -> ReportTopologySchema:
        return ReportTopologySchema(self._topology_schema)

    @topology_schema.setter
    def topology_schema(self, value):
        self._topology_schema = value

    def _fetchRoute(self):
        return "get_report"

    def _fetchArgs(self) -> list:
        return [self.id]

    @property
    def status(self) -> ReportStatus:
        return ReportStatus(self, {"__fetch__": self.name})

    @property
    def results(self) -> ReportResults:
        return ReportResults(self, {"__fetch__": self.name})

class Reports(RestResourceList):
    def _fetchRoute(self):
        return "get_reports"

    def _fetchArgs(self) -> list:
        return []

    def _createChild(self, data):
        return Report(self, data)

    def byName(self, name: str):
        for i in self:
            if i.name == name:
                return i
        return None
