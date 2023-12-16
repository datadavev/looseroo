"""
FastAPI interface to hopper.

Service to report on the redirect hops needed to reach the
resource identified by a URL.
"""
import logging
import os
import sys
import urllib.parse
import fastapi
import fastapi.middleware.cors
import fastapi.staticfiles
import json_logging
import starlette.responses

import hopper

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

app = fastapi.FastAPI(
    title="Hopper",
    description=__doc__,
    version=hopper.__version__,
    contact={"name": "Dave Vieglais", "url": "https://github.com/datadavev/looseroo"},
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/mit/",
    },
    openapi_url="/api/v1/openapi.json",
    docs_url="/api",
)
logger = logging.getLogger("roo")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))

try:
    json_logging.init_fastapi(enable_json=True)
    json_logging.init_request_instrument(app)
except RuntimeError:
    logger.warning("json_logging already initialized.")

# Enables CORS for UIs on different domains
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "HEAD",
    ],
    allow_headers=[
        "*",
    ],
)

app.mount(
    "/static",
    fastapi.staticfiles.StaticFiles(directory=os.path.join(BASE_FOLDER, "static")),
    name="static",
)


@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    raise fastapi.HTTPException(status_code=404, detail="Not found")


@app.get("/", include_in_schema=False)
def get_api():
    logging.info("get /")
    return starlette.responses.FileResponse(
        os.path.join(BASE_FOLDER, "static/index.html")
    )
    #return fastapi.responses.RedirectResponse(url="/api")


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
    return hopper.follow_redirects(
        url, accept=accept, user_agent=user_agent, method=method
    )


@app.get(
    "/{url:path}",
    summary="Follow redirects for provided URL.",
    response_model=hopper.Hops,
)
def get_hops(
    request: fastapi.Request,
    url: str,
    accept: str = None,
    user_agent: str = None,
    method: str = None,
):
    logger.info("URL = %s", url)
    if url.lower().startswith("http"):
        return do_hops(request, url, accept, user_agent, method)
    return hopper.Hops(
        hops=[],
        start_url=url,
        message="Unsupported target",
    )
