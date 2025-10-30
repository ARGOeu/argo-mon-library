#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from datetime import datetime

from argo_mon_library import ArgoMonitoringService

if __name__ == "__main__":
    parser = ArgumentParser(description="Simple Argo Monitoring metric fetch example")
    parser.add_argument(
        "--host",
        type=str,
        default="api.devel.mon.argo.grnet.gr",
        help="FQDN of Argo Monitoring Service",
    )
    parser.add_argument("--api-key", type=str, required=True, help="API key")
    parser.add_argument(
        "-f",
        help="treat the API key argument as a path to a file holding the key",
        action="store_true",
    )
    parser.add_argument(
        "--endpoint", type=str, required=True, help="endpoint for metric results"
    )
    parser.add_argument(
        "--status", type=str, help="optional status filter (CRITICAL, WARNING, etc)"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="optional date for issues, in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--metric",
        type=str,
        help="filter detailed info to a specific metric",
    )
    parser.add_argument(
        "--timestamp",
        type=str,
        help="filter detailed info for a specific timestamp, in zulu time format",
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

    timestamp = None
    if args.timestamp is not None:
        try:
            timestamp = datetime.strptime(args.timestamp, "%Y-%m-%dT%H:%M:%SZ")
        except Exception as e:
            print("Cannot parse timestamp parameter. Error:", str(e))
            exit(1)

    if args.date is None:
        args.date = datetime.today().strftime("%Y-%m-%d")
    mon = ArgoMonitoringService(args.host, api_key)
    try:
        metric_results = mon.period(datetime.strptime(args.date, "%Y-%m-%d")).metric_results(
                args.endpoint,
                args.metric or None,
                args.timestamp or None
                )
        for i in metric_results:
            print(i)
    except Exception as e:
        print("Error while fetching metric results:", str(e))
