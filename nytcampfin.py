"""
A Python client for the New York Times Campaign Finance API
"""
__author__ = "Derek Willis (dwillis@nytimes.com)"
__version__ = "0.4.0"

import os
import requests
import requests_cache

__all__ = ('NytCampfin', 'NytCampfinError', 'NytNotFoundError')

DEBUG = False

CURRENT_CYCLE = 2012

requests_cache.configure(expire_after=5)

# Error classes

class NytCampfinError(Exception):
    """
    Exception for New York Times Campaign Finance API errors
    """

class NytNotFoundError(NytCampfinError):
    """
    Exception for things not found
    """

# Clients

class Client(object):
        
    BASE_URI = "http://api.nytimes.com/svc/elections/us/v3/finances"
    
    def __init__(self, apikey):
        self.apikey = apikey
    
    def fetch(self, path, *args, **kwargs):
        if not kwargs['offset']:
            kwargs['offset'] = 0
        parse = kwargs.pop('parse', lambda r: r['results'][0])
        kwargs['api-key'] = self.apikey

        if not path.lower().startswith(self.BASE_URI):
            url = self.BASE_URI + "%s.json" % path
            url = (url % args)
        else:
            url = path + '?'
        
        resp = requests.get(url, params = dict(kwargs))
        if not resp.status_code in (200, 304):
            content = resp.json
            errors = '; '.join(e for e in content['errors'])
            if resp.status_code == 404:
                raise NytNotFoundError(errors)
            else:
                raise NytCampfinError(errors)
        
        result = resp.json
        
        if callable(parse):
            result = parse(result)
            if DEBUG:
                result['_url'] = url
        return result

