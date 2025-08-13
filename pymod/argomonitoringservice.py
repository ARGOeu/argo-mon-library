from .httprequests import HttpRequests
from .reports import Reports, Report, ReportStatus, ReportResults
from .exceptions import MonException
from typing import Optional, Union
from datetime import datetime

try:
    from typing import Self, List
except ImportError:
    from typing_extensions import Self, List


class Period(object):
    """
    Helper class used for period definition (start/end date and granularity) for service API calls that need a
    reporting period. See the ArgoMonitoringService::period method for more details.
    """

    def __init__(
        self,
        startDate: Union[datetime, str],
        endDate: Union[datetime, str, None] = None,
        granularity: str = "daily",
    ):
        if type(startDate) is str:
            if startDate == "now":
                self._startDate = datetime.now()
            elif startDate == "today":
                self._startDate = datetime.now().replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
            else:
                self._startDate = datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%SZ")
        else:
            self._startDate = startDate
        if endDate is None:
            self._endDate = self._startDate.replace(
                hour=23, minute=59, second=59, microsecond=0
            )
        else:
            if type(endDate) is str:
                if endDate == "now":
                    self._endDate = datetime.now()
                elif endDate == "today":
                    self._endDate = datetime.now().replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )
                else:
                    self._endDate = datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%SZ")
            else:
                self._endDate = endDate
        if granularity in ["daily", "monthly", "custom"]:
            self._granularity = granularity
        else:
            raise MonException("Invalid granularity parameter")


class ArgoMonitoringService(object):
    """Module main class, to access the REST API"""

    def __init__(self, endpoint: str, apikey: str):
        self._endpoint = endpoint
        self._conn = HttpRequests(apikey)
        self._period = Period(
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
            datetime.now().replace(hour=23, minute=59, second=59, microsecond=0),
        )
        self._reports: Optional[Reports] = None

    @property
    def reports(self) -> Reports:
        """
        Access a list of reports for the current tenant
        """
        self._reports = self._reports or Reports(self)
        return self._reports

    @property
    def connection(self):
        return self._conn

    @property
    def endpoint(self):
        return self._endpoint

    def period(
        self,
        startDate: Union[datetime, str],
        endDate: Union[datetime, str, None] = None,
        granularity="daily",
    ) -> Self:
        """
        Define a period for requests that need a start and end date. After a call to this method, subsequent calls
        will use the same period, until another call changes it. Omitting the endDate parameter will default to the
        end of the same day as the startDate parameter (H:M:S=23:59:59).

        Both startDate and endDate may be either python datetime objects, or Zulu-formatted date-time strings, i.e.:
            1979-01-01T00:00:00Z

        Other datetime formats when passing strings are not supported, with the exception of the literals 'now' and
        'today' which will use the current date and/or time.

        The optional granularity parameter may take the values of 'daily' (default) or 'monthly' and will be used
        to group result values per the respected time frame.
        """
        self._period = Period(startDate, endDate, granularity)
        return self
