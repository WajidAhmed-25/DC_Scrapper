# import json
# from bs4 import BeautifulSoup

# def extract_food_deals(input_html, output_json):
#     with open(input_html, 'r', encoding='utf-8') as file:
#         soup = BeautifulSoup(file, 'html.parser')

#     divs = soup.find_all('div', class_='p-0 mb-md-0 m-0 mb-3 col-12 col-md-6')
#     deals = []

#     for div in divs:
#         deal = {}

#         title_tag = div.find('p', class_='truncated trancated-3')
#         if title_tag:
#             deal['product_title'] = title_tag.get_text(strip=True)

#         img_tag = div.find('img', class_='img-fluid rounded-2')
#         if img_tag and img_tag.get('src'):
#             deal['product_image'] = "https://foodsinn.co"+img_tag['src']

#         price_wrapper = div.find('div', class_='price-wrapper')
#         if price_wrapper:
          
#             original_price_tag = price_wrapper.find('span', style='text-decoration-line: line-through;')
#             if original_price_tag:
#                 original_price = original_price_tag.get_text(strip=True).replace('Rs.', '').strip()
#                 if original_price:
#                     deal['original_price'] = original_price

      
#             discount_price_tag = price_wrapper.find('span', class_='normal-price has-discount')
#             if discount_price_tag:
#                 discount_price = discount_price_tag.get_text(strip=True).replace('Rs.', '').strip()
#                 if discount_price:
#                     deal['discount_price'] = discount_price


#             discount_tag = div.find('div', class_='discount-wrapper')
#             if discount_tag:
#                 deal['discount_percentage'] = discount_tag.find('span').get_text(strip=True).replace('OFF', '').strip()

#         if deal:
#             deals.append(deal)

#     with open(output_json, 'w', encoding='utf-8') as json_file:
#         json.dump(deals, json_file, indent=4)

#     print(f"Data has been successfully saved to {output_json}")

# extract_food_deals('foodsinn_deals.html', 'foodsinn_deals.json')









##################################################################################################################################







import json
from bs4 import BeautifulSoup

def extract_food_deals(input_html, output_json):
    with open(input_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    divs = soup.find_all('div', class_='p-0 mb-md-0 m-0 mb-3 col-12 col-md-6')
    deals = []

    for div in divs:
        deal = {}


        datacatid = div.get('datacatid', '')
        dataitemid = div.get('dataitemid', '')
        if datacatid and dataitemid:
            deal['product_url'] = f"https://foodsinn.co/?item_id={dataitemid}%7C{datacatid}"
            

        title_tag = div.find('p', class_='truncated trancated-3')
        if title_tag:
            deal['product_title'] = title_tag.get_text(strip=True)

        img_tag = div.find('img', class_='img-fluid rounded-2')
        if img_tag and img_tag.get('src'):
            deal['product_image'] = "https://foodsinn.co" + img_tag['src']

        price_wrapper = div.find('div', class_='price-wrapper')
        if price_wrapper:
            original_price_tag = price_wrapper.find('span', style='text-decoration-line: line-through;')
            if original_price_tag:
                original_price = original_price_tag.get_text(strip=True).replace('Rs.', '').strip()
                if original_price:
                    deal['original_price'] = original_price

            discount_price_tag = price_wrapper.find('span', class_='normal-price has-discount')
            if discount_price_tag:
                discount_price = discount_price_tag.get_text(strip=True).replace('Rs.', '').strip()
                if discount_price:
                    deal['discount_price'] = discount_price

            discount_tag = div.find('div', class_='discount-wrapper')
            if discount_tag:
                discount_percentage = discount_tag.find('span').get_text(strip=True).replace('OFF', '').strip()
                if discount_percentage:
                    deal['discount_percentage'] = discount_percentage

        if deal:
            deals.append(deal)

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(deals, json_file, indent=4)

    print(f"Data has been successfully saved to {output_json}")


extract_food_deals('foodsinn_deals.html', 'foodsinn_deals.json')
















