from .restresource import RestResourceList, RestResourceItem
from .reportresults import ReportResults
from .reportstatus import ReportStatus
from datetime import datetime
import json

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

    def __init__(self, parent, data = {}):
        if data is not None:
            self.id = data.get("id")
            self.type = data.get("type")
            self.name = data.get("name")

    def __str__(self):
        return json.dumps(self.__dict__)

class ReportProfiles(RestResourceList):
    def __init__(self, parent, data = {}):
        super().__init__(parent, 1)
        self._fetch()

    def _fetch(self):
        for i in self._parent._profiles:
            self.update({i["id"]: ReportProfile(self, i)})
            self._pageCount = 1
            self._currentPage = 1

    def byName(self, name: str):
        for i in self:
            if i.name == name:
                return i
        return None


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

class ReportTopologySchemaGroup(RestResourceItem):
    type = ""
    group = None

    def __init__(self, parent, data = {}):
        super().__init__(parent, data)
        if data is not None:
            self.type = data.get("type")
            if data.get("group") is not None:
                self.group = ReportTopologySchemaGroup(self, data.get("group"))
            else:
                self.group = None

    def _fetchRoute(self):
        return ""

    def _fetchArgs(self) -> list:
        return []

class ReportTopologySchema(RestResourceItem):
    group: ReportTopologySchemaGroup = None

    def __init__(self, parent, data = {}):
        super().__init__(parent, data)
        if data is not None:
            self.group = ReportTopologySchemaGroup(self, data.get("group"))

    def _fetchRoute(self):
        return ""

    def _fetchArgs(self) -> list:
        return []


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
        return ReportProfiles(self, self._profiles)

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
        return ReportTopologySchema(self, self._topology_schema)

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
