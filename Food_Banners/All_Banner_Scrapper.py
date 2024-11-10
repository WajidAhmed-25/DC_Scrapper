

#######################################################################################################################################




# -------------------------------------------------------- Libraries Declaration ------------------------------------------------------------------#

import pyautogui
import webbrowser
import time
import os
import pyperclip
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
import re

# -------------------------------------------------------- Functions Declaration ------------------------------------------------------------------#

def save_banners_content(url):
    webbrowser.open(url)
    time.sleep(8)

    pyautogui.hotkey('ctrl', 'shift', 'c')
    time.sleep(3)
    pyautogui.hotkey('ctrl', ']')
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(5)

    js_command = 'copy(document.getElementsByClassName("carousel slide")[0].outerHTML);'
    pyautogui.write(js_command)
    time.sleep(2.5)
    pyautogui.press('enter')
    time.sleep(1.5)

    html_content = pyperclip.paste()
    file_name = "url.html"

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML content for {url} has been saved to {os.path.abspath(file_name)}")
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1.3)
    return file_name


def extract_food_menu(input_html, output_json, url):
    with open(input_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    divs = soup.find_all('div', class_='position-relative w-100 carousel-img-container')
    
    images = []

    for div in divs:
        img_tag = div.find('img', class_='')
        if img_tag and img_tag.get('src'):
            img_url = img_tag['src']
            full_img_url = f"{url}{img_url}"
            images.append(full_img_url)


    if os.path.exists(output_json):
        with open(output_json, 'r', encoding='utf-8') as json_file:
            all_data = json.load(json_file)
    else:
        all_data = {}


    all_data[url] = images

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, indent=4)

    print(f"Data for {url} has been successfully appended to {output_json}")


    os.remove(input_html)
    print(f"Temporary file {input_html} has been removed.")


# -------------------------------------------------------- Main Execution ------------------------------------------------------------------#

print("Automation Started")

output_json = 'All_Banners.json'
urls_file = 'Sites_Urls.txt'

with open(urls_file, 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

for url in urls:
    html_file = save_banners_content(url)
    extract_food_menu(html_file, output_json, url)

print("Automation Ended, and JSON File Created/Updated Successfully")



























