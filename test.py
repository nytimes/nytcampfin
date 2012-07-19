import os
import unittest
import requests
import requests_cache

from nytcampfin import NytCampfin, NytCampfinError, NytNotFoundError

CURRENT_CYCLE = 2012
API_KEY = os.environ['NYT_CAMPFIN_API_KEY']

class APITest(unittest.TestCase):
    
    def check_response(self, result, url, parse=lambda r: r['results']):
        with requests_cache.disabled(): # test requests should not be cached
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

class IndependentExpenditureTest(APITest):
    
    def test_latest(self):
        latest = self.finance.indexp.latest()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/independent_expenditures.json?api-key=%s" % API_KEY
        self.check_response(latest, url)
    
    def test_ies_for_date(self):
        july3rd = self.finance.indexp.date(2012,07,03)
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/independent_expenditures/2012/07/03.json?api-key=%s" % API_KEY
        self.check_response(july3rd, url)

    def test_committee_ies(self):
        ies = self.finance.indexp.committee("C00490045")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/C00490045/independent_expenditures.json?api-key=%s" % API_KEY
        self.check_response(ies, url)
        
    def test_race_totals(self):
        races = self.finance.indexp.race_totals("president")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/independent_expenditures/race_totals/president.json?api-key=%s" % API_KEY
        self.check_response(races, url)

    def test_candidate_ies(self):
        ies = self.finance.indexp.candidate("P00003608")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/candidates/P00003608/independent_expenditures.json?api-key=%s" % API_KEY
        self.check_response(ies, url)

    def test_president_ies(self):
        ies = self.finance.indexp.president()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/president/independent_expenditures.json?api-key=%s" % API_KEY
        self.check_response(ies, url)
        
    def test_superpacs(self):
        superpacs = self.finance.indexp.superpacs()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/superpacs.json?api-key=%s" % API_KEY
        self.check_response(superpacs, url)


class CandidateTest(APITest):
    
    def test_latest(self):
        latest = self.finance.candidates.latest()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/candidates/new.json?api-key=%s" % API_KEY
        self.check_response(latest, url)
    
    def test_detail(self):
        detail = self.finance.candidates.get("H4NY11138")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/candidates/H4NY11138.json?api-key=%s" % API_KEY
        response = requests.get(url)
        self.check_response(detail, url, parse=lambda r: r['results'][0])
    
    def test_filter(self):
        wilson = self.finance.candidates.filter("Wilson")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/candidates/search.json?api-key=%s&query=Wilson" % API_KEY
        self.check_response(wilson, url)
    
    def test_leaders(self):
        loans = self.finance.candidates.leaders("candidate-loan")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/candidates/leaders/candidate-loan.json?api-key=%s" % API_KEY
        self.check_response(loans, url)
    
    def test_candidates_for_state(self):
        candidates = self.finance.candidates.seats('RI')
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/seats/RI.json?api-key=%s" % API_KEY
        self.check_response(candidates, url)
        
    def test_candidates_for_state_and_chamber(self):
        candidates = self.finance.candidates.seats('MD', 'senate')
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/seats/MD/senate.json?api-key=%s" % API_KEY
        self.check_response(candidates, url)

    def test_candidates_for_state_and_chamber_and_district(self):
        candidates = self.finance.candidates.seats('MD', 'house', 6)
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/seats/MD/house/6.json?api-key=%s" % API_KEY
        self.check_response(candidates, url)
        
    def test_late_contributions(self):
        late_contribs = self.finance.candidates.late_contributions("H0TN08246")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/candidates/H0TN08246/48hour.json?api-key=%s" % API_KEY
        self.check_response(late_contribs, url)
    

class CommitteeTest(APITest):
    
    def test_latest(self):
        latest = self.finance.committees.latest()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/new.json?api-key=%s" % API_KEY
        self.check_response(latest, url)
    
    def test_detail(self):
        detail = self.finance.committees.get("C00490045")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/C00490045.json?api-key=%s" % API_KEY
        response = requests.get(url)
        self.check_response(detail, url, parse=lambda r: r['results'][0])

    def test_filter(self):
        hallmark = self.finance.committees.filter("Hallmark")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/search.json?api-key=%s&query=Hallmark" % API_KEY
        self.check_response(hallmark, url)

    def test_contributions(self):
        contributions = self.finance.committees.contributions("C00381277")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/C00381277/contributions.json?api-key=%s" % API_KEY
        self.check_response(contributions, url)

    def test_contributions_to_candidate(self):
        contributions = self.finance.committees.contributions_to_candidate("C00007450", "H0PA12132")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/C00007450/contributions/candidates/H0PA12132.json?api-key=%s" % API_KEY
        self.check_response(contributions, url)
        
    def test_late_contributions(self):
        late_contribs = self.finance.committees.late_contributions("C00466854")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/C00466854/48hour.json?api-key=%s" % API_KEY
        self.check_response(late_contribs, url)
    
    def test_filings(self):
        filings = self.finance.committees.filings("C00490045")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/C00490045/filings.json?api-key=%s" % API_KEY
        self.check_response(filings, url)
    
    def test_ie_totals(self):
        ie_totals = self.finance.committees.ie_totals("C00490045")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/C00490045/independent_expenditures/races.json?api-key=%s" % API_KEY
        self.check_response(ie_totals, url)
    
    def test_leadership(self):
        leadership = self.finance.committees.leadership()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/committees/leadership.json?api-key=%s" % API_KEY
        self.check_response(leadership, url)

class LateContributionTest(APITest):
    
    def test_latest(self):
        late_contribs = self.finance.late_contribs.latest()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/contributions/48hour.json?api-key=%s" % API_KEY
        self.check_response(late_contribs, url)
        
    def test_date(self):
        late_contribs = self.finance.late_contribs.date(2012,3,23)
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/contributions/48hour/2012/3/23.json?api-key=%s" % API_KEY
        self.check_response(late_contribs, url)

class PresidentTest(APITest):
    
    def test_candidates(self):
        candidates = self.finance.president.candidates()
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/president/totals.json?api-key=%s" % API_KEY
        self.check_response(candidates, url)
        
    def test_detail_using_id(self):
        candidate = self.finance.president.detail("C00431445")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/president/candidates/C00431445.json?api-key=%s" % API_KEY
        self.check_response(candidate, url, parse=lambda r: r['results'][0])

    def test_detail_using_name(self):
        candidate = self.finance.president.detail("obama")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/president/candidates/obama.json?api-key=%s" % API_KEY
        self.check_response(candidate, url, parse=lambda r: r['results'][0])
    
    def test_state_total(self):
        state = self.finance.president.state("AZ")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/president/states/AZ.json?api-key=%s" % API_KEY
        self.check_response(state, url, parse=lambda r: r['results'][0])
    
    def test_zip_total(self):
        zipcode = self.finance.president.zipcode("33407")
        url = "http://api.nytimes.com/svc/elections/us/v3/finances/2012/president/zips/33407.json?api-key=%s" % API_KEY
        self.check_response(zipcode, url, parse=lambda r: r['results'][0])
    

if __name__ == "__main__":
    unittest.main()