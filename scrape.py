import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from lxml import html

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
}

# # Define the URL to scrape
url = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87507&index=0&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords="
session = requests.Session()
session.headers.update(headers)

# Make the request to fetch the page
response = session.get(url)

selector = html.fromstring(response.text)
data = selector.xpath("//script[contains(.,'jsonModel = ')]/text()")
data = data[0].split("jsonModel = ", 1)[1].strip()
data = json.loads(data)
pagination = data.get("pagination", {})
total = pagination.get("total", None)
# Property ID scraping

pages = total

# Page count scrape
url_list = []


for i in range(pages):
    index = i * 24
    url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=OUTCODE%5E2519&index={i}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
    url_list.append(url)

scraped_data = []

for url in url_list:
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    hrefs = set(a['href']
                for a in soup.find_all('a', class_='propertyCard-link'))
    scraped_data.extend([href.split('/')[2] for href in hrefs])


property_id = pd.DataFrame({'property id': scraped_data})

# property_id.to_csv("data/hrefs/href.csv", index=False)

# Individual property scraping
urls = []

for row in property_id.values:
    urls.append(
        f'https://www.rightmove.co.uk/properties/{row[0]}/?channel=RES_BUY')

extracted_data_list = []
for url in urls:
    session = requests.Session()
    session.headers.update(headers)

    # Make the request to fetch the page
    response = session.get(url)
    selector = html.fromstring(response.text)
    data = selector.xpath("//script[contains(.,'PAGE_MODEL = ')]/text()")
    data = data[0].split("PAGE_MODEL = ", 1)[1].strip()
    data = json.loads(data)
    property_data = data["propertyData"]

    # ID
    id = property_data.get("id", "")

    # Prices
    prices = property_data.get("prices", {})
    primary_price = prices.get("primaryPrice", "")

    # Address
    address = property_data.get("address", {})
    display_address = address.get("displayAddress", "")
    outcode = address.get("outcode", "")
    incode = address.get("incode", "")
    # Stations
    nearest_stations = property_data.get("nearestStations", [])
    station_data = {}
    for i, station in enumerate(nearest_stations):
        station_data[f"station_{i + 1}"] = station.get("name", "")
        station_data[f"station_{i + 1}_distance_miles"] = station.get(
            "distance", "")

    extracted_data = {
        "id": id,
        "primaryPrice": primary_price,
        "displayAddress": display_address,
        "outcode": outcode,
        "incode": incode,
        "bedrooms": property_data.get("bedrooms", ""),
        "bathrooms": property_data.get("bathrooms", ""),
        **station_data,
    }
    extracted_data_list.append(extracted_data)

df = pd.DataFrame(extracted_data_list)
df.to_csv('data/property_data/property_data.csv', index=False)
