import numpy as np
import pandas as pd 
import requests
import matplotlib.pyplot as plt 
from bs4 import BeautifulSoup

# Requesting page elements
r = requests.get('https://www.renthop.com/nyc/apartments-for-rent')

# Analyzing page elements with BeautifulSoup
soup = BeautifulSoup(r.content, 'html5lib')

# Listing all divs that contains 'search-info' 
listing_divs = soup.select('div[class*=search-info]')

# Definition of function to parse parse_data
def parse_data(listing_divs):
    listing_list = []
    # Parsing page elements
    for index in range(len(listing_divs)):
        indiv_listing = []
        href = listing_divs[index].select('a[id*=title]')[0]['href']
        addy = listing_divs[index].select('a[id*=title]')[0].string
        hood = listing_divs[index].select('div[id*=hood]')[0].string.replace('\n','')

        indiv_listing.append(href)
        indiv_listing.append(addy)
        indiv_listing.append(hood)
        listing_specs = listing_divs[index].select('table[id*=info] tr')
        for spec in listing_specs:
            try:
                values = spec.text.strip().replace(' ','_').split()
                clean_values = [x for x in values if x != '_']
                indiv_listing.extend(spec.text.strip().replace(' ','_').split())
            except:
                indiv_listing.extend(np.nan)
        listing_list.append(indiv_listing)
    return listing_list


url_prefix = 'https://www.renthop.com/search/nyc?max_price=50000&min_price=0&page='
url_suffix = '&sort=hopscore&q=&search=0'
page_number = 1
for i in range(3):
    target_page = url_prefix + str(page_number) + url_suffix
    print(target_page)
    page_number += 1
