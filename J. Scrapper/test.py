import requests
from bs4 import BeautifulSoup
import time
import json
import os




def scrape_junaids_sales(num_pages, output_file):

    base_url = "https://www.junaidjamshed.com/sale.html?p="


    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('<html><body>')
        file.write('<h1>Sale Items</h1>')
        file.write('<div class="products">')  

      
        for page in range(1, num_pages + 1):
        
            url = f"{base_url}{page}"
            
         
            response = requests.get(url)

    
            if response.status_code == 200:
             
                soup = BeautifulSoup(response.content, 'html.parser')

             
                
                sale_items = soup.find_all('div', class_='product-item-info')
               

           
                for item in sale_items:
                    
                    file.write(str(item))  
        
            else:
                print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

        file.write('</div>')  
        file.write('</body></html>')

    print(f"Data scraped and saved to {output_file}")
    
    


def extract_product_data_from_file(file_path, output_file):
 
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    

    soup = BeautifulSoup(html_content, "html.parser")
    products = []

   
    product_items = soup.find_all("div", class_="product-item-info hover-animation-none")
    
    for item in product_items:
        product_data = {}

     
        image_tag = item.find("img", class_="product-image-photo")
        if image_tag:
            product_data['image_url'] = image_tag.get("data-original")

      
        link_tag = item.find("a", class_="product-item-link")
        if link_tag:
            product_data['product_page'] = link_tag.get("href")
            product_data['title'] = link_tag.get_text(strip=True)

    
        price_box = item.find("div", class_="price-box price-final_price")
        if price_box:
           
            special_price_tag = price_box.find("span", {"data-price-type": "finalPrice"})
            if special_price_tag:
                product_data['sale_price'] = special_price_tag.get_text(strip=True)

        
            old_price_tag = price_box.find("span", {"data-price-type": "oldPrice"})
            if old_price_tag:
                product_data['original_price'] = old_price_tag.get_text(strip=True)
                
                
        product_data['Brand_Name'] = "J. Clothing"    
        
   

        products.append(product_data)

   
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(products, json_file, ensure_ascii=False, indent=4)

    print(f"Data has been saved to {output_file}")



#----------------------------------------------------------- Function Calling ==============================================================#
 
 
scrape_junaids_sales(num_pages=6, output_file='all_j._sales.html')    



file_path = "all_j._sales.html"
output_file = "junaid_jamshed.json"
extract_product_data_from_file(file_path, output_file)

os.remove('all_j._sales.html')