class FilingsClient(Client):
    
    def today(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns today's FEC electronic filings"
        path = "/%s/filings"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result
    
    def date(self, year, month, day, cycle=CURRENT_CYCLE, offset=0):
        "Returns electronic filings for a given date"
        path = "/%s/filings/%s/%s/%s"
        result = self.fetch(path, cycle, year, month, day, offset=offset, parse=lambda r: r['results'])
        return result
    
    def form_types(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns an array of filing form types"
        path = "/%s/filings/types"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result
        
    def by_type(self, form_type, cycle=CURRENT_CYCLE, offset=0):
        "Returns an array of electronic filings for a given form type"
        path = "/%s/filings/types/%s"
        result = self.fetch(path, cycle, form_type, offset=offset, parse=lambda r: r['results'])
        return result        
    
    def amendments(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns an array of recent amendments"
        path = "/%s/filings/amendments"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result
        
class IndependentExpenditureClient(Client):
    
    def latest(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns latest received independent expenditures"
        path = "/%s/independent_expenditures"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result

    def date(self, year, month, day, cycle=CURRENT_CYCLE, offset=0):
        "Returns independent expenditures made on a given date"
        path = "/%s/independent_expenditures/%s/%s/%s"
        result = self.fetch(path, cycle, year, month, day, offset=offset, parse=lambda r: r['results'])
        return result

    def committee(self, cmte_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of a committee's independent expenditures within a cycle"
        path = "/%s/committees/%s/independent_expenditures"
        result = self.fetch(path, cycle, cmte_id, offset=offset, parse=lambda r: r['results'])
        return result

    def candidate(self, cand_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of independent expenditures about a candidate within a cycle"
        path = "/%s/candidates/%s/independent_expenditures"
        result = self.fetch(path, cycle, cand_id, offset=offset, parse=lambda r: r['results'])
        return result

    def president(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of independent expenditures about presidential candidates within a cycle"
        path = "/%s/president/independent_expenditures"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result

    def superpacs(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of independent expenditures about presidential candidates within a cycle"
        path = "/%s/committees/superpacs"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result
        
    def race_totals(self, office, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of races and the total amount of independent expenditures for the cycle"
        path = "/%s/independent_expenditures/race_totals/%s"
        result = self.fetch(path, cycle, office, offset=offset, parse=lambda r: r['results'])
        return result

class CandidatesClient(Client):
    
    def latest(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns newly registered candidates"
        path = "/%s/candidates/new"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result
        
    def get(self, cand_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns details for a single candidate within a cycle"
        path = "/%s/candidates/%s"
        result = self.fetch(path, cycle, cand_id, offset=offset)
        return result

    def filter(self, query, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of candidates based on a search term"
        path = "/%s/candidates/search"
        result = self.fetch(path, cycle, query=query, offset=offset, parse=lambda r: r['results'])
        return result
        
    def late_contributions(self, cand_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of 48-hour contributions to the given candidate"
        path = "/%s/candidates/%s/48hour"
        result = self.fetch(path, cycle, cand_id, offset=offset, parse=lambda r: r['results'])
        return result
    
    def leaders(self, category, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of leading candidates in a given category"
        path = "/%s/candidates/leaders/%s"
        result = self.fetch(path, cycle, category, offset=offset, parse=lambda r: r['results'])
        return result
    
    def seats(self, state, chamber=None, district=None, cycle=CURRENT_CYCLE, offset=0):
        "Returns an array of candidates for seats in the specified state and optional chamber and district"
        if district:
            path = "/%s/seats/%s/%s/%s"
            result = self.fetch(path, cycle, state, chamber, district, offset=offset, parse=lambda r: r['results'])
        elif chamber:
            path = "/%s/seats/%s/%s"
            result = self.fetch(path, cycle, state, chamber, offset=offset, parse=lambda r: r['results'])
        else:
            path = "/%s/seats/%s"
            result = self.fetch(path, cycle, state, offset=offset, parse=lambda r: r['results'])
        return result

class CommitteesClient(Client):
    
    def latest(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns newly registered committees"
        path = "/%s/committees/new"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result
    
    def get(self, cmte_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns details for a single committee within a cycle"
        path = "/%s/committees/%s"
        result = self.fetch(path, cycle, cmte_id, offset=offset)
        return result
    
    def filter(self, query, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of committees based on a search term"
        path = "/%s/committees/search"
        result = self.fetch(path, cycle, query=query, offset=offset, parse=lambda r: r['results'])
        return result

    def late_contributions(self, cmte_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of 48-hour contributions to the given candidate committee"
        path = "/%s/committees/%s/48hour"
        result = self.fetch(path, cycle, cmte_id, offset=offset, parse=lambda r: r['results'])
        return result

    def filings(self, cmte_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of a committee's filing within a cycle"
        path = "/%s/committees/%s/filings"
        result = self.fetch(path, cycle, cmte_id, offset=offset, parse=lambda r: r['results'])
        return result

    def contributions(self, cmte_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of a committee's contributions within a cycle"
        path = "/%s/committees/%s/contributions"
        result = self.fetch(path, cycle, cmte_id, offset=offset, parse=lambda r: r['results'])
        return result

    def contributions_to_candidate(self, cmte_id, candidate_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of a committee's contributions to a given candidate within a cycle"
        path = "/%s/committees/%s/contributions/candidates/%s"
        result = self.fetch(path, cycle, cmte_id, candidate_id, offset=offset, parse=lambda r: r['results'])
        return result
        
    def ie_totals(self, cmte_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of races where the given committee has done independent expenditures"
        path = "/%s/committees/%s/independent_expenditures/races"
        result = self.fetch(path, cycle, cmte_id, offset=offset, parse=lambda r: r['results'])
        return result
        
    def leadership(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of leadership committees"
        path = "/%s/committees/leadership"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result

class PresidentClient(Client):
    
    def candidates(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns a list of presidential candidates with top-level totals"
        path = "/%s/president/totals"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result
    
    def detail(self, candidate_id, cycle=CURRENT_CYCLE, offset=0):
        "Returns financial details for a presidential candidate, using either FEC committee ID or last name as a param"
        path = "/%s/president/candidates/%s"
        result = self.fetch(path, cycle, candidate_id, offset=offset)
        return result
    
    def state(self, state_abbrev, cycle=CURRENT_CYCLE, offset=0):
        "Returns state totals for presidential candidates"
        path = "/%s/president/states/%s"
        result = self.fetch(path, cycle, state_abbrev, offset=offset, parse=lambda r: r['results'])
        return result
    
    def zipcode(self, zipcode, cycle=CURRENT_CYCLE, offset=0):
        "Returns zip code totals for presidential candidates"
        path = "/%s/president/zips/%s"
        result = self.fetch(path, cycle, zipcode, offset=offset, parse=lambda r: r['results'])
        return result

class LateContributionClient(Client):
    
    def latest(self, cycle=CURRENT_CYCLE, offset=0):
        "Returns most recent 48-hour contributions"
        path = "/%s/contributions/48hour"
        result = self.fetch(path, cycle, offset=offset, parse=lambda r: r['results'])
        return result
    
    def date(self, year, month, day, cycle=CURRENT_CYCLE, offset=0):
        "Returns 48-hour contributions made on a given date"
        path = "/%s/contributions/48hour/%s/%s/%s"
        result = self.fetch(path, cycle, year, month, day, offset=offset, parse=lambda r: r['results'])
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
    variable and pass that in.

    NytCampfin uses requests and the requests-cache library. By default,
    it uses a sqlite database named cache.sqlite, but other cache options
    may be used.
    """
    
    def __init__(self, apikey):
        super(NytCampfin, self).__init__(apikey)
        self.filings = FilingsClient(self.apikey)
        self.committees = CommitteesClient(self.apikey)
        self.candidates = CandidatesClient(self.apikey)
        self.president = PresidentClient(self.apikey)
        self.indexp = IndependentExpenditureClient(self.apikey)
        self.late_contribs = LateContributionClient(self.apikey)

