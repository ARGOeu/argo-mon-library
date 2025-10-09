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
        "--report", type=str, required=True, help="report name for issues"
    )
    parser.add_argument(
        "--status", type=str, help="optional status filter (CRITICAL or WARNING)"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="optional date for issues, in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--metrics",
        help="get issues for metrics instead of endpoints",
        action="store_true",
    )
    parser.add_argument(
        "--group",
        type=str,
        required="--metrics" in sys.argv,
        help="group name for metric issues",
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

    if args.date is None:
        args.date = datetime.today().strftime("%Y-%m-%d")
    mon = ArgoMonitoringService(args.host, api_key)
    try:
        crit = 0
        warn = 0
        tot = 0
        crit_issues = []
        warn_issues = []
        if args.metrics:
            issues = (
                mon.period(datetime.strptime(args.date, "%Y-%m-%d"))
                .reports.by_name(args.report)
                .issues.by_metric(args.group, args.status)
            )
        else:
            issues = (
                mon.period(datetime.strptime(args.date, "%Y-%m-%d"))
                .reports.by_name(args.report)
                .issues.by_endpoint(args.status)
            )

        for i in issues:
            tot += 1
            if i.status == "CRITICAL":
                crit += 1
                if args.metrics:
                    crit_issues.append("{0} ({1})".format(i.metric, i.service))
                else:
                    crit_issues.append("{0} ({1})".format(i.url, i.service))
            elif i.status == "WARNING":
                warn += 1
                if args.metrics:
                    warn_issues.append("{0} ({1})".format(i.metric, i.service))
                else:
                    warn_issues.append("{0} ({1})".format(i.url, i.service))

        print(
            "Service {0} with critical issues:".format(
                "metrics" if args.metrics else "endpoints"
            )
        )
        if crit == 0:
            print("  No issues")
        else:
            print("\n".join("  " + str(x) for x in sorted(set(crit_issues))))
        print()

        print(
            "Service {0} with warnings:".format(
                "metrics" if args.metrics else "endpoints"
            )
        )
        if warn == 0:
            print("  No issues")
        else:
            print("\n".join("  " + str(x) for x in sorted(set(warn_issues))))
        print()

        print(
            "Summary:",
            crit,
            "critical issues,",
            warn,
            "warnings",
            "({0} total)".format(tot),
        )
    except Exception as e:
        print("Error while iterating report issues:", str(e))
