# looseroo

The loose roo hops along redirects.

```
$ roo --help
usage: roo [-h] [-a ACCEPT] [-u USER_AGENT] [-t TIMEOUT] [-m METHOD] url

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
                        HTTP method to use for requests```
```

or visit:

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
      "content_length": "262",
      "t_ms": 134.613
    },
    {
      "url": "http://collections.nmnh.si.edu/id/ark:/65665/3ae126b96aad84681a8eb56c7232cf12f",
      "status": 302,
      "content_type": null,
      "content_length": "0",
      "t_ms": 5.282
    },
    {
      "url": "https://collections.nmnh.si.edu/id/ark:/65665/3ae126b96aad84681a8eb56c7232cf12f",
      "status": 302,
      "content_type": "text/html; charset=iso-8859-1",
      "content_length": "276",
      "t_ms": 15.663
    },
    {
      "url": "https://collections.nmnh.si.edu/search/ark/?ark=ark:/65665/3ae126b96aad84681a8eb56c7232cf12f",
      "status": 302,
      "content_type": "text/html; charset=UTF-8",
      "content_length": "0",
      "t_ms": 23.425
    },
    {
      "url": "https://collections.nmnh.si.edu/search/ento/?ark=ark:/65665/3ae126b96aad84681a8eb56c7232cf12f",
      "status": 200,
      "content_type": "text/html; charset=UTF-8",
      "content_length": 0,
      "t_ms": 16.764000000000003
    }
  ],
  "start_url": "http://n2t.net/ark:/65665/3ae126b96-aad8-4681-a8eb-56c7232cf12f",
  "final_url": "https://collections.nmnh.si.edu/search/ento/?ark=ark:/65665/3ae126b96aad84681a8eb56c7232cf12f",
  "t_ms": 204.29182052612305,
  "message": null,
  "accept": "*/*",
  "user_agent": "curl/8.1.2",
  "version": "1.0.0"
}
```
