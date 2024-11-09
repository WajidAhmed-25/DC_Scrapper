# import json
# from bs4 import BeautifulSoup

# def extract_food_menu(input_html, output_json):
#     with open(input_html, 'r', encoding='utf-8') as file:
#         soup = BeautifulSoup(file, 'html.parser')

#     divs = soup.find_all('div', class_='p-0 mb-md-0 m-0 mb-0 col-12 col-md-6')
#     deals = []

#     for div in divs:
#         deal = {}

#         title_tag = div.find('h2', style='color: rgb(33, 37, 41);')
#         if title_tag:
#             deal['product_title'] = title_tag.get_text(strip=True)

#         description_tag = div.find('p', class_='truncated trancated-3')
#         if description_tag:
#             deal['product_description'] = description_tag.get_text(strip=True)
            
        

#         price_wrapper = div.find('div', class_='price-wrapper')
#         if price_wrapper:
#             price_tag = price_wrapper.find('span', class_='normal-price')
#             if price_tag:
#                 price = price_tag.get_text(strip=True).replace('Rs.', '').strip()
#                 if price:
#                     deal['product_price'] = price

#         if deal:
#             deals.append(deal)

#     with open(output_json, 'w', encoding='utf-8') as json_file:
#         json.dump(deals, json_file, indent=4)

#     print(f"Data has been successfully saved to {output_json}")


# extract_food_menu('foodsinn_menu_items.html', 'foodsinn_menu_items.json')




















import json
from bs4 import BeautifulSoup

def extract_food_menu(input_html, output_json):
    with open(input_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    divs = soup.find_all('div', class_='p-0 mb-md-0 m-0 mb-0 col-12 col-md-6')
    deals = []

    for div in divs:
        deal = {}
        
        datacatid = div.get('datacatid', '')
        dataitemid = div.get('dataitemid', '')
        if datacatid and dataitemid:
            deal['product_url'] = f"https://foodsinn.co/?item_id={dataitemid}%7C{datacatid}"

        title_tag = div.find('h2', style='color: rgb(33, 37, 41);')
        if title_tag:
            deal['product_title'] = title_tag.get_text(strip=True)

        description_tag = div.find('p', class_='truncated trancated-3')
        if description_tag:
            deal['product_description'] = description_tag.get_text(strip=True)

        price_wrapper = div.find('div', class_='price-wrapper')
        if price_wrapper:
            price_tag = price_wrapper.find('span', class_='normal-price')
            if price_tag:
                price = price_tag.get_text(strip=True).replace('Rs.', '').strip()
                if price:
                    deal['product_price'] = price


        img_tag = div.find('img', class_='img-fluid rounded-2')
        if img_tag and img_tag.get('src'):
            img_url = img_tag['src']
            deal['product_image'] = "https://foodsinn.co"+img_url

        if deal:
            deals.append(deal)

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(deals, json_file, indent=4)

    print(f"Data has been successfully saved to {output_json}")


extract_food_menu('foodsinn_menu_items.html', 'foodsinn_menu_items.json')









