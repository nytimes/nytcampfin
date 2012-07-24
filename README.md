NYT Campfin
==================

A very basic Python client for the New York Times [Campaign Finance API](http://developer.nytimes.com/docs/campaign_finance_api). You'll need an API key, which should be set as an environment variable to run the tests. The client returns JSON only, not full Python objects, and attempts to implement each response in The Times' API.

Install
-------

Set your API key as an environment variable NYT_CAMPFIN_API_KEY:

    $ export NYT_CAMPFIN_API_KEY=YOUR-API-KEY
    $ pip install nytcampfin

Or download and run

    $ python setup.py install

Requirements
------------

NYT Campfin uses the [Kenneth Reitz's Requests library](https://github.com/kennethreitz/requests) for retrieving API endpoints and [Roman Haritonov's requests-cache library](https://github.com/reclosedev/requests-cache) for local caching. The cache is preconfigured to use a local sqlite database and set to expire after 5 minutes.
    
Tests
-----

To run the tests, do the following:
    
    $ python test.py
    
The use of caching is disabled in the tests.

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
    
    # retrieve a candidate's details
    >>> cand = finance.candidates.get('H4NY11138')
    >>> cand['name']
    u'CLARKE, YVETTE D'
    
See the tests for plenty more examples.

Note on Patches/Pull Requests
-----------------------------

  * Fork the project.
  * Make your feature addition or bug fix.
  * Add tests for it.
  * Send a pull request. Bonus points for topic branches.

Authors
-------

  Derek Willis, dwillis@nytimes.com

Copyright
---------

Copyright (c) 2012 The New York Times Company. See LICENSE for details.

    