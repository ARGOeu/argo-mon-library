#!/usr/bin/env python

from argparse import ArgumentParser
from argo_mon_library import ArgoMonitoringService
from datetime import datetime
import sys
import json

if __name__ == "__main__":
    parser = ArgumentParser(description="Simple Argo Monitoring metric fetch example")
    parser.add_argument(
        "--host",
        type=str,
        default="api.devel.mon.argo.grnet.gr",
        help="FQDN of Argo Monitoring Service",
    )
    parser.add_argument(
        "--api-key", type=str, required=True, help="API key"
    )
    parser.add_argument(
        "-f",
        help="treat the API key argument as a path to a file holding the key",
        action="store_true",
    )
    parser.add_argument(
        "--report", type=str, required=True, help="report name"
    )
    parser.add_argument(
        "--date", type=str, required=True, help="effective date for report status, in YYYY-MM-DD format"
    )
    args = parser.parse_args()

    if args.f:
        try:
            with open(args.api_key, "r") as keyfile:
                api_key = keyfile.read()
        except Exception as e:
            print("Error while reading API key from file:", str(e), file=sys.stderr)
            exit(1)
    else:
        api_key = args.api_key

    try:
        mon = ArgoMonitoringService(args.host, api_key)
        for group in mon.period(datetime.strptime(args.date, "%Y-%m-%d")).reports.byName(args.report).status.groups:
            for endpoint in group.endpoints:
                for status in endpoint.statuses:
                    print(group.name, endpoint.id, status.timestamp, status.value)
    except Exception as e:
        print("Error while iterating report status groups:", str(e))
