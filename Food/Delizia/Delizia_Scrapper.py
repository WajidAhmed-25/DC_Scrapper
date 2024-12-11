# -------------------------------------------------------- Libraries Decleration ------------------------------------------------------------------#


import pyautogui
import webbrowser
import time
import os
import pyperclip
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
import re



# -------------------------------------------------------- Functions Decleration ------------------------------------------------------------------#


def save_html_content():
    url = "https://www.delizia.pk/"
    webbrowser.open(url)
    time.sleep(5)

    pyautogui.hotkey('ctrl', 'shift', 'c')
    time.sleep(2)
    pyautogui.hotkey('ctrl', ']')
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(2)

    js_command = 'copy(document.getElementsByClassName("items-section-wrapper")[0].outerHTML);'
    pyautogui.write(js_command)
    time.sleep(1.5)
    pyautogui.press('enter')
    time.sleep(1.5)

    html_content = pyperclip.paste()
    
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.split('.')[0]  
    file_name = f"Delizia.html"

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML content has been saved to {os.path.abspath(file_name)}")

    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1.3)
    








def extract_and_save_menu(input_html, output_html, div_ids_and_classes):


    with open(input_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')


    new_soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
    new_body = new_soup.body


    for div_info in div_ids_and_classes:
        div = soup.find('div', div_info)
        if div:
            new_body.append(div)

 
    with open(output_html, 'w', encoding='utf-8') as file:
        file.write(str(new_soup))

    print(f"The specified divs have been saved to {output_html}.")





def extract_food_menu_1(input_html, output_json):
    with open(input_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    div= soup.find_all('div', class_='p-0 mb-3 mb-md-0 large_icons_menu-item undefined undefined undefined col-12 col-sm-12 col-md-4 col-lg-3')
    

    
    deals = []

    for div in div:
        deal = {}
        
        datacatid = div.get('datacatid', '')
        dataitemid = div.get('dataitemid', '')
        if datacatid and dataitemid:
            deal['product_url'] = f"https://www.delizia.pk/?item_id={dataitemid}%7C{datacatid}"

        title_tag = div.find('h2', style='color: rgb(33, 37, 41);')
        if title_tag:
            deal['product_title'] = title_tag.get_text(strip=True)

        description_tag = div.find('p', class_='truncated trancated-3')
        if description_tag:
            deal['product_description'] = description_tag.get_text(strip=True)

    
    
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
                    
            if 'original_price' not in deal:        
                price_tag = price_wrapper.find('span', class_='normal-price')
                if price_tag:
                            price = price_tag.get_text(strip=True).replace('Rs.', '').strip()
                            if price:
                                deal['product_price'] = price        


        img_tag = div.find('img', class_='rounded-0')
        if img_tag and img_tag.get('src'):
            img_url = img_tag['src']
            deal['product_image'] = "https://www.delizia.pk"+img_url

        if deal:
            deals.append(deal)

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(deals, json_file, indent=4)

    print(f"Data has been successfully saved to {output_json}")







def add_brand_name_to_products(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    for product in data:

        product["brand_name"] = "Delizia"


        match = re.search(r'%7C(\d+)', product["product_url"])
        if match:
            number = match.group(1)
           
            if number == '404128':
                product["food_category"] = "Cake"
            
            elif number == '404129':
                product["food_category"] = "Donut"
                
            elif number == '404130':
                product["food_category"] = "Cupcake"   
                
            elif number == '404131':
                product["food_category"] = "Brownie"
                
            elif number == '404132':
                product["food_category"] = "Dessert"     
           

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)



def modify_product_data(input_file):
    
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        return None
    
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    for product in data:
       
        if 'product_price' in product:
            product['original_price'] = product.pop('product_price')
        else:
            product['original_price'] = None         

        product['discount_price'] = 0
        product['discount_percentage'] = 0
    
    with open('Delizia_Deals.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    return 'Delizia_Deals.json'
        
        
# -------------------------------------------------------- Functions Calling ------------------------------------------------------------------#

print("Automation Started")

save_html_content()

print("Automation Ended and HTML File Created Successfully")


time.sleep(1)


div_ids_and_classes = [
    {'id': '404128', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '404129', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '404130', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '404131', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '404132', 'class': 'item-category indolj-container large_icons_menu'},

]


extract_and_save_menu('Delizia.html', 'Delizia_menu_items.html', div_ids_and_classes)

time.sleep(1.5)

os.remove('Delizia.html')


extract_food_menu_1('Delizia_menu_items.html', 'Delizia_Deals.json')   


time.sleep(2)



os.remove('Delizia_menu_items.html')



input_file = 'Delizia_Deals.json'

output_file = 'Delizia_Deals.json'

add_brand_name_to_products(input_file, output_file)

input_file = 'Delizia_Deals.json'


modified_file = modify_product_data(input_file)
print(f"Modified JSON file saved as: {modified_file}")


print("All Done")



print("All Done")



