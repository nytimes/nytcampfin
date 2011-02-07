"""
A Python client for the New York Times Campaign Finance API
"""
__author__ = "Derek Willis (dwillis@gmail.com)"
__version__ = "0.1.0"

import datetime
import httplib2
import os
import urllib

try:
    import json
except ImportError:
    import simplejson as json

__all__ = ('NytCampfin', 'NytCampfinError', 'NytNotFoundError')

DEBUG = False

CURRENT_CYCLE = 2012

# Error classes

class NytCampfinError(Exception):
    """
    Exception for New York Times Congress API errors
    """

class NytNotFoundError(NytCampfinError):
    """
    Exception for things not found
    """

# Clients

class Client(object):
    
    BASE_URI = "http://api.nytimes.com/svc/elections/us/v3/finances"
    
    def __init__(self, apikey, cache='.cache'):
        self.apikey = apikey
        self.http = httplib2.Http(cache)
    
    def fetch(self, path, *args, **kwargs):
        parse = kwargs.pop('parse', lambda r: r['results'][0])
        kwargs['api-key'] = self.apikey
        
        if not path.lower().startswith(self.BASE_URI):
            url = self.BASE_URI + "%s.json?" % path
            url = (url % args) + urllib.urlencode(kwargs)
        else:
            url = path + '?' + urllib.urlencode(kwargs)
        
        resp, content = self.http.request(url)
        if not resp.status in (200, 304):
            content = json.loads(content)
            errors = '; '.join(e['error'] for e in content['errors'])
            if resp.status == 404:
                raise NytNotFoundError(errors)
            else:
                raise NytCampfinError(errors)
        
        result = json.loads(content)
        
        if callable(parse):
            result = parse(result)
            if DEBUG:
                result['_url'] = url
        return result

class FilingsClient(Client):

    def today(self, cycle=CURRENT_CYCLE):
        "Returns today's FEC electronic filings"
        path = "/%s/filings"
        result = self.fetch(path, cycle, parse=lambda r: r['results'])
        return result

class NytCampfin(Client):
    """
    Implements the public interface for the NYT Campaign Finance API

    Methods are namespaced by topic (though some have multiple access points).
    Everything returns decoded JSON, with fat trimmed.

    In addition, the top-level namespace is itself a client, which
    can be used to fetch generic resources, using the API URIs included
    in responses. This is here so you don't have to write separate
    functions that add on your API key and trim fat off responses.

    Create a new instance with your API key, or set an environment
    variable called NYT_CAMPFIN_API_KEY.

    NytCampfin uses httplib2, and caching is pluggable. By default,
    it uses httplib2.FileCache, in a directory called .cache, but it
    should also work with memcache or anything else that exposes the
    same interface as FileCache (per httplib2 docs).
    """

    def __init__(self, apikey=os.environ.get('NYT_CAMPFIN_API_KEY'), cache='.cache'):
        super(NytCampfin, self).__init__(apikey, cache)
        self.filings = FilingsClient(self.apikey, cache)

