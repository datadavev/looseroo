"""
This module implements FastAPI routes for hopper.

This module may be used in other FastAPI applications to provide hopper functionality.
"""

import logging
import urllib.parse
import fastapi

from . import (Hops, follow_redirects)

logger = logging.getLogger("hopper")

router = fastapi.APIRouter(
    tags=["hopper", ]
)


def do_hops(
    request: fastapi.Request,
    url: str,
    accept: str = None,
    user_agent: str = None,
    method: str = None,
):
    if accept is None:
        accept = request.headers.get("accept", None)
    if user_agent is None:
        user_agent = request.headers.get("user-agent", None)
    if method is None:
        method = request.method
    url = urllib.parse.unquote(url)
    return follow_redirects(
        url, accept=accept, user_agent=user_agent, method=method
    )


@router.get(
    "/{url:path}",
    summary="Follow redirects for provided URL.",
    response_model=Hops,
)
async def get_hops(
    request: fastapi.Request,
    url: str,
    accept: str = None,
    user_agent: str = None,
    method: str = None,
):
    logger.info("URL = %s", url)
    if url.lower().startswith("http"):
        return do_hops(request, url, accept, user_agent, method)
    return Hops(
        hops=[],
        start_url=url,
        message="Target is not a http url.",
    )
