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
    url = "https://www.unitedkingonline.com/"
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
    file_name = f"UnitedKing.html"

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
            deal['product_url'] = f"https://www.kaybees.com.pk/?item_id={dataitemid}%7C{datacatid}"

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
            deal['product_image'] = "https://www.kaybees.com.pk/"+img_url

        if deal:
            deals.append(deal)

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(deals, json_file, indent=4)

    print(f"Data has been successfully saved to {output_json}")



def separate_deals_and_normal(input_file):

    with open(input_file, "r") as file:
        data = json.load(file)
    

    deals = [item for item in data if "original_price" in item]
    normal = [item for item in data if "original_price" not in item]
    

    with open("Kaybees_Deals.json", "w") as deals_file:
        json.dump(deals, deals_file, indent=4)
    

    with open("Kaybees_Menu.json", "w") as normal_file:
        json.dump(normal, normal_file, indent=4)

    print("Separation complete: 'Kaybees_Deals.json' and 'Kaybees_Menu.json' created.")








def add_brand_name_to_products(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    for product in data:

        product["brand_name"] = "Kaybees"


        match = re.search(r'%7C(\d+)', product["product_url"])
        if match:
            number = match.group(1)
           
            if number == '418864':
                product["food_category"] = "Deal"
            
            elif number == '419454':
                product["food_category"] = "Deal"
                
            elif number == '419456':
                product["food_category"] = "Deal"   
                
            elif number == '417449':
                product["food_category"] = "Deal"
                
            elif number == '412476':
                product["food_category"] = "Starter"     
                
            elif number == '402434':
                product["food_category"] = "Deal"    
                
            elif number == '2003':
                product["food_category"] = "Soup"              
        
            elif number == '1444':
                product["food_category"] = "Starter"
                 
            elif number == '1466':
                product["food_category"] = "Sandwich"              
        
            elif number == '1465':
                product["food_category"] = "Burger"        
        
            elif number == '1468':
                product["food_category"] = "Broast"              
        
            elif number == '1462':
                product["food_category"] ="BBQ"
                
            elif number == '1464':
                product["food_category"] ="Chinese" 
           
            elif number == '1467':
                product["food_category"] ="Noodle" 
            
            elif number == '1463':
                product["food_category"] ="Chinese"    
            
            elif number == '1461':
                product["food_category"] ="Steak"  
                
            elif number == '1460':
                product["food_category"] ="Karachi"  
                
            elif number == '1459':
                product["food_category"] ="Handi" 
            
            elif number == '1458':
                product["food_category"] ="Desi"    
            
            elif number == '1469':
                product["food_category"] ="Sea Food"  
                
            elif number == '1457':
                product["food_category"] ="Rice"   
                
            elif number == '1455':
                product["food_category"] ="Naan"                            
                
            elif number == '08021':
                product["food_category"] ="Kid"   
                
            elif number == '1453':
                product["food_category"] ="Dessert"       
                
            elif number == '1454':
                product["food_category"] ="Add Ons"   
                
            elif number == '1448':
                product["food_category"] ="Mocktail or Shake"  
                
            elif number == '1450':
                product["food_category"] ="Mocktail or Shake"   
                
            elif number == '1449':
                product["food_category"] ="Beverage"                            
                
            elif number == '1447':
                product["food_category"] ="Hot Beverage"   
                
        
 

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)


# -------------------------------------------------------- Functions Calling ------------------------------------------------------------------#

print("Automation Started")

save_html_content()

print("Automation Ended and HTML File Created Successfully")


time.sleep(1)


div_ids_and_classes = [
    
    {'id': '419870', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '418986', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '411699', 'class': 'item-category indolj-container large_icons_menu_2'},
    {'id': '410905', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '415379', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '405790', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '415969', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '400804', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '402998', 'class': 'item-category indolj-container large_icons_menu'},   
    {'id': '400809', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '415381', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '400808', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '418005', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '418004', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '400801', 'class': 'item-category indolj-container large_icons_menu'},   
    {'id': '401107', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '401108', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '405807', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '405802', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '401505', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '408687', 'class': 'item-category indolj-container large_icons_menu'},   
    {'id': '406861', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '414594', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '401104', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '405810', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '400803', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '400800', 'class': 'item-category indolj-container large_icons_menu'},   
    {'id': '401106', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '400799', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '405806', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '400810', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '400802', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '415378', 'class': 'item-category indolj-container large_icons_menu'},

]


extract_and_save_menu('UnitedKing.html', 'UnitedKing_menu_items.html', div_ids_and_classes)

time.sleep(1.5)

# os.remove('UnitedKing.html')

# extract_food_menu_1('UnitedKing_menu_items.html', 'UnitedKing_Combined_Menu.json')   


# time.sleep(2)


# os.remove('Kaybees_menu_items.html')


# input_file = 'Kaybees_Combined_Menu.json'

# output_file = 'Kaybees_Combined_Menu.json'

# add_brand_name_to_products(input_file, output_file)


# separate_deals_and_normal('Kaybees_Combined_Menu.json')

# time.sleep(1)

# os.remove('Kaybees_Combined_Menu.json')

# print("All Done")



