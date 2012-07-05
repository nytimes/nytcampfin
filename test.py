import datetime
import json
import os
import time
import unittest
import requests

from nytcampfin import NytCampfin, NytCampfinError, NytNotFoundError

CURRENT_CYCLE = 2012
API_KEY = os.environ['NYT_CAMPFIN_API_KEY']

class APITest(unittest.TestCase):
    
    def check_response(self, result, url, parse=lambda r: r['results']):
        response = requests.get(url)
        if parse and callable(parse):
            response = parse(response.json)
        self.assertEqual(result, response)
    
    def setUp(self):
        self.finance = NytCampfin(API_KEY)
    
class FilingTest(APITest):

    def test_todays_filings(self):
        today = self.finance.filings.today(offset=20)
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/filings.json?api-key=%s&offset=20" % API_KEY
        self.check_response(today, url)
        
    def test_filings_for_date(self):
        july4th = self.finance.filings.date(2012,07,04)
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/filings/2012/07/04.json?api-key=%s" % API_KEY
        self.check_response(july4th, url)
    
    def test_form_types(self):
        form_types = self.finance.filings.form_types()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/filings/types.json?api-key=%s" % API_KEY
        self.check_response(form_types, url)
        
    def test_filings_by_form_type(self):
        f2s = self.finance.filings.by_type('F2')
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/filings/types/f2.json?api-key=%s" % API_KEY
        self.check_response(f2s, url)
    
    def test_amended_filings(self):
        amendments = self.finance.filings.amendments()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/filings/amendments.json?api-key=%s" % API_KEY
        self.check_response(amendments, url)

class CommitteeTest(APITest):
    
    def test_latest(self):
        latest = self.finance.committees.latest()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/new.json?api-key=%s" % API_KEY
        self.check_response(latest, url)
    
    def test_detail(self):
        detail = self.finance.committees.get("C00490045")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/C00490045.json?api-key=%s" % API_KEY
        response = requests.get(url)
        parse=lambda r: r['results']
        results = parse(response.json)[0]
        self.assertEqual(detail['total_receipts'], results['total_receipts'])

    def test_filter(self):
        hallmark = self.finance.committees.filter("Hallmark")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/search.json?api-key=%s&query=Hallmark" % API_KEY
        self.check_response(hallmark, url)

    def test_contributions(self):
        contributions = self.finance.committees.contributions("C00381277")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/C00381277/contributions.json?api-key=%s" % API_KEY
        self.check_response(contributions, url)
    
    def test_filings(self):
        filings = self.finance.committees.filings("C00490045")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/C00490045/filings.json?api-key=%s" % API_KEY
        self.check_response(filings, url)
        
    

if __name__ == "__main__":
    unittest.main()