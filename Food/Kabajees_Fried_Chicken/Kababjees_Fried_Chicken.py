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
    url = "https://www.kababjeesfriedchicken.com/"
    webbrowser.open(url)
    time.sleep(8)

    pyautogui.hotkey('ctrl', 'shift', 'c')
    time.sleep(5)
    pyautogui.hotkey('ctrl', ']')
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(2)

    js_command = 'copy(document.getElementsByClassName("items-section-wrapper")[0].outerHTML);'
    pyautogui.write(js_command)
    time.sleep(1.5)
    pyautogui.press('enter')
    time.sleep(2.5)

    html_content = pyperclip.paste()
    
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.split('.')[0]  
    file_name = f"Kababjees_Fried_Chicken.html"

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




    
def extract_food_menu_2(input_html, output_json):
    with open(input_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    div = soup.find_all('div', class_='p-0 mb-3 mb-md-0 large_icons_menu_2-item undefined undefined undefined col-6 col-sm-6 col-md-4 col-lg-4' )


    
    deals = []

    for div in div:
        deal = {}
        
        datacatid = div.get('datacatid', '')
        dataitemid = div.get('dataitemid', '')
        if datacatid and dataitemid:
            deal['product_url'] = f"https://www.kababjeesfriedchicken.com/?item_id={dataitemid}%7C{datacatid}"

        title_tag = div.find('h2', style='color: rgb(33, 37, 41);')
        if title_tag:
            deal['product_title'] = title_tag.get_text(strip=True)

        
        description_tag = div.find('p', style='color: rgb(113, 128, 150);')
        if description_tag:
            deal['product_description'] = description_tag.get_text(strip=True)
        
        else:
            deal['product_description'] = ""


        price_wrapper = div.find('div', class_='price-wrapper pizza-menu-price-wrapper function(){return(0,m.sp)(ue,le,O)} without-border')
        if price_wrapper:
         
             price_tag = price_wrapper.find('span')
             if price_tag:
                 price = price_tag.get_text(strip=True).replace('Rs.', '').strip()
                 if price:
                     deal['product_price'] = price


        img_tag = div.find('img', class_='rounded-0')
        if img_tag and img_tag.get('src'):
            img_url = img_tag['src']
            deal['product_image'] = "https://www.kababjeesfriedchicken.com"+img_url
            
    

        if deal:
            deals.append(deal)

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(deals, json_file, indent=4)

    print(f"Data has been successfully saved to {output_json}")




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
            deal['product_url'] = f"https://www.kababjeesfriedchicken.com/?item_id={dataitemid}%7C{datacatid}"

        title_tag = div.find('h2', style='color: rgb(33, 37, 41);')
        if title_tag:
            deal['product_title'] = title_tag.get_text(strip=True)

        description_tag = div.find('p', class_='truncated trancated-3')
        if description_tag:
            deal['product_description'] = description_tag.get_text(strip=True)

    
    
    price_wrapper = div.find('div', class_='price-wrapper pizza-menu-price-wrapper function(){return(0,m.sp)(ue,le,O)} without-border')
    if price_wrapper:
    
        price_tag = price_wrapper.find('span')
        if price_tag:
            price = price_tag.get_text(strip=True).replace('Rs.', '').strip()
            if price:
                deal['product_price'] = price
    
            img_tag = div.find('img', class_='rounded-0')
            if img_tag and img_tag.get('src'):
                img_url = img_tag['src']
                deal['product_image'] = "https://www.kababjeesfriedchicken.com"+img_url
    
            if deal:
                deals.append(deal)
    
        with open(output_json, 'w', encoding='utf-8') as json_file:
            json.dump(deals, json_file, indent=4)
    
        print(f"Data has been successfully saved to {output_json}")




def merge_json_files(file1, file2, output_file="Kababjees_Fried_Chicken_Menu.json"):

    with open(file1, "r") as f1:
        data1 = json.load(f1)
    
    with open(file2, "r") as f2:
        data2 = json.load(f2)

    merged_data = data1 + data2

    with open(output_file, "w") as output:
        json.dump(merged_data, output, indent=4)
    
    print(f"Merge complete: '{output_file}' created.")





def add_brand_name_to_products(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    for product in data:

        product["brand_name"] = "Kababjees Fried Chicken"


        match = re.search(r'%7C(\d+)', product["product_url"])
        if match:
            number = match.group(1)
           
            if number == '419981':
                product["food_category"] = "Deal"
            
            elif number == '416671':
                product["food_category"] = "Deal"
                
            elif number == '414069':
                product["food_category"] = "Wing"   
                
            elif number == '415886':
                product["food_category"] = "Chicken Bites"
                
            elif number == '415892':
                product["food_category"] = "Starter" 
                
            elif number == '407639':
                product["food_category"] = "Deal"  
                   
            elif number == '407640':
                product["food_category"] = "Deal" 
                      
            elif number == '407641':
                product["food_category"] = "Burger"  
                
            elif number == '416904':
                product["food_category"] = "Kid"              
        
            elif number == '407642':
                product["food_category"] = "Add Ons"        
        
            elif number == '407643':
                product["food_category"] = "Beverage"              
        
          
                 

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)


# -------------------------------------------------------- Functions Calling ------------------------------------------------------------------#

print("Automation Started")

save_html_content()

print("Automation Ended and HTML File Created Successfully")


time.sleep(1)



div_ids_and_classes = [
    {'id': '419981', 'class': 'item-category indolj-container large_icons_menu'},
    {'id': '416671', 'class': 'item-category indolj-container large_icons_menu_2'},
    {'id': '414069', 'class': 'item-category indolj-container large_icons_menu_2'},
    {'id': '415886', 'class': 'item-category indolj-container large_icons_menu_2'},
    {'id': '415892', 'class': 'item-category indolj-container large_icons_menu_2'},
    {'id': '407639', 'class': 'item-category indolj-container large_icons_menu_2'},
    {'id': '407640', 'class': 'item-category indolj-container large_icons_menu_2'},
    {'id': '407641', 'class': 'item-category indolj-container large_icons_menu_2'},
    {'id': '416904', 'class': 'item-category indolj-container large_icons_menu_2'},
    {'id': '407642', 'class': 'item-category indolj-container large_icons_menu_2'},
    {'id': '407643', 'class': 'item-category indolj-container large_icons_menu_2'},

    
]


extract_and_save_menu('Kababjees_Fried_Chicken.html', 'Kababjees_Fried_Chicken_menu_items.html', div_ids_and_classes)

time.sleep(1.5)

os.remove('Kababjees_Fried_Chicken.html')


extract_food_menu_1('Kababjees_Fried_Chicken_menu_items.html', 'Kababjees_Fried_Deals.json')   


time.sleep(2)

extract_food_menu_2('Kababjees_Fried_Chicken_menu_items.html', 'Kababjees_Fried_Menu.json')   

time.sleep(2)


os.remove('Kababjees_Fried_Chicken_menu_items.html')


merge_json_files("Kababjees_Fried_Deals.json", "Kababjees_Fried_Menu.json")

time.sleep(1)

os.remove('Kababjees_Fried_Deals.json')

time.sleep(0.5)

os.remove('Kababjees_Fried_Menu.json')



input_file = 'Kababjees_Fried_Chicken_Menu.json'

output_file = 'Kababjees_Fried_Chicken_Menu.json'

add_brand_name_to_products(input_file, output_file)

time.sleep(1)

print("All Done")



