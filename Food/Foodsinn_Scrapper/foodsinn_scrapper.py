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
    url = "https://foodsinn.co/"
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
    file_name = f"{domain_name}.html"

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML content has been saved to {os.path.abspath(file_name)}")

    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1.3)




def extract_and_save_deals(input_html, output_html, div_ids_and_classes):
  
    """
    Extract specific <div> elements from an HTML file and save them to a new HTML file.

    Parameters:
    - input_html (str): Path to the input HTML file.
    - output_html (str): Path to the output HTML file where the result will be saved.
    - div_ids_and_classes (list of dicts): A list of dictionaries containing 'id' and 'class' keys
      for identifying the <div> elements to extract.

    Returns:
    - None
    """

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





def add_brand_name_to_products(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    for product in data:

        product["brand_name"] = "Foods Inn"


        match = re.search(r'%7C(\d+)', product["product_url"])
        if match:
            number = match.group(1)
           
            if number == '8376':
                product["food_category"] = "Deal"
            
            elif number == '7319':
                product["food_category"] = "Deal"
                
            elif number == '7306':
                product["food_category"] = "Starter"   
                
            elif number == '7308':
                product["food_category"] = "Burger"
                
            elif number == '7309':
                product["food_category"] = "Sandwich" 
                
            elif number == '403363':
                product["food_category"] = "Sancwich"  
                   
            elif number == '7310':
                product["food_category"] = "Broast" 
                      
            elif number == '7328':
                product["food_category"] = "Steak"       
                     
                  
            elif number == '7311':
                product["food_category"] = "Pasta"  
                   
            elif number == '7312':
                product["food_category"] = "Chinese" 
                      
            elif number == '7313':
                product["food_category"] = "Chinese"     
                
                    
            elif number == '7314':
                product["food_category"] = "BBQ"  
                   
            elif number == '7315':
                product["food_category"] = "Chicken Karahi" 
                      
            elif number == '7329':
                product["food_category"] = "Mutton Karahi"    
                  
            elif number == '7316':
                product["food_category"] = "Handi"  
                   
            elif number == '7320':
                product["food_category"] = "Platter" 
                      
            elif number == '7338':
                product["food_category"] = "Roll"     
                         
            elif number == '402916':
                product["food_category"] = "Kid" 
                    
            elif number == '7321':
                product["food_category"] = "Naan"     
                          
            elif number == '7318':
                product["food_category"] = "Dessert" 
                      
            elif number == '7317':
                product["food_category"] = "Mocktail or Shake"     
                           
            elif number == '7322':
                product["food_category"] = "Beverage" 
                      
            elif number == '403522':
                product["food_category"] = "Hot Beverage"     
                           
            elif number == '7323':
                product["food_category"] = "Add Ons" 
                      
                            

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)





# -------------------------------------------------------- Functions Calling ------------------------------------------------------------------#

print("Automation Started")

save_html_content()

print("Automation Ended and HTML File Created Successfully")


time.sleep(1)

div_ids_and_classes = [
    {'id': '8376', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7319', 'class': 'item-category indolj-container list_menu_three'}
]

extract_and_save_deals('foodsinn.html', 'foodsinn_deals.html', div_ids_and_classes)

time.sleep(1)


div_ids_and_classes = [
    {'id': '7306', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7388', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7389', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '40363', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7310', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7328', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7311', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7312', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7313', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7314', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7315', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7329', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7316', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7320', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7338', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '402916', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7321', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7318', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7317', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7322', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '403522', 'class': 'item-category indolj-container'},
    {'id': '7323', 'class': 'item-category indolj-container list_menu_three'}
]


extract_and_save_menu('foodsinn.html', 'foodsinn_menu_items.html', div_ids_and_classes)

time.sleep(1.5)

os.remove('foodsinn.html')

time.sleep(1.5)

extract_food_deals('foodsinn_deals.html', 'foodsinn_deals.json')

time.sleep(1.5)

extract_food_menu('foodsinn_menu_items.html', 'foodsinn_menu_items.json')   

time.sleep(1)

os.remove('foodsinn_menu_items.html')

os.remove('foodsinn_deals.html')


input_file = 'foodsinn_deals.json'

output_file = 'foodsinn_deals.json'

add_brand_name_to_products(input_file, output_file)

time.sleep(1)

input_file = 'foodsinn_menu_items.json'

output_file = 'foodsinn_menu_items.json'

add_brand_name_to_products(input_file, output_file)



print("All Done")






