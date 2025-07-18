from .restresource import RestResourceList, RestResourceItem
from datetime import datetime
import json

class ReportResultsGroup(RestResourceItem):
    name = ""
    type = ""

    def __init__(self, parent, data = {}):
        super().__init__(parent, data)
        if data is not None:
            self.name= data.get("name")
            self.type = data.get("type")
            self.results = data.get("results")

    @property
    def results(self):
        return ReportResultsResults(self)

    @results.setter
    def results(self, value):
        self._results = value

    def _fetchRoute(self):
        return ""

    def _fetchArgs(self) -> list:
        return []


class ReportResultsGroups(RestResourceList):
    def __init__(self, parent):
        super().__init__(parent, 1)
        self._fetch()

    def _fetch(self):
        for i in self._parent._groups:
            self.update({i["name"]: ReportResultsGroup(self, i)})
            self._pageCount = 1
            self._currentPage = 1

    def byName(self, name: str):
        for i in self:
            if i.name == name:
                return i
        return None


class ReportResultsResult(RestResourceItem):
    date = ""
    availability = ""
    reliability = ""
    unknown = ""
    uptime = ""
    downtime = ""

    def __init__(self, parent, data = {}):
        super().__init__(parent, data)
        if data is not None:
            try:
                self.date = datetime.strptime(data.get("date"), '%Y-%m-%d')
            except ValueError:
                self.date = datetime.strptime(data.get("date"), '%Y-%m')
            self.availability = data.get("availability")
            self.reliability = data.get("reliability")
            self.unknown = data.get("unknown")
            self.uptime = data.get("uptime")
            self.downtime = data.get("downtime")

    def _fetchRoute(self):
        return ""

    def _fetchArgs(self) -> list:
        return []


class ReportResultsResults(RestResourceList):
    def __init__(self, parent):
        super().__init__(parent, 1)
        self._fetch()

    def _fetch(self):
        for i in self._parent._results:
            self.update({i["date"]: ReportResultsResult(self, i)})
            self._pageCount = 1
            self._currentPage = 1


class ReportResults(RestResourceItem):
    @property
    def dataRoot(self):
        return "results"

    @property
    def groups(self) -> ReportResultsGroups:
        """Parent object to results of a specific group"""
        return ReportResultsGroups(self)

    @groups.setter
    def groups(self, value):
        self._groups = value

    @property
    def toplevel(self) -> ReportResultsResults:
        """
        Alternative property for top-level results.
        Equivalent to ArgoMonitoringService::results::results
        """
        return self.results

    def byGroup(self, group):
        """
        Shortcut to results for a specific group
        Equivalent to ArgoMonitoringService::results::groups[…]::results
        """
        return self.groups[group].results

    @property
    def results(self) -> ReportResultsResults:
        """Get top-level results"""
        return ReportResultsResults(self)

    @results.setter
    def results(self, value):
        self._results = value

    def _fetchRoute(self):
        return "get_report_results"

    def _fetchArgs(self) -> list:
        return [self.id]

    def _fetchParams(self) -> dict:
        return {
            "start_time": (str(self._parent._parent._parent._period._startDate) + "Z").replace(" ", "T"),
            "end_time": (str(self._parent._parent._parent._period._endDate) + "Z").replace(" ", "T"),
            "granularity": self._parent._parent._parent._period._granularity
        }
