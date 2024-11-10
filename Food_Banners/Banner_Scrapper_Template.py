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


def save_banners_content():
    url = "https://www.delizia.pk/"
    webbrowser.open(url)
    time.sleep(5)


    pyautogui.hotkey('ctrl', 'shift', 'c')
    time.sleep(2)
    pyautogui.hotkey('ctrl', ']')
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(4)

    js_command = 'copy(document.getElementsByClassName("carousel slide")[0].outerHTML);'
    pyautogui.write(js_command)
    time.sleep(2.5)
    pyautogui.press('enter')
    time.sleep(1.5)

    html_content = pyperclip.paste()
    
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.split('.')[0]  
    file_name = f"url.html"

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML content has been saved to {os.path.abspath(file_name)}")

    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1.3)
    


def extract_food_menu_1(input_html, output_json):
    with open(input_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    div= soup.find_all('div', class_='position-relative w-100 carousel-img-container')
    

    
    deals = []

    for div in div:
        deal = {}
  


        img_tag = div.find('img', class_='')
        if img_tag and img_tag.get('src'):
            img_url = img_tag['src']
            deal['product_image'] = "https://www.delizia.pk"+img_url

        if deal:
            deals.append(deal)

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(deals, json_file, indent=4)

    print(f"Data has been successfully saved to {output_json}")





# -------------------------------------------------------- Functions Calling ------------------------------------------------------------------#

# print("Automation Started")

# save_banners_content()

# print("Automation Ended and HTML File Created Successfully")


extract_food_menu_1('url.html', 'delizia_Banners.json')   



























