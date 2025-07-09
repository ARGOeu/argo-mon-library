from .restresource import RestResourceList, RestResourceItem
from datetime import datetime
import json

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
            self.date = datetime.strptime(data.get("date"), '%Y-%m-%d')
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
    def results(self) -> ReportResultsResults:
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
