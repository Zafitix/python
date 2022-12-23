import requests
from bs4 import BeautifulSoup
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

while True:
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json')
    client = gspread.authorize(creds)
    sheet = client.open('Poke').sheet1

    values = sheet.get_all_values()

    index = 2

    for value in values:
        if value[0] == "Nom de l'item":
            values.remove(value)

    for value in values:
        keywords = value[1]

        URL = f"https://www.ebay.fr/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={keywords}&_sacat=0&LH_TitleDesc=0&_odkw={keywords}&_osacat=0&LH_Complete=1&LH_Sold=1"

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')

        products = soup.find_all('li', class_='s-item')

        prices = []

        for product in products:
            price = product.find('span', class_='s-item__price').text
            price = price[:-4]
            price = price.replace(",", ".")
            if price != "$2":
                try:
                    price = float(price)
                    prices.append(price)
                except:
                    pass
        try:

            ref_price = float(sheet.cell(index,3).value)

            min_price = ref_price*0.70
            max_price = ref_price*1.30

            sorted_prices = []

            for price in prices:
                if (price > min_price) and (price < max_price):
                    sorted_prices.append(price)

            price_average = sum(sorted_prices)/len(sorted_prices)

            sheet.update_cell(index,5,price_average)

            index += 1
        except:
            pass

        print("RefPrice :", ref_price)
        print("MinPrice :", min_price)
        print("MaxPrice :", max_price)
        print("PriceAverage :",price_average)
        print("================")




   













    