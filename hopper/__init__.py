import re
import time
import typing

import dataclasses
import httpx

__version__ = "1.0.0"


# A vercel hobby instance can run for 10 seconds
# Change this value if your deployment supports longet connections
DEFAULT_TIMEOUT: float = 9.0

RE_PROTOCOL = re.compile(r"^(https?)(:\/{1})([\w+])", flags=re.IGNORECASE)

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


def fix_url(url):
    return RE_PROTOCOL.sub(r"\1://\3", url)

def follow_redirects(
    url: str,
    accept: typing.Optional[str] = None,
    user_agent: typing.Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> Hops:
    url = fix_url(url)
    headers = {}
    if user_agent is not None:
        headers["User-agent"] = user_agent
    if accept is not None:
        headers["Accept"] = accept
    message = None
    results = Hops(start_url=url, t_ms=0, hops=[], message=message)
    t0 = time.time()
    try:
        max_bytes = 1024 * 500
        received = 0
        with httpx.stream(
            "GET", url, headers=headers, follow_redirects=True, timeout=timeout
        ) as response:
            try:
                for chunk in response.iter_bytes(1024):
                    received += len(chunk)
                    if received > max_bytes:
                        raise ValueError("Max size reached.")
            except ValueError:
                message = "Response terminated at 500k."
                response.close()
            results.t_ms = (time.time() - t0)*1000.0
            results.message = message
            for r in response.history:
                results.hops.append(
                    Hop(
                        url=str(r.url),
                        status=r.status_code,
                        t_ms=r.elapsed.total_seconds() * 1000.0,
                        content_type=r.headers.get("content-type", None),
                        content_length=r.headers.get("content-length", 0),
                    )
                )
            results.hops.append(
                Hop(
                    url=str(response.url),
                    status=response.status_code,
                    t_ms=response.elapsed.total_seconds() * 1000.0,
                    content_type=response.headers.get("content-type", None),
                    content_length=response.headers.get("content-length", 0),
                )
            )
            results.accept = response.request.headers.get("accept", None)
            results.user_agent = response.request.headers.get("user-agent", None)
            results.final_url = str(response.url)
            return results
    except Exception as e:
        results.message = str(e)
        results.t_ms = (time.time() - t0)*1000.0
    return results
