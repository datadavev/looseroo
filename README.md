# looseroo

The loose roo hops along redirects.

```
$ roo --help
usage: roo [-h] [-a ACCEPT] [-u USER_AGENT] [-t TIMEOUT] [-m METHOD] [-w WHITEHOSTS] url

Report on redirect hops when dereferencing a URL

positional arguments:
  url                   URL to dereference.

options:
  -h, --help            show this help message and exit
  -a ACCEPT, --accept ACCEPT
                        Accept header value for request
  -u USER_AGENT, --user-agent USER_AGENT
                        User-agent header value for request
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds for response
  -m METHOD, --method METHOD
                        HTTP method to use for requests
  -w WHITEHOSTS, --whitehosts WHITEHOSTS
                        Follow redirects on these hosts only.
```

or visit:

```
https://hopper.rslv.xyz/
```

or call the api directly:

```
https://hopper.rslv.xyz/http://n2t.net/ark:/65665/3ae126b96-aad8-4681-a8eb-56c7232cf12f
```

```json
{
  "hops": [
    {
      "url": "http://n2t.net/ark:/65665/3ae126b96-aad8-4681-a8eb-56c7232cf12f",
      "status": 302,
      "content_type": "text/html; charset=iso-8859-1",
      "content_length": 262,
      "link": [],
      "t_ms": 135.139
    },
    {
      "url": "http://collections.nmnh.si.edu/id/ark:/65665/3ae126b96aad84681a8eb56c7232cf12f",
      "status": 302,
      "content_type": null,
      "content_length": 0,
      "link": [],
      "t_ms": 98.141
    },
    {
      "url": "https://collections.nmnh.si.edu/id/ark:/65665/3ae126b96aad84681a8eb56c7232cf12f",
      "status": 302,
      "content_type": "text/html; charset=iso-8859-1",
      "content_length": 276,
      "link": [],
      "t_ms": 20.556
    },
    {
      "url": "https://collections.nmnh.si.edu/search/ark/?ark=ark:/65665/3ae126b96aad84681a8eb56c7232cf12f",
      "status": 302,
      "content_type": "text/html; charset=UTF-8",
      "content_length": 0,
      "link": [],
      "t_ms": 27.628
    },
    {
      "url": "https://collections.nmnh.si.edu/search/ento/?ark=ark:/65665/3ae126b96aad84681a8eb56c7232cf12f",
      "status": 200,
      "content_type": "text/html; charset=UTF-8",
      "content_length": 0,
      "link": [],
      "t_ms": 23.825
    }
  ],
  "start_url": "http://n2t.net/ark:/65665/3ae126b96-aad8-4681-a8eb-56c7232cf12f",
  "final_url": "https://collections.nmnh.si.edu/search/ento/?ark=ark:/65665/3ae126b96aad84681a8eb56c7232cf12f",
  "t_ms": 307.53326416015625,
  "message": null,
  "accept": "*/*",
  "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
  "hopper_version": "1.7.0"
}
```
