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
    
    def check_response(self, result, url, parse=lambda r: r['results'][0]):
        
        response = requests.get(url, params = dict(kwargs))
        
        if parse and callable(parse):
            response = parse(response)
        
        self.assertEqual(result, response)
    
    def setUp(self):
        self.finance = NytCampfin(API_KEY)
    
class FilingTest(APITest):

    def test_todays_filings(self):
        today = self.finance.filing.today()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/filings.json?api-key=%s" % API_KEY
        self.check_response(today, url)
