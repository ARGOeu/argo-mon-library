from collections import OrderedDict
import json
import abc
from time import sleep
import logging
from typing import Union

logger = logging.getLogger(__name__)


class RestResource(abc.ABC):
    """Base class for REST API responses"""

    def __init__(self, parent):
        """Initialize a REST response

        Args:
            parent(oject): an ArgoMonitoringService object or another RestResource instance
        """
        self._parent = parent

    @property
    def endpoint(self):
        return self._parent.endpoint

    @property
    def connection(self):
        return self._parent.connection

    @property
    def idName(self):
        """Return the JSON field name that identifies the resource. Defaults to "id", subclasses may need to override it"""
        return "id"

    @property
    def dataRoot(self):
        """Return the JSON field name that contains the resource data. Defaults to "data", subclasses may need to override it"""
        return "data"

    def _fetchParams(self) -> dict:
        """Method to provide values for querystring params on the GET REST route"""
        return {}

class RestResourceItem(RestResource):
    """Base class for REST API responses representing a single item"""

    id = None

    def __init__(self, parent, data: dict):
        """
        Initialize a REST response item, setting properties from provided data dictionary.
        If the dictionary contains a single entry named "__fetch__" instead of actual response data,
        then the data will be fetched from the API.
        """
        logger.debug("Initing RestResourceItem object " + str(type(self)))
        self._parent = parent
        if len(data) == 1 and data.get("__fetch__") is not None:
            self.id = data["__fetch__"]
            if self.dataRoot is None:
                data = self._fetch()
            else:
                data = self._fetch()[self.dataRoot][0]
        for k in data:
            # logger.debug("setting " + k + " to " + (str(data[k]) or "<None>"))
            setattr(self, k, data[k])

    def __str__(self):
        """Return a JSON representation of the resource, recursivly."""
        # Extract a dictonary of primitive properties
        d1 = {
            x: self.__dict__[x]
            for x in self.__dict__
            if not isinstance(self.__dict__[x], RestResource)
            and x not in {"_parent", "parent"}
        }
        while True:
            changed = False
            for k, v in d1.items():
                if k.startswith("__"):
                    del d1[k]
                    changed = True
                    break
                if k.startswith("_"):
                    d1[k[1:]] = v
                    del d1[k]
                    changed = True
                    break
            if not changed:
                break
        # Loop over properties that are RestResource instances (excluding "_parent")
        # and append their properties to the dictionary
        for x in self.__dict__:
            if isinstance(self.__dict__[x], RestResource) and x not in {"_parent"}:
                d2 = self.__dict__[x].__dict__
                del d2["_parent"]
                d1 = {**d1, x: d2}
        # Return a JSON representation of the built dictionary
        return json.dumps(d1, default=str)

    @abc.abstractmethod
    def _fetchRoute(self) -> str:
        """Abstract method to be implemented by subclasses, to denote the REST API route for GET requests

        Should return the key from the parent service object route dict, that corresponds to the REST route
        """
        return ""

    @abc.abstractmethod
    def _fetchArgs(self) -> list:
        """Abstract method to be implemented by subcasses, to provide values for params on the GET REST route"""
        return []

    def _fetch(self):
        """Fetch an entry from the REST API, using the fetch route denoted by self::_fetchRoute"""
        logger.debug("FETCHING ITEM")
        res = self.connection.make_request(
            self.connection.routes[self._fetchRoute()][1].format(
                self.endpoint, *self._fetchArgs()
            ),
            self._fetchRoute(),
            self._fetchParams(),
        )
        return res


