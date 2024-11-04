import requests
from bs4 import BeautifulSoup
import time
import json
import os





def scrape_alkaram_sales(num_pages, output_file):

    base_url = "https://www.alkaramstudio.com/collections/sale?page="


    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('<html><body>')
        file.write('<h1>Sale Items</h1>')
        file.write('<div class="products">')  

      
        for page in range(1, num_pages + 1):
        
            url = f"{base_url}{page}"
            
         
            response = requests.get(url)

    
            if response.status_code == 200:
             
                soup = BeautifulSoup(response.content, 'html.parser')

             
                
                sale_items = soup.find_all('div', class_='t4s-product')
               

           
                for item in sale_items:
                    
                    file.write(str(item))  
        
            else:
                print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

        file.write('</div>')  
        file.write('</body></html>')

    print(f"Data scraped and saved to {output_file}")
    
def scrape_product_data(file_path, output_json):
  
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
  
    products = soup.find_all("div", class_="t4s-product")


    product_data = []
    for product in products:
    
        if 't4s-pr-grid' in product.get("class", []) and 't4s-pr-style1' in product.get("class", []):
                       
            image_url = product.find("noscript").find("img", class_="t4s-product-main-img")['src'] if product.find("noscript") else None

            
            title_tag = product.find("h3", class_="t4s-product-title")
            title = title_tag.get_text(strip=True) if title_tag else None
            link_tag = title_tag.find("a") if title_tag else None
            href = link_tag['href'] if link_tag else None
            
         
            price_div = product.find("div", class_="t4s-product-price")
            original_price = price_div.find("del").get_text(strip=True) if price_div and price_div.find("del") else None
            sale_price = price_div.find("ins").get_text(strip=True) if price_div and price_div.find("ins") else None
            
            
            Brand_name = "Alkaram Studio"
            
  
            product_data.append({
                'title': title,
                'product_page': "https://www.alkaramstudio.com/collections/sale"+href,
                'image_url':"https:"+image_url,
                'original_price': original_price,
                'sale_price': sale_price,
                'Brand_Name':Brand_name
            })
    

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(product_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Data successfully saved to {output_json}")

    
# ----------------------------------------------------- Function Calling -------------------------------------------------------------------#    


scrape_alkaram_sales(num_pages=147, output_file='all_alkaram_sales.html')


time.sleep(2)

file_path = 'all_alkaram_sales.html'
output_json = 'all_Alkaram_sales.json'
scrape_product_data(file_path, output_json)

time.sleep(1)

os.remove('all_alkaram_sales.html')