import re
import time
import typing

import dataclasses
import httpx

__version__ = "1.3.0"


# A vercel hobby instance can run for 10 seconds
# Change this value if your deployment supports longet connections
DEFAULT_TIMEOUT: float = 9.0

# The default http method to use for requests.
DEFAULT_METHOD = "GET"

# Pattern to match a http or https url
RE_PROTOCOL = re.compile(r"^(https?)(:\/{1})([\w+])", flags=re.IGNORECASE)

HTTP_METHODS = ("GET", "HEAD", "POST", "PUT")


@dataclasses.dataclass
class Hop:
    url: str
    status: int
    content_type: typing.Optional[str] = None
    content_length: int = 0
    t_ms: float = 0


@dataclasses.dataclass
class Hops:
    hops: typing.List[Hop]
    start_url: str
    final_url: typing.Optional[str] = None
    t_ms: float = 0
    message: typing.Optional[str] = None
    accept: typing.Optional[str] = None
    user_agent: typing.Optional[str] = None
    hopper_version: str = __version__


def fix_url(url):
    return RE_PROTOCOL.sub(r"\1://\3", url)


def follow_redirects(
    url: str,
    accept: typing.Optional[str] = None,
    user_agent: typing.Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
    method: str = DEFAULT_METHOD,
    white_hosts: typing.Optional[list[str]] = None,
) -> Hops:
    if white_hosts is None:
        white_hosts = []
    url = fix_url(url)
    headers = {}
    if user_agent is not None:
        headers["User-agent"] = user_agent
    if accept is not None:
        headers["Accept"] = accept
    message = None
    results = Hops(start_url=url, t_ms=0, hops=[], message=message)
    method = method.strip().upper()
    if method not in HTTP_METHODS:
        results.message = f"Error: method must be one of {', '.join(HTTP_METHODS)}"
        return results
    with httpx.Client(timeout=timeout, max_redirects=0) as client:
        t0 = time.time()
        more_work = True
        try:
            while more_work:
                with client.stream(method, url, headers=headers, follow_redirects=False, timeout=timeout) as response:
                    response.close()
                    results.hops.append(
                        Hop(
                            url=str(response.url),
                            status=response.status_code,
                            t_ms=response.elapsed.total_seconds() * 1000.0,
                            content_type=response.headers.get("content-type", None),
                            content_length=response.headers.get("content-length", 0),
                        )
                    )
                if response.next_request is not None:
                    url = response.next_request.url
                else:
                    url = response.url
                    more_work = False
                results.accept = response.request.headers.get("accept", None)
                results.user_agent = response.request.headers.get("user-agent", None)
                results.final_url = str(url)
                if (len(white_hosts) > 0)  and (url.host not in white_hosts):
                    results.message = "Redirection terminate by host not listed in white hosts."
                    break

            results.t_ms = (time.time() - t0) * 1000.0
        except Exception as e:
            results.message = str(e)
            results.t_ms = (time.time() - t0) * 1000.0
    return results
