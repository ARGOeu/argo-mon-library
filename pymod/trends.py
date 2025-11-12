from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from .restresource import RestResourceItem, RestResourceList

if TYPE_CHECKING:
    from .argomonitoringservice import ArgoMonitoringService
    from .reports import Report


class FlappingType(IntEnum):
    """Enumeration type for flapping items"""

    GROUPS = 1
    SERVICES = 2
    ENDPOINTS = 3
    METRICS = 4
    METRIC_TAGS = 5


class Trends(object):
    """Helper class for group, endpoint, service, and metric trends"""

    def __init__(self, parent: Report):
        self._parent: Report = parent

    def flapping(self, flapping_type: FlappingType, top: int = 0):
        self._top: int = top
        if flapping_type == FlappingType.GROUPS:
            return FlappingGroups(self)
        elif flapping_type == FlappingType.SERVICES:
            return FlappingServices(self)
        elif flapping_type == FlappingType.ENDPOINTS:
            return FlappingEndpoints(self)
        elif flapping_type == FlappingType.METRICS:
            return FlappingMetrics(self)
        elif flapping_type == FlappingType.METRIC_TAGS:
            return FlappingMetricTags(self)
        else:
            raise ValueError("Unsupported enum value for flapping type")


class FlappingItemsBase(RestResourceList):
    """Base class for all flapping trends"""

    def __init__(self, parent: Trends):
        self._top: int = parent._top  # get 'top' parameter from parent
        super().__init__(parent)
        self._parent: ArgoMonitoringService = parent._parent._parent  # set parent to argo service object
        self._report: Report = parent._parent  # set report from parent

    def _fetch_args(self):
        return [self._report.name]

    def _fetch_params(self):
        args = {
                "start_date": self._parent._parent._period._start_date.strftime("%Y-%m-%d"),
                "end_date": self._parent._parent._period._end_date.strftime("%Y-%m-%d"),
                "granularity": self._parent._parent._period._granularity
                }
        if self._top != 0:
            args["top"] = self._top
        return args


class FlappingGroups(FlappingItemsBase):
    """Collection class for flapping group trends"""

    @property
    def id_name(self):
        return "endpoint_group"

    def _fetch_route(self):
        return "get_flapping_groups"

    def _create_child(self, data: dict):
        return FlappingGroup(self, data)


class FlappingServices(FlappingGroups):
    """Collection class for flapping service trends"""

    def _fetch_route(self):
        return "get_flapping_services"

    def _create_child(self, data: dict):
        return FlappingService(self, data)


class FlappingEndpoints(FlappingServices):
    """Collection class for flapping endpoint trends"""

    def _fetch_route(self):
        return "get_flapping_endpoints"

    def _create_child(self, data: dict):
        return FlappingEndpoint(self, data)


class FlappingMetrics(FlappingEndpoints):
    """Collection class for flapping metric trends"""

    def _fetch_route(self):
        return "get_flapping_metrics"

    def _create_child(self, data: dict):
        return FlappingMetric(self, data)


class FlappingMetricTags(FlappingItemsBase):
    """Collection class for flapping metric trends by tag"""

    @property
    def id_name(self):
        return "tag"

    def _fetch_route(self):
        return "get_flapping_metric_tags"

    def _create_child(self, data: dict):
        return FlappingMetricTag(self, data)


class FlappingItemBase(RestResourceItem):
    """Base class for all flapping items"""

    def __init__(self, parent, data={}):
        super().__init__(parent, data)
        if data is not None:
            self.flapping = data.get("flapping")
            self.endpoint_group = data.get("endpoint_group")
            delattr(self, "id")  # flapping objects have no meaningful id attribute

    @property
    def flapping(self):
        return self._flapping

    @flapping.setter
    def flapping(self, value):
        self._flapping = value

    @property
    def endpoint_group(self):
        return self._endpoint_group

    @endpoint_group.setter
    def endpoint_group(self, value):
        self._endpoint_group = value

    def _fetch_route(self):
        return ""

    def _fetch_args(self):
        return []


class FlappingGroup(FlappingItemBase):
    pass


class FlappingService(FlappingGroup):
    def __init__(self, parent, data={}):
        super().__init__(parent, data)
        if data is not None:
            self.service = data.get("service")

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, value):
        self._service = value


class FlappingEndpoint(FlappingService):
    def __init__(self, parent, data={}):
        super().__init__(parent, data)
        if data is not None:
            self.endpoint = data.get("endpoint")

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value


class FlappingMetric(FlappingEndpoint):
    def __init__(self, parent, data={}):
        super().__init__(parent, data)
        if data is not None:
            self.metric = data.get("metric")

    @property
    def metric(self):
        return self._metric

    @metric.setter
    def metric(self, value):
        self._metric = value


class FlappingMetricTag(RestResourceItem):
    """For metric tags, the API returns data aggregated differently wrt to other flapping resources.
    Inherit from RestResourceItem instead of FlappingItemsBase or descentants.
    Actual flapping metrics that belong to a tag wiil be exposed by the 'metrics' property
    """
    def __init__(self, parent, data={}):
        super().__init__(parent, data)
        if data is not None:
            self.tag = data.get("tag")
            self._x_metrics = []
            for i in data.get("top"):
                self._x_metrics.append(FlappingMetric(self, i))
            delattr(self, "top")
            delattr(self, "id")

    def _fetch_route(self):
        return ""

    def _fetch_args(self):
        return []

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    @property
    def metrics(self) -> list[FlappingMetric]:
        """List of flapping metrics that belong under the tag in question"""
        return self._x_metrics