class RestResourceList(OrderedDict, RestResource):
    """
    Base class for REST API responses representing a paged list of items.

    Inherits OrderedDict to keep an internal dict of RestResourceItems when iterrating, and a separate cache dict to avoid
    re-fetching individual items.
    """

    _pageSize = 10
    _pageCount = 1
    _currentPage = 0
    _cache = OrderedDict()

    def __init__(self, parent, pageSize=10):
        logger.debug("Initing RestResourceList object " + str(type(self)))
        super(OrderedDict, self).__init__()
        super(RestResource, self).__init__()
        self._parent = parent
        self._pageSize = pageSize

    def refresh(self):
        """Clear the internal dict, the cache dict, and reset paging"""
        self.clear()
        self._cache.clear()
        self._currentPage = 0
        self._pageCount = 1
        return self

    @abc.abstractmethod
    def _addRoute(self) -> str:
        """Abstract method to be implemented by subclasses, to denote the REST API route for POST requests

        Should return the key from the parent service object route dict, that corresponds to the REST route
        """
        return ""

    @abc.abstractmethod
    def _addArgs(self) -> list:
        """Abstract method to be implemented by subcasses, to provide values for params on the POST REST route"""
        return []

    @abc.abstractmethod
    def _fetchRoute(self) -> str:
        """Abstract method to be implemented by subcasses, to denote the REST API route for GET requests

        Should return the key from the parent service object route dict, that corresponds to the REST route
        """
        return ""

    @abc.abstractmethod
    def _fetchArgs(self) -> list:
        """Abstract method to be implemented by subcasses, to provide values for params on the GET REST route"""
        return []

    @abc.abstractmethod
    def _createChild(self, data: dict):
        """Abstract method to be implemented by subclasses, to create the appropriate RestResourceItem instance"""
        #return RestResourceItem(self, {})
        raise Exception("Operation not supported or not implemented")

    def _fetch(self):
        """Fetch results from the REST API, using the fetch route denoted by self::_fetchRoute

        Will fetch up to self::_pageSize results each time, keeping track of the current page of results in self::_currentPage
        """
        logger.debug("FETCHING LIST")
        res = self.connection.make_request(
            self.connection.routes[self._fetchRoute()][1].format(
                self.endpoint, *self._fetchArgs()
            ),
            self._fetchRoute(),
#            params={"page": self._currentPage + 1},
        )
        # hardcode pageCount to 1, as the API does not support paging
        self._pageCount = 1
        # Create a RestResourceItem for each JSON object in the response, and add it to the internal dict
        if self.dataRoot is None:
            dataRoot = res
        else:
            dataRoot = res[self.dataRoot]
        for i in dataRoot:
            self.update({i[self.idName]: self._createChild(i)})
        self._currentPage += 1

    def __iter__(self):
        """Iterate over all results, using self::_fetch for each page"""
        self._currentPage = 0
        logger.debug("ITERING")
        while self._currentPage < self._pageCount:
            self._fetch()
            logger.debug(
                "PAGE " + str(self._currentPage) + " of " + str(self._pageCount)
            )
            for i, j in enumerate(self.items()):
                if i >= (self._currentPage - 1) * self._pageSize:
                    yield j[1]
        logger.debug("EOD")

    def __getitem__(self, id):
        """
        OrderedDict __getitem__ override.

        Checks if the internal dict has an item with the requested id, from an iteration.
        If not, check the cache. If there's no such item, attempt a fetch request and cache the item
        upon success
        """
        if isinstance(id, int):
            item = list(self)[id]
        else:
            item = super(OrderedDict, self).get(id)
            if item is None:
                item = self._cache.get(id)
                if item is None:
                    item = self._createChild({"__fetch__": id})
                    if item is not None:
                        self._cache.update({getattr(item, self.idName): item})
        return item

    def get(self, id, default=None):
        """OrderedDict get override. Calls __getitem__ but ignores errors and returns default value on failures, instead"""
        tmp = None
        try:
            tmp = self.__getitem__(id)
        finally:
            return tmp or default

    def add(self, item: Union[RestResourceItem, dict, str]):
        """
        Creates a new subresource under the resource list

        This will issue an API request using the endpoint specified by the _addRoute property, posting a JSON representation of the given item.
        If the request succeedes, the appropriate RestResourceItem subclassed object will be returned, populated with the response's data
        """
        if self._addRoute != "":
            if isinstance(item, RestResourceItem):
                body = str(item)
            elif isinstance(item, dict):
                body = json.dumps(item)
            else:
                body = item
            res = self.connection.make_request(
                self.connection.routes[self._addRoute()][1].format(
                    self.endpoint, *self._addArgs()
                ),
                self._addRoute(),
                body=body,
            )
            ret = self._createChild(res)
            return ret
        else:
            raise Exception("Operation not supported or not implemented")

    def __str__(self):
        return "[{0}]".format(", ".join([str(x) for x in list(self)]))
