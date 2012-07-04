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
        today = self.finance.filings.today()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/filings.json?api-key=%s" % API_KEY
        self.check_response(today, url)
        
    def test_filings_for_date(self):
        july4th = self.finance.filings.date(2012,07,04)
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/filings/2012/07/04.json?api-key=%s" % API_KEY
        self.check_response(july4th, url)
    
    def test_form_types(self):
        form_types = self.finance.filings.form_types()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/filings/types.json?api-key=%s" % API_KEY
        self.check_response(form_types, url)

if __name__ == "__main__":
    unittest.main()