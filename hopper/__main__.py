"""
Hopper CLI
"""
import argparse
import dataclasses
import json
import sys
import hopper


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def main():
    parser = argparse.ArgumentParser(
        prog="roo", description="Report on redirect hops when dereferencing a URL"
    )
    parser.add_argument("url", help="URL to dereference.")
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
    args = parser.parse_args()
    results = hopper.follow_redirects(
        args.url,
        accept=args.accept,
        user_agent=args.user_agent,
        timeout=args.timeout,
        method=args.method,
    )
    print(json.dumps(results, indent=2, cls=EnhancedJSONEncoder))
    return 0


if __name__ == "__main__":
    sys.exit(main())
