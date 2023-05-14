from requests_html import HTML, HTMLSession
from easy_reed import config
from easy_reed.namespace import NameSpace

# Defining a new config field for the USER_AGENT Header
app_namespace = NameSpace("app")
app_namespace.add_entry("USER_AGENT", str, "")
config.add_namespace(app_namespace)

# constants
URL = 'https://www.asxenergy.com.au/futures_au/'
HEADERS = {'user-agent': config['app']['USER_AGENT']}

def scrape_asx():
    session = HTMLSession()
    response = session.get(URL)
    response.html.render()
    with open('sample_page.html', 'w') as page:
        page.write(response.html.find('body')[0].html)
    print(response.html.find('div')[0].attrs)

    market_datasets = response.html.find('div.market-dataset')
    print(market_datasets)
    sections = market_datasets[0].find('td.market-dataset-state')
    print(sections)

    final_index = -1
    for index, section in enumerate(sections):
        if 'New South Wales' in section.html:
            final_index = index
            break

    print(final_index)
    time_data_tables = market_datasets[1].find('td.market-dataset-state')
    wales_data_set = time_data_tables[final_index]

    tables = wales_data_set.find('table')

    for table in tables:
        if 'BQtr' in table.html:
            tbody = table.find('tbody')
            rows = tbody[0].find('tr')
            print(rows)
            for row in rows:
                if 'Q423' in row.html:
                    print("here")
                    data = row.find('td.settlement')
                    result = str(data.html).split('>', maxsplit=1)
                    result = result[1].split('<', maxsplit=1)
                    return result[0]
                
if __name__ == '__main__':
    print(scrape_asx())