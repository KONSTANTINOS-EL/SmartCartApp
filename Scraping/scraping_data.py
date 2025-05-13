import requests
from bs4 import BeautifulSoup
import re
import json

kotsovolos_tablet_url = "https://www.kotsovolos.gr/computing/laptop-tablet-ipad/tablets-ipad/320593-apple-ipad-a16-wifi-128gb-silver"

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip",
    "accept-encoding": "deflate", 
    "accept-encoding": "br",
    "accept-encoding": "zstd",
    "accept-language": "en-US,en;q=0.9,el;q=0.8"
}

response =requests.get(kotsovolos_tablet_url, headers=HEADERS)
response.raise_for_status()  # Check for request errors



soup = BeautifulSoup(response.text, "html.parser")

script_tag = soup.find(id="insider-title")
# print(script_tag) 
elements_name = soup.find_all("div", class_= "MuiGrid-root sc-4920ff9-0 rUcAx MuiGrid-item MuiGrid-grid-xs-12")
elements_description = elements_name
elements_price = soup.find_all("div", class_="MuiGrid-root sc-4920ff9-0 rUcAx MuiGrid-item")
# print(elements)

for element in elements_name:
    name_element = element.find("h2", class_="MuiTypography-root sc-e50979a4-0 fFfVJj MuiTypography-h2")
    if name_element is not None:
        name = name_element.text.strip()
        # print(name)

for element in elements_description:
    descr_element = element.find("span", class_="MuiTypography-root sc-e50979a4-0 fECOOy MuiTypography-body1 MuiTypography-colorTextSecondary")
    if descr_element is not None:
        description = descr_element.text.strip()
        # print(description)


# print(name)
# print(description)