# Standard Library Imports
import datetime, os
from typing import List

# Third Party package imports (install through pip install -r requirements.txt)
import requests
from easy_reed import config
from easy_reed.namespace import NameSpace
from easy_reed import logger

# Defining a new config field for the USER_AGENT Header
app_namespace = NameSpace("app")
app_namespace.add_entry("USER_AGENT", str, "")
config.add_namespace(app_namespace)

# Constants
DATA_REPORTING_FIRST_FULL_YEAR = 1999
URL = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_{YEAR}{MONTH}_NSW1.csv"
HEADERS = {'user-agent': config['app']['USER_AGENT']}

def scrape_aemo():
    """ Script used to download AEMO Historical aggregated price and demand data
    
    This script programatically calls AEMOS API to retrieve Historical aggregated price and demand data for
    electricity price in the NSW (New South Wales) region of Australia.  The API is split up by month and year,
    so getting all of the historical data for one year takes 12 calls.  Once we have aggregated the data,
    we will clean it and write it out to a single CSV.
    """
    # Create the results array; we will story the yearly results here and join them all to a single string after making all of the web calls.  This will be faster than doing it on the fly.
    results = []
    # Make 1 call for the first year data, since it is a special case (Data only exists for December)
    results.extend(gather_year_data(DATA_REPORTING_FIRST_FULL_YEAR-1, start_month=12, start=True))
    # Loop through each year that has a full 12 months of data.  Gather the historical data and append it to results
    for year in range(DATA_REPORTING_FIRST_FULL_YEAR, datetime.date.today().year):
        results.extend(gather_year_data(year))
    # Make 1 final call for the most recent year data, since it is a special case (Data only exists up to the current month.)
    results.extend(gather_year_data(datetime.date.today().year, end_month=datetime.date.today().month))
    # Write the data
    with open(f'{os.path.dirname(__file__)}/aemo_price_data.csv', 'w') as outfile:
        outfile.write("".join(results))

def gather_year_data(year: int, start_month: int = 1, end_month: int = 12, start=False) -> List[str]:
    """ Function to gather historical data from Aemo for a single year.

    This function takes the year to gather data for.  Then, it will make the necessary web calls
    to AEMO's api to gather the data.  If we only want data for specific months of the year, we can optionally
    pass 'start_month' and 'end_month' to specify a range.  By default, this function will search for data
    from all 12 months of the year

    PARAMETERS
    ----------
    year: int
        - the year we are gathering data for
    start_month: int
        - the first month in the year to gather data for
    end_month: int
        - the last month in the year to gather data for
    start: bool
        - specifies if this is the first call to gather data.  If it is, we keep the indexes
        
    RETURNS
    -------
    List[str]
        - a list where each index is a string representing the CSV data for a given month of Historical data
    """
    # Set the current URL to include the given year, and prepare an empty result list
    current_url = URL.replace("{YEAR}", str(year))
    results: List[str] = []

    # Make one call to the API for each month
    for month in range(start_month, end_month + 1):
        logger.debug(f"Calling for year {year} and month {month}")
        # If the month is 1 digit, it must have a leading 0 in the URL
        month_string = str(month)
        if month < 10:
            month_string = f"0{month}"
        # Make a call to the final URL and translate the response data to string
        response = str(requests.get(current_url.replace("{MONTH}", month_string), headers=HEADERS).text)
        # If this is the first month processed; keep the indexes.  Otherwise, remove them
        if(start and month == start_month):
            results.append(response)
        else:
            results.append(response.split('\n', maxsplit=1)[1])
    # Return the data that was processed for the given year
    return results

# If this file is run as a script, it will run the scrape_aemo function and create the csv datafile
if __name__ == '__main__':
    scrape_aemo()