import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

data = []

sklavenitis_tablet_urls = [
    "https://www.sklavenitis.gr/fresko-kreas/fresko-choirino/kimas-choirinos/kimas-hoirinos-apahos-eisagogs-500gr-246223/",
    "https://www.sklavenitis.gr/fresko-kreas/fresko-choirino/spala-choirini/meat-house-tigania-hoirin-nop-700gr-246160/",
    "https://www.sklavenitis.gr/fresko-kreas/fresko-choirino/mprizoles-choirines/laimos-hoirinos-sklavenitis-me-osto-ollandias/",
    "https://www.sklavenitis.gr/fresko-kreas/fresko-choirino/mprizoles-choirines/sklavenitis-mprizola-hoirin-ollandias-me-osto-240986/",
    "https://www.sklavenitis.gr/fresko-kreas/fresko-choirino/panseta/sklavenitis-panseta-hoirin-ollandias-me-osto-240965/",
    "https://www.sklavenitis.gr/fresko-kreas/fresko-choirino/mpoyti-choirino/mpouti-hoirino-me-osto-sklavenitis-ollandias-1252965/",
    "https://www.sklavenitis.gr/fresko-kreas/fresko-choirino/psaronefri/fileto-hoirino-ollandias-1454391/",
    "https://www.sklavenitis.gr/galata-rofimata-chymoi-psygeioy/galata-psygeioy/xynogala-kefir-ariani/marata-kefir-me-geusi-fraoula-500ml-1633638/",
    "https://www.sklavenitis.gr/galata-rofimata-chymoi-psygeioy/galata-psygeioy/xynogala-kefir-ariani/marata-kefir-500ml-1633637/",
    "https://www.sklavenitis.gr/galata-rofimata-chymoi-psygeioy/galata-psygeioy/galata-agelados-ypsilis-pasteriosis/olumpos-pnoi-gala-upsilis-pasteriosis-me-vitamini-d-15-1l-1650197/",
    "https://www.sklavenitis.gr/galata-rofimata-chymoi-psygeioy/galata-psygeioy/galata-agelados-ypsilis-pasteriosis/marata-gala-upsils-pasteriosis-plres-1lt-240867/",
    "https://www.sklavenitis.gr/galata-rofimata-chymoi-psygeioy/galata-psygeioy/galata-agelados-ypsilis-pasteriosis/marata-gala-upsils-pasteriosis-elafru-1lt-240563/",
    "https://www.sklavenitis.gr/galata-rofimata-chymoi-psygeioy/galata-psygeioy/galata-agelados-ypsilis-pasteriosis/nounou-family-gala-upsils-pasteriosis-elafru-15lt-220182/",
    "https://www.sklavenitis.gr/galata-rofimata-chymoi-psygeioy/galata-psygeioy/galata-agelados-ypsilis-pasteriosis/nounou-family-gala-upsilis-pasteriosis-plires-15lt/",
    "https://www.sklavenitis.gr/giaoyrtia-kremes-galaktos-epidorpia-psygeioy/giaoyrtia/giaoyrtia-agelados-straggista/fage-total-giaourti-straggisto-0-1kg-1650135/",
    "https://www.sklavenitis.gr/giaoyrtia-kremes-galaktos-epidorpia-psygeioy/giaoyrtia/giaoyrtia-agelados-straggista/marata-giaourti-straggisto-2-1kg/",
    "https://www.sklavenitis.gr/giaoyrtia-kremes-galaktos-epidorpia-psygeioy/giaoyrtia/giaoyrtia-agelados-straggista/marata-giaourti-straggisto-10-elliniko-1kg-243038/",
    "https://www.sklavenitis.gr/giaoyrtia-kremes-galaktos-epidorpia-psygeioy/giaoyrtia/giaoyrtia-agelados-straggista/total-giaourti-straggisto-2-1kg/",
    "https://www.sklavenitis.gr/turokomika-futika-anapliromata/feta-leyka-tyria/feta/feta-thumelis-mutilinis-pop-horis-glouteni-400g-1649597/",
    "https://www.sklavenitis.gr/turokomika-futika-anapliromata/feta-leyka-tyria/feta/feta-karali-pop-400gr/",
    "https://www.sklavenitis.gr/turokomika-futika-anapliromata/feta-leyka-tyria/leyka-tyria-ageladina/rodopi-leuko-turi-agelados-400gr/",
    "https://www.sklavenitis.gr/turokomika-futika-anapliromata/feta-leyka-tyria/feta/karalis-feta-pop-200gr-1221842/",
    "https://www.sklavenitis.gr/turokomika-futika-anapliromata/feta-leyka-tyria/feta/sunetairismos-kalavruton-feta-varelisia-pop-243957/",
    "https://www.sklavenitis.gr/turokomika-futika-anapliromata/feta-leyka-tyria/feta/-peiros-turi-feta-se-almi-400gr-232548/",
    "https://www.sklavenitis.gr/turokomika-futika-anapliromata/feta-leyka-tyria/leyka-tyria-ageladina/leuko-turi-rodopi-900gr/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/ayga/ayga/auga-ahurona-vlahaki-diafora-megethi-6tem-320g/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/ayga/ayga/hrusa-auga-freska-eleutheras-vosks-me-o3-medium-53-63gr-6-tem--050-232066/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/ayga/ayga/-1223800/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/ayga/ayga/auga-ahurona-tsaousi-diafora-megethi-6tem-318gr/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/ayga/ayga/auga-hrusa-auga-large-6tem-63-73gr-5163068/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/voytyra/voytyra-agelados-proveia/president-vouturo-analato-60-200gr-1615757/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/voytyra/voytyro-galaktos/karalis-vouturo-aigoproveio-liomeno-300gr-1222817/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/voytyra/voytyro-galaktos/divanis-vouturo-galaktos-liomeno-500gr-1297635/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/voytyra/voytyro-galaktos/milba-ghee-vouturo-galaktos-agelados-300gr-1514079/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/voytyra/voytyra-agelados-proveia/marata-vouturo-agelados-250gr-1629284/",
    "https://www.sklavenitis.gr/ayga-voytyro-nopes-zymes-zomoi/voytyra/voytyra-agelados-proveia/lurpak-vouturo-analato-250gr-220769/",
    "https://www.sklavenitis.gr/eidi-artozacharoplasteioy/psomi-artoskeyasmata/mpagketa-margarita-alla-psomia-gia-santoyits/psomi-me-prozumi-diplozumoto-katselis-starenio-se-fetes-500gr/",
    "https://www.sklavenitis.gr/eidi-artozacharoplasteioy/psomi-artoskeyasmata/mpagketa-margarita-alla-psomia-gia-santoyits/psomi-me-prozumi-fournismata-vosinaki-starenio-se-fetes-500gr-1584223/",
    "https://www.sklavenitis.gr/eidi-artozacharoplasteioy/psomi-artoskeyasmata/mpagketa-margarita-alla-psomia-gia-santoyits/psomi-me-prozumi-diplozumoto-katselis-olikis-alesis-se-fetes-500gr/",
    "https://www.sklavenitis.gr/freska-froyta-lachanika/lachanika/anithos-maintanos-selino-alla-myrodika/maidanos-eghorios-100gr/",
    "https://www.sklavenitis.gr/freska-froyta-lachanika/lachanika/anithos-maintanos-selino-alla-myrodika/duosmos-eghorios-50gr/",
    "https://www.sklavenitis.gr/freska-froyta-lachanika/lachanika/anithos-maintanos-selino-alla-myrodika/mantanos-viologikos-ellinikos-243840/",
    "https://www.sklavenitis.gr/freska-froyta-lachanika/lachanika/kremmydia-skorda-volvoi/kremmudia-kokkina-ellinika-238343/",
    "https://www.sklavenitis.gr/freska-froyta-lachanika/lachanika/kremmydia-skorda-volvoi/kremmudakia-hlora-ellinika-240661/",
    "https://www.sklavenitis.gr/freska-froyta-lachanika/lachanika/anithos-maintanos-selino-alla-myrodika/duosmos-eghorios-25gr-1158254/",
    "https://www.sklavenitis.gr/freska-froyta-lachanika/lachanika/kremmydia-skorda-volvoi/kremmudia-xantha-ellinika-238553/",
    "https://www.sklavenitis.gr/freska-froyta-lachanika/lachanika/kremmydia-skorda-volvoi/skorda-eisagogs-3tem-245932/",
    "https://www.sklavenitis.gr/freska-froyta-lachanika/lachanika/lachana-karota-mprokola-koynoypidia/karota-viologika-ellados/",
    "https://www.sklavenitis.gr/fresko-psari-thalassina/psaria-ichthyokalliergeias/tsipoyres/tsipoura-46-eghoria/",
    "https://www.sklavenitis.gr/fresko-psari-thalassina/psaria-ichthyokalliergeias/lavrakia/lavraki-ektrofis-katharismeno-elliniko-400gr-eos-600gr/",
    "https://www.sklavenitis.gr/fresko-psari-thalassina/psaria-ichthyokalliergeias/pestrofes-solomoi/solomos-norvigias-fileto/",
    "https://www.sklavenitis.gr/fresko-psari-thalassina/psaria-ichthyokalliergeias/pestrofes-solomoi/solomos-norvigias-feta/"

]

for url in sklavenitis_tablet_urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find(class_="product-detail")
    # print(results.prettify())  # Uncomment to see the full HTML structure

    items_right = results.find_all("article", class_="product-detail__right") 
    for item in items_right: 
        item_name = item.find("h1", class_="product-detail__title")
        if item_name is not None:
            name = item_name.text.strip()
            # print(name)
        item_description = item.find("div", class_="product-detail__text")
        if item_description is not None:
            description = item_description.text.strip()
            # print(description)

    items_left = results.find_all("div", class_="product_prices")
    for item in items_left:
        item_price = item.find("div", class_="price")
        if item_price is not None:
            price = item_price.text.strip()
            # print(price)

    img_tag = soup.find("img", class_="product-image__img")

    if img_tag:
        img_src = img_tag.get("src")
        img_alt = img_tag.get("alt")
        img_title = img_tag.get("title")  

        # print(f"Image Source: {img_src}")
        # print(f"Image Alt: {img_alt}")  
        # print(f"Image Title: {img_title}")

        data.append((name, description, price, img_src))

# print(data)

df = pd.DataFrame(data, columns=["name", "description", "price", "image_url"])
df.to_csv("sklavenitis_products.csv", sep=';', index=False, encoding="utf-8-sig")





