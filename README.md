Python NytCampfin
==================

A Python client for the New York Times [Campaign Finance API](http://developer.nytimes.com/docs/campaign_finance_api)

Install
-------

    $ pip install python-nytcampfin

Or download and run

    $ python setup.py install

Usage
-----

    >>> from nytcampfin import NytCampfin
    >>> finance = NytCampfin(API_KEY)
    
    # get member by bioguide ID
    >>> pelosi = congress.members.get('P000197')
    >>> pelosi['twitter_id']
    'NancyPelosi'
    
    # get recent House bills
    # recent bills come in two types: 'introduced' and 'updated'
    >>> introd = congress.bills.recent(chamber='house', congress=111, type='introduced')
    >>> len(introd['bills'])
    20
    >>> introd['chamber']
    'House'
    
    # or use a convenience function
    >>> introd = congress.bills.introduced('house')
    >>> introd['chamber']
    'House'
    >>> len(introd['bills'])
    20
    
