"""
Tests for link header parsing
"""
import pytest
import hopper

test_cases = (
    (
        '</docs/jsonldcontext.jsonld>; rel="alternate"; type="application/ld+json"',
        [
            {
                "url": "/docs/jsonldcontext.jsonld",
                "rel": "alternate",
                "type": "application/ld+json"
            }
        ]
    ),
    (
        '<https://w3id.org/profile/ga-spaceprez>; rel="profile"',
        [
            {
                'url':'https://w3id.org/profile/ga-spaceprez',
                'rel':'profile'
            }
        ]
    ),
    (
        '<https://igsn.rslv.xyz/igsn:AU12434>; rel="canonical", </.info/igsn:10.60516/au12434>; type="application/json"; rel="alternate"; profile="https://igsn.org/info", <https://hdl.handle.net/AU12434/10.60516>; rel="alternate"; profile="https://schema.datacite.org/"',
        [
            {
                "url": "https://igsn.rslv.xyz/igsn:AU12434",
                "rel": "canonical"
            },
            {
                "url": "/.info/igsn:10.60516/au12434",
                "type": "application/json",
                "rel": "alternate",
                "profile": "https://igsn.org/info"
            },
            {
                "url": "https://hdl.handle.net/AU12434/10.60516",
                "rel": "alternate",
                "profile": "https://schema.datacite.org/"
            }
        ]
    ),
    (
        '<https://w3id.org/profile/ga-spaceprez>; rel="profile", <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="prez"; anchor=<https://w3id.org/profile/prez>, <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="profiles"; anchor=<https://w3id.org/profile/>, <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="geo"; anchor=<http://www.opengis.net/ont/geosparql>, <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="oai"; anchor=<https://spec.openapis.org/oas/v3.1.0>, <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="alt"; anchor=<http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile>, <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="dcat"; anchor=<https://w3id.org/profile/dcat2null>, <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="mem"; anchor=<https://w3id.org/profile/mem>, <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="vocpub"; anchor=<https://w3id.org/profile/vocpub>, <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="sdo"; anchor=<https://schema.org>, <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="dd"; anchor=<https://w3id.org/profile/dd>, <http://www.w3.org/ns/dx/prof/Profile>; rel="type"; token="gas"; anchor=<https://w3id.org/profile/ga-spaceprez>, <https://pid.geoscience.gov.au/sample/AU12434?_profile=prez&_mediatype=text/html>; rel="alternate"; type="text/html"; profile="https://w3id.org/profile/prez", <https://pid.geoscience.gov.au/sample/AU12434?_profile=profiles&_mediatype=text/html>; rel="alternate"; type="text/html"; profile="https://w3id.org/profile/", <https://pid.geoscience.gov.au/sample/AU12434?_profile=profiles&_mediatype=application/json>; rel="alternate"; type="application/json"; profile="https://w3id.org/profile/", <https://pid.geoscience.gov.au/sample/AU12434?_profile=geo&_mediatype=text/html>; rel="alternate"; type="text/html"; profile="http://www.opengis.net/ont/geosparql", <https://pid.geoscience.gov.au/sample/AU12434?_profile=geo&_mediatype=text/turtle>; rel="alternate"; type="text/turtle"; profile="http://www.opengis.net/ont/geosparql", <https://pid.geoscience.gov.au/sample/AU12434?_profile=geo&_mediatype=application/rdf+xml>; rel="alternate"; type="application/rdf+xml"; profile="http://www.opengis.net/ont/geosparql", <https://pid.geoscience.gov.au/sample/AU12434?_profile=geo&_mediatype=application/ld+json>; rel="alternate"; type="application/ld+json"; profile="http://www.opengis.net/ont/geosparql", <https://pid.geoscience.gov.au/sample/AU12434?_profile=oai&_mediatype=text/html>; rel="alternate"; type="text/html"; profile="https://spec.openapis.org/oas/v3.1.0", <https://pid.geoscience.gov.au/sample/AU12434?_profile=oai&_mediatype=application/geo+json>; rel="alternate"; type="application/geo+json"; profile="https://spec.openapis.org/oas/v3.1.0", <https://pid.geoscience.gov.au/sample/AU12434?_profile=alt&_mediatype=text/html>; rel="alternate"; type="text/html"; profile="http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile", <https://pid.geoscience.gov.au/sample/AU12434?_profile=alt&_mediatype=text/turtle>; rel="alternate"; type="text/turtle"; profile="http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile", <https://pid.geoscience.gov.au/sample/AU12434?_profile=alt&_mediatype=application/rdf+xml>; rel="alternate"; type="application/rdf+xml"; profile="http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile", <https://pid.geoscience.gov.au/sample/AU12434?_profile=alt&_mediatype=application/json>; rel="alternate"; type="application/json"; profile="http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile", <https://pid.geoscience.gov.au/sample/AU12434?_profile=alt&_mediatype=application/ld+json>; rel="alternate"; type="application/ld+json"; profile="http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile", <https://pid.geoscience.gov.au/sample/AU12434?_profile=dcat&_mediatype=text/html>; rel="alternate"; type="text/html"; profile="https://w3id.org/profile/dcat2null", <https://pid.geoscience.gov.au/sample/AU12434?_profile=dcat&_mediatype=text/turtle>; rel="alternate"; type="text/turtle"; profile="https://w3id.org/profile/dcat2null", <https://pid.geoscience.gov.au/sample/AU12434?_profile=dcat&_mediatype=application/rdf+xml>; rel="alternate"; type="application/rdf+xml"; profile="https://w3id.org/profile/dcat2null", <https://pid.geoscience.gov.au/sample/AU12434?_profile=dcat&_mediatype=application/ld+json>; rel="alternate"; type="application/ld+json"; profile="https://w3id.org/profile/dcat2null", <https://pid.geoscience.gov.au/sample/AU12434?_profile=mem&_mediatype=text/html>; rel="alternate"; type="text/html"; profile="https://w3id.org/profile/mem", <https://pid.geoscience.gov.au/sample/AU12434?_profile=mem&_mediatype=text/turtle>; rel="alternate"; type="text/turtle"; profile="https://w3id.org/profile/mem", <https://pid.geoscience.gov.au/sample/AU12434?_profile=mem&_mediatype=application/rdf+xml>; rel="alternate"; type="application/rdf+xml"; profile="https://w3id.org/profile/mem", <https://pid.geoscience.gov.au/sample/AU12434?_profile=mem&_mediatype=application/json>; rel="alternate"; type="application/json"; profile="https://w3id.org/profile/mem", <https://pid.geoscience.gov.au/sample/AU12434?_profile=mem&_mediatype=application/ld+json>; rel="alternate"; type="application/ld+json"; profile="https://w3id.org/profile/mem", <https://pid.geoscience.gov.au/sample/AU12434?_profile=vocpub&_mediatype=text/html>; rel="alternate"; type="text/html"; profile="https://w3id.org/profile/vocpub", <https://pid.geoscience.gov.au/sample/AU12434?_profile=vocpub&_mediatype=text/turtle>; rel="alternate"; type="text/turtle"; profile="https://w3id.org/profile/vocpub", <https://pid.geoscience.gov.au/sample/AU12434?_profile=vocpub&_mediatype=application/rdf+xml>; rel="alternate"; type="application/rdf+xml"; profile="https://w3id.org/profile/vocpub", <https://pid.geoscience.gov.au/sample/AU12434?_profile=vocpub&_mediatype=application/ld+json>; rel="alternate"; type="application/ld+json"; profile="https://w3id.org/profile/vocpub", <https://pid.geoscience.gov.au/sample/AU12434?_profile=sdo&_mediatype=text/html>; rel="alternate"; type="text/html"; profile="https://schema.org", <https://pid.geoscience.gov.au/sample/AU12434?_profile=sdo&_mediatype=text/turtle>; rel="alternate"; type="text/turtle"; profile="https://schema.org", <https://pid.geoscience.gov.au/sample/AU12434?_profile=sdo&_mediatype=application/rdf+xml>; rel="alternate"; type="application/rdf+xml"; profile="https://schema.org", <https://pid.geoscience.gov.au/sample/AU12434?_profile=sdo&_mediatype=application/ld+json>; rel="alternate"; type="application/ld+json"; profile="https://schema.org", <https://pid.geoscience.gov.au/sample/AU12434?_profile=dd&_mediatype=application/json>; rel="alternate"; type="application/json"; profile="https://w3id.org/profile/dd", <https://pid.geoscience.gov.au/sample/AU12434?_profile=dd&_mediatype=text/csv>; rel="alternate"; type="text/csv"; profile="https://w3id.org/profile/dd", <https://pid.geoscience.gov.au/sample/AU12434?_profile=gas&_mediatype=text/html>; rel="self"; type="text/html"; profile="https://w3id.org/profile/ga-spaceprez", <https://pid.geoscience.gov.au/sample/AU12434?_profile=gas&_mediatype=text/turtle>; rel="alternate"; type="text/turtle"; profile="https://w3id.org/profile/ga-spaceprez", <https://pid.geoscience.gov.au/sample/AU12434?_profile=gas&_mediatype=application/rdf+xml>; rel="alternate"; type="application/rdf+xml"; profile="https://w3id.org/profile/ga-spaceprez", <https://pid.geoscience.gov.au/sample/AU12434?_profile=gas&_mediatype=application/ld+json>; rel="alternate"; type="application/ld+json"; profile="https://w3id.org/profile/ga-spaceprez"',
        [
            {
                "url": "https://w3id.org/profile/ga-spaceprez",
                "rel": "profile"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "prez",
                "anchor": "<https://w3id.org/profile/prez>"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "profiles",
                "anchor": "<https://w3id.org/profile/>"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "geo",
                "anchor": "<http://www.opengis.net/ont/geosparql>"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "oai",
                "anchor": "<https://spec.openapis.org/oas/v3.1.0>"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "alt",
                "anchor": "<http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile>"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "dcat",
                "anchor": "<https://w3id.org/profile/dcat2null>"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "mem",
                "anchor": "<https://w3id.org/profile/mem>"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "vocpub",
                "anchor": "<https://w3id.org/profile/vocpub>"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "sdo",
                "anchor": "<https://schema.org>"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "dd",
                "anchor": "<https://w3id.org/profile/dd>"
            },
            {
                "url": "http://www.w3.org/ns/dx/prof/Profile",
                "rel": "type",
                "token": "gas",
                "anchor": "<https://w3id.org/profile/ga-spaceprez>"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=prez&_mediatype=text/html",
                "rel": "alternate",
                "type": "text/html",
                "profile": "https://w3id.org/profile/prez"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=profiles&_mediatype=text/html",
                "rel": "alternate",
                "type": "text/html",
                "profile": "https://w3id.org/profile/"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=profiles&_mediatype=application/json",
                "rel": "alternate",
                "type": "application/json",
                "profile": "https://w3id.org/profile/"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=geo&_mediatype=text/html",
                "rel": "alternate",
                "type": "text/html",
                "profile": "http://www.opengis.net/ont/geosparql"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=geo&_mediatype=text/turtle",
                "rel": "alternate",
                "type": "text/turtle",
                "profile": "http://www.opengis.net/ont/geosparql"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=geo&_mediatype=application/rdf+xml",
                "rel": "alternate",
                "type": "application/rdf+xml",
                "profile": "http://www.opengis.net/ont/geosparql"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=geo&_mediatype=application/ld+json",
                "rel": "alternate",
                "type": "application/ld+json",
                "profile": "http://www.opengis.net/ont/geosparql"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=oai&_mediatype=text/html",
                "rel": "alternate",
                "type": "text/html",
                "profile": "https://spec.openapis.org/oas/v3.1.0"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=oai&_mediatype=application/geo+json",
                "rel": "alternate",
                "type": "application/geo+json",
                "profile": "https://spec.openapis.org/oas/v3.1.0"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=alt&_mediatype=text/html",
                "rel": "alternate",
                "type": "text/html",
                "profile": "http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=alt&_mediatype=text/turtle",
                "rel": "alternate",
                "type": "text/turtle",
                "profile": "http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=alt&_mediatype=application/rdf+xml",
                "rel": "alternate",
                "type": "application/rdf+xml",
                "profile": "http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=alt&_mediatype=application/json",
                "rel": "alternate",
                "type": "application/json",
                "profile": "http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=alt&_mediatype=application/ld+json",
                "rel": "alternate",
                "type": "application/ld+json",
                "profile": "http://www.w3.org/ns/dx/conneg/altr-ext#alt-profile"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=dcat&_mediatype=text/html",
                "rel": "alternate",
                "type": "text/html",
                "profile": "https://w3id.org/profile/dcat2null"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=dcat&_mediatype=text/turtle",
                "rel": "alternate",
                "type": "text/turtle",
                "profile": "https://w3id.org/profile/dcat2null"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=dcat&_mediatype=application/rdf+xml",
                "rel": "alternate",
                "type": "application/rdf+xml",
                "profile": "https://w3id.org/profile/dcat2null"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=dcat&_mediatype=application/ld+json",
                "rel": "alternate",
                "type": "application/ld+json",
                "profile": "https://w3id.org/profile/dcat2null"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=mem&_mediatype=text/html",
                "rel": "alternate",
                "type": "text/html",
                "profile": "https://w3id.org/profile/mem"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=mem&_mediatype=text/turtle",
                "rel": "alternate",
                "type": "text/turtle",
                "profile": "https://w3id.org/profile/mem"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=mem&_mediatype=application/rdf+xml",
                "rel": "alternate",
                "type": "application/rdf+xml",
                "profile": "https://w3id.org/profile/mem"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=mem&_mediatype=application/json",
                "rel": "alternate",
                "type": "application/json",
                "profile": "https://w3id.org/profile/mem"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=mem&_mediatype=application/ld+json",
                "rel": "alternate",
                "type": "application/ld+json",
                "profile": "https://w3id.org/profile/mem"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=vocpub&_mediatype=text/html",
                "rel": "alternate",
                "type": "text/html",
                "profile": "https://w3id.org/profile/vocpub"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=vocpub&_mediatype=text/turtle",
                "rel": "alternate",
                "type": "text/turtle",
                "profile": "https://w3id.org/profile/vocpub"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=vocpub&_mediatype=application/rdf+xml",
                "rel": "alternate",
                "type": "application/rdf+xml",
                "profile": "https://w3id.org/profile/vocpub"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=vocpub&_mediatype=application/ld+json",
                "rel": "alternate",
                "type": "application/ld+json",
                "profile": "https://w3id.org/profile/vocpub"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=sdo&_mediatype=text/html",
                "rel": "alternate",
                "type": "text/html",
                "profile": "https://schema.org"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=sdo&_mediatype=text/turtle",
                "rel": "alternate",
                "type": "text/turtle",
                "profile": "https://schema.org"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=sdo&_mediatype=application/rdf+xml",
                "rel": "alternate",
                "type": "application/rdf+xml",
                "profile": "https://schema.org"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=sdo&_mediatype=application/ld+json",
                "rel": "alternate",
                "type": "application/ld+json",
                "profile": "https://schema.org"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=dd&_mediatype=application/json",
                "rel": "alternate",
                "type": "application/json",
                "profile": "https://w3id.org/profile/dd"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=dd&_mediatype=text/csv",
                "rel": "alternate",
                "type": "text/csv",
                "profile": "https://w3id.org/profile/dd"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=gas&_mediatype=text/html",
                "rel": "self",
                "type": "text/html",
                "profile": "https://w3id.org/profile/ga-spaceprez"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=gas&_mediatype=text/turtle",
                "rel": "alternate",
                "type": "text/turtle",
                "profile": "https://w3id.org/profile/ga-spaceprez"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=gas&_mediatype=application/rdf+xml",
                "rel": "alternate",
                "type": "application/rdf+xml",
                "profile": "https://w3id.org/profile/ga-spaceprez"
            },
            {
                "url": "https://pid.geoscience.gov.au/sample/AU12434?_profile=gas&_mediatype=application/ld+json",
                "rel": "alternate",
                "type": "application/ld+json",
                "profile": "https://w3id.org/profile/ga-spaceprez"
            }
        ]
    )
)



@pytest.mark.parametrize('link,expected', test_cases)
def test_parse_links(link, expected):
    links = hopper.parse_link_header(link)
    assert len(links) == len(expected)
    for i in range(0, len(expected)):
        assert links[i] == expected[i]
