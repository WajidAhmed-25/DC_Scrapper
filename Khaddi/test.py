import requests
from bs4 import BeautifulSoup
import os
import json
import time 



def scrape_khaadi_sales():
    url = "https://pk.khaadi.com/sale/?start=0&sz=1109"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        
        with open("khaadi_sales.html", "w", encoding="utf-8") as file:
            file.write(response.text)
        
        print("Content saved to all_khaadi_sales.html")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)




def filter_khaadi_sales():
    input_file = "khaadi_sales.html"
    output_file = "filtered.html"
    
    with open(input_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    filtered_divs = soup.find_all("div", class_="tile col-6 col-md-4 col-lg-3")
    

    for div in filtered_divs:
        for script in div.find_all("script"):
            script.decompose()
    
    filtered_soup = BeautifulSoup("<html><body></body></html>", "html.parser")
    for div in filtered_divs:
        filtered_soup.body.append(div)
    
   
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(filtered_soup.prettify())
    
    print(f"Filtered content saved to {output_file}")
    




def parse_khaadi_html():
   
    with open("filtered.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
  
    products_data = []

   
    for div in soup.find_all("div", class_="tile col-6 col-md-4 col-lg-3"):
        product_info = {}
        
        
        product_info['Brand_Name'] = "Khaadi Clothing"
        
      
        image_tag = div.find("img", class_="tile-image")
        if image_tag:
            product_info['image_url'] = image_tag.get("src")

    
        anchor_tag = div.find("a", class_="plp-tap-mobile plpRedirectPdp")
        if anchor_tag:
            product_info['product_page'] = "https://pk.khaadi.com"+anchor_tag.get("href")

    
        product = div.find("div", class_="product")
        if product:
            gtm_data = product.get("data-gtmdata")
            if gtm_data:
                gtm_json = json.loads(gtm_data)
                product_info['title'] = gtm_json.get("name")
                product_info['category'] = gtm_json.get("category")
        
       
        sales_price_span = div.find("span", class_="sales reduced-price d-inline-block")
        if sales_price_span:
            sale_price_value = sales_price_span.find("span", class_="value cc-price")
            if sale_price_value:
                product_info['sale_price'] = sale_price_value.get("content")

     
        original_price_span = div.find("span", class_="strike-through list")
        if original_price_span:
            original_price_value = original_price_span.find("span", class_="value cc-price")
            if original_price_value:
                product_info['original_price'] = original_price_value.get("content")

      
      
        
        products_data.append(product_info)

 
    with open("all_khaadi.json", "w", encoding="utf-8") as json_file:
        json.dump(products_data, json_file, indent=4, ensure_ascii=False)




# -------------------------------------------------------------------------------------------------------------------------------------#




scrape_khaadi_sales()

time.sleep(2)


filter_khaadi_sales()    

time.sleep(2)

os.remove('khaadi_sales.html')

time.sleep(2)

parse_khaadi_html()

os.remove('filtered.html')

