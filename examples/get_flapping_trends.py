#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from datetime import datetime

from argo_mon_library import ArgoMonitoringService, FlappingType

if __name__ == "__main__":
    parser = ArgumentParser(description="Simple Argo Monitoring A/R fetch example")
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
    parser.add_argument("--report", type=str, required=True, help="report name")
    parser.add_argument(
        "--start-date",
        type=str,
        help="start date for report results, in YYYY-MM-DD format (default: current date)",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        help="optional end date for report results, in YYYY-MM-DD format (default: same as start date)",
    )
    parser.add_argument(
        "--monthly",
        help="get report results with monthly granularity (default: daily)",
        action="store_true",
    )
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        help="type of flapping trend to fetch (enum: GROUPS, SERVICES, ENDPOINTS, METRICS, METRIC_TAGS)",
    )
    parser.add_argument(
        "--top",
        type=str,
        help="fetch up to TOP number of results"
    )
    parser.add_argument(
        "--ext-tags",
        help="also print metric data when requesting flapping metric tags (otherwise ignored)",
        action="store_true",
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

    if args.start_date is None:
        args.start_date = datetime.today().strftime('%Y-%m-%d')

    if args.end_date is None:
        args.end_date = args.start_date

    flap_type = None
    if args.type == "GROUPS":
        flap_type = FlappingType.GROUPS
    elif args.type == "SERVICES":
        flap_type = FlappingType.SERVICES
    elif args.type == "ENDPOINTS":
        flap_type = FlappingType.ENDPOINTS
    elif args.type == "METRICS":
        flap_type = FlappingType.METRICS
    elif args.type == "METRIC_TAGS":
        flap_type = FlappingType.METRIC_TAGS
    else:
        print("Unsupported flapping trend type '{0}'".format(args.type), file=sys.stderr)
        exit(1)

    max_res = 0
    if args.top:
        try:
            max_res = int(args.top)
        except Exception as e:
            print("Invalid value for 'top' parameter", str(e), file=sys.stderr)

    try:
        mon = ArgoMonitoringService(args.host, api_key)
        trends = (
            mon.period(
                datetime.strptime(args.start_date, "%Y-%m-%d"),
                datetime.strptime(args.end_date, "%Y-%m-%d"),
                granularity="monthly" if args.monthly else "daily",
            )
            .reports.by_name(args.report)
            .trends
            .flapping(flap_type, max_res)
        )
        for i in trends:
            print(i)
            if flap_type == FlappingType.METRIC_TAGS and args.ext_tags:
                for m in i.metrics:
                    print("  ", m)
    except Exception as e:
        print("Error while iterating report results:", str(e))
