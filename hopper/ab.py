import argparse
import dataclasses
import json
import sys
import hopper
import logging

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(
        prog="ab", description="Compare redirect from two targets"
    )
    parser.add_argument("url", nargs=2, help="URL to dereference.")
    parser.add_argument(
        "-a", "--accept", default=None, help="Accept header value for request"
    )
    parser.add_argument(
        "-u", "--user-agent", default=None, help="User-agent header value for request"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=10.0,
        help="Timeout in seconds for response",
    )
    parser.add_argument(
        "-m", "--method", default="GET", help="HTTP method to use for requests"
    )
    parser.add_argument(
        "-w", "--whitehosts", default=None, help="Follow redirects on these hosts only."
    )
    args = parser.parse_args()
    white_hosts = None
    if args.whitehosts is not None:
        white_hosts = args.whitehosts.split(",")
    results_a = hopper.follow_redirects(
        args.url[0],
        accept=args.accept,
        user_agent=args.user_agent,
        timeout=args.timeout,
        method=args.method,
        white_hosts=white_hosts,
    )
    logging.info(json.dumps(results_a, cls=EnhancedJSONEncoder))
    results_b = hopper.follow_redirects(
        args.url[1],
        accept=args.accept,
        user_agent=args.user_agent,
        timeout=args.timeout,
        method=args.method,
        white_hosts=white_hosts,
    )
    logging.info(json.dumps(results_b, cls=EnhancedJSONEncoder))
    cmp = ["=","="]
    msg = "OK "
    if results_a.final_status != results_b.final_status:
        cmp[1] = "!"
        msg = "ERR"
    if results_a.final_url != results_b.final_url:
        cmp[0] = "!"
        msg = "ERR"
    cmp = "".join(cmp)
    print(f"{msg}: {results_a.final_status} {results_a.final_url} {cmp} {results_b.final_status} {results_b.final_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
