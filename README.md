NYT Campfin
==================

A very basic Python client for the New York Times [Campaign Finance API](http://developer.nytimes.com/docs/campaign_finance_api). You'll need an API key, which should be set as an environment variable to run the tests.

Install
-------

    $ pip install nytcampfin

Or download and run

    $ python setup.py install

Usage
-----

    >>> from nytcampfin import NytCampfin
    >>> finance = NytCampfin(YOUR_NYT_CAMPAIGN_FINANCE_API_KEY)
    
    # retrieve today's filings
    >>> today = finance.filings.today()
    >>> today[0]['filing_id']
    793150
    
    # retrieve a committee's details
    >>> cmte = finance.committees.get('C00490219',2012)
    >>> cmte['id']
    u'C00490219'
