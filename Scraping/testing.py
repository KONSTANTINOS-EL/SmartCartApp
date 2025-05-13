import requests
from bs4 import BeautifulSoup
import re
import html

# Request headers to simulate browser
headers = {
    'User-Agent': 'Mozilla/5.0'
}

url = "https://www.sklavenitis.gr/fresko-kreas/fresko-choirino/"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

product_divs = soup.find_all("div", class_="product")

for i, div in enumerate(product_divs, 1):
    raw_data = div.get("data-plugin-analyticsclickable")
    if not raw_data:
        print(f"❌ Product {i}: No data-plugin-analyticsclickable attribute.")
        continue

    # Unescape any HTML entities
    raw_data = html.unescape(raw_data)

    # Try to find the JS string that looks like window.dataLayer.push({...});
    match = re.search(r'window\.dataLayer\.push\(\{.*?"items"\s*:\s*\[(.*?)\]\s*\}\);', raw_data, re.DOTALL)
    if match:
        item_json = match.group(1)

        # Now extract item_name and price from that inner JS block
        name_match = re.search(r'"item_name"\s*:\s*"([^"]+)"', item_json)
        price_match = re.search(r'"price"\s*:\s*([0-9.]+)', item_json)

        if name_match and price_match:
            name = name_match.group(1)
            price = float(price_match.group(1))
            print(f"🛒 Product {i}")
            print(f"   🔹 Name: {name}")
            print(f"   🔹 Price: €{price}")
            print("-" * 40)
        else:
            print(f"❌ Product {i}: Couldn't extract name or price.")
    else:
        print(f"❌ Product {i}: JavaScript data not found or malformed.")
