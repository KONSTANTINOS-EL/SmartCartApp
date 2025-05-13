import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
from smartCartApp import db
from unidecode import unidecode 

def normalize_string(string):
    return unidecode(string.lower()).strip()

def scrape_products_from_sklavenitis(search_term):
    base_url = "https://www.sklavenitis.gr"
    search_url = f"{base_url}/apotelesmata-anazitisis/?Query={search_term}"
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {search_url}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    #Find the first product block
    product_items = soup.find_all("div", class_="product_innerTop")
    price_divs = soup.find_all("div", class_="price", attrs={"data-price": True})
    if not product_items:
        print("No products found.")
        return []
    
    products = []
    
    #Iterate through the product items and price divs
    # Use zip_longest to handle cases where the number of product items and price divs are not equal
    for item, price_div in list(zip_longest(product_items, price_divs))[:20]:
        #Exctarct product details
        title_tag = item.find("h4", class_= "product__title")
        product_name = title_tag.get_text(strip=True) if title_tag else "Unknown Product"
        img_tag = item.find("img")
        image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else None
        description = img_tag['title'] if img_tag and img_tag.has_attr('title') else "No description available"
        price = float(price_div['data-price'].replace(",", ".").replace("€", "").strip()) if price_div and price_div.has_attr("data-price") else None
        
        product = {
            "name": product_name,
            "description": description,
            "price": price,
            "image_url": image_url
        }

        # if not db.products.find_one({"name":product_name}):
        #     db.products.insert_one(product)
        
        #In this stage i will try to normalize name and description
        #data for searching.
        #Fist it is going on find the name and after that the description.
        normalized_name = normalize_string(product_name)
        normalized_descrption = normalize_string(description)

        existing_product = db.products.find_one({
            "$or":[
                {"name": normalized_name},
                {"description": normalized_descrption}
            ]
        })

        if not existing_product:
            db.products.insert_one(product)

        products.append(product)

    return products

def scrape_products_from_masouti(search_term):
    base_url = "https://www.market-in.gr"
    search_url = f"{base_url}/el-gr/ALL?Title={search_term}"
    response = requests.get(search_url) 
    if response.status_code != 200:
        print(f"Failed to retrieve data from {search_url}. Status code: {response.status_code}")


    soup = BeautifulSoup(response.text, "html.parser")

    #Find the first product block
    product_items = soup.find_all("div", class_="product-col")

    products = []

    for item in product_items:
        #Exctarct product details
        name = item.find("a", class_="product-ttl").get_text(strip=True)

        brand = item.find("a", class_="product-brand").get_text(strip=True)
        description = name  
        
        price_tag = item.find("span", class_="new-price")
        price = float(price_tag.get_text(strip=True).replace(",", ".").replace("€", "")) if price_tag else None


        img_tag = item.find("a", class_="product-thumb").find("img")
        image_url = "https://www.market-in.gr" +  img_tag["src"] if img_tag else ""

        product = {
            "name": brand,
            "description": description,
            "price": price,
            "image_url": image_url
        }

        #In this stage i will try to normalize name and description
        #data for searching.
        #Fist it is going on find the name and after that the description.
        normalized_name = normalize_string(name)
        normalized_descrption = normalize_string(description)

        existing_product = db.products.find_one({
            "$or":[
                {"name": normalized_name},
                {"description": normalized_descrption}
            ]
        })

        if not existing_product:
            db.products.insert_one(product)

        products.append(product)

    return products
