import requests
from bs4 import BeautifulSoup
import os
import json
import time 
import re






def get_last_url(image_urls):

    if isinstance(image_urls, list):
    
        url_string = image_urls[0]
    else:
        url_string = image_urls
    

    urls = url_string.split(',')
    
    last_url = urls[-1].strip()
    

    url = last_url.split(' ')[0]
    

    if url.startswith('//'):
        url = 'https:' + url
        
    return url






def scrape_dhanak_sales(num_pages, output_file):

    base_url = "https://dhanak.com.pk/collections/sale?page="


    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('<html><body>')
        file.write('<h1>Sale Items</h1>')
        file.write('<div class="products">')  

      
        for page in range(1, num_pages + 1):
        
            url = f"{base_url}{page}"
            
         
            response = requests.get(url)

    
            if response.status_code == 200:
             
                soup = BeautifulSoup(response.content, 'html.parser')

             
                
                sale_items = soup.find_all('li', class_='product')
               

           
                for item in sale_items:
                    
                    file.write(str(item))  
        
            else:
                print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

        file.write('</div>')  
        file.write('</body></html>')

    print(f"Data scraped and saved to {output_file}")





scrape_dhanak_sales(num_pages=5, output_file='all_dhanak_sales.html')

time.sleep(2) 


with open("all_dhanak_sales.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

products = soup.find_all("li", class_="product")

product_list = []

for product in products:
    title_tag = product.find("a", class_="card-title link-underline card-title-ellipsis")
    title = title_tag.find("span", class_="text").get_text(strip=True) if title_tag else "Unknown"
    
    product_url = title_tag["href"] if title_tag else "Unknown"
    

    card_media_div = product.find('div', class_='card-media card-media--adapt media--hover-effect media--loading-effect')
    
    clean_url = "Unknown"  
    if card_media_div:
        image_tag = card_media_div.find("img", alt=True)
    
        if image_tag and "data-srcset" in image_tag.attrs:
            data_srcset = image_tag["data-srcset"].split(", ")
    
     
         
            result = get_last_url(data_srcset)
         #   print(result)
            
            
            
            
            
        else:
            print("No 'data-srcset' attribute found.")
    else:
        print("No div with the specified class found.")
      
      
    price_sale_div = product.find("div", class_="price__sale")
    
    if price_sale_div:
        original_price_tag = price_sale_div.find("s", class_="price-item--regular")
        sale_price_tag = price_sale_div.find("span", class_="price-item--sale")
        original_price = original_price_tag.get_text(strip=True) if original_price_tag else "Unknown"
        new_original_price = original_price.replace("Rs.", "Rs. ")
        
        formatted_org_price = re.match(r"(Rs\. \d{1,3}(?:,\d{3})*)", new_original_price).group(0)
        
        if "Rs." in formatted_org_price:
            trimmed_price = formatted_org_price.replace("Rs. ", "").strip()
        else:
            trimmed_price = formatted_org_price.strip()
        
        
        
        sale_price = sale_price_tag.get_text(strip=True) if sale_price_tag else "Unknown"
        new_sales_price = sale_price.replace("Rs.", "Rs. ")
        
        match = re.match(r"(Rs\. \d{1,3}(?:,\d{3})*)", new_sales_price)
        
        if match:
            formatted_sale_price = match.group(0)
            if "Rs." in formatted_sale_price:
                numeric_price = formatted_sale_price.split("Rs.")[-1].strip()
            else:
                numeric_price = formatted_sale_price.strip() 
            
        else:
            formatted_sale_price = new_sales_price
    else:
        formatted_org_price = "Unknown"
        formatted_sale_price = "Unknown"
    
    product_info = {
        "title": title,
        "product_url": "https://dhanak.com.pk" + product_url,
        "image_url": result,
        "original_price": trimmed_price,
        "sale_price": numeric_price,
        "Brand_Name": "Dhanak Clothing"
    }
    product_list.append(product_info)

with open("all_dhanak_sales.json", "w", encoding="utf-8") as json_file:
    json.dump(product_list, json_file, ensure_ascii=False, indent=4)

print("JSON file has been created successfully.")   

time.sleep(2)

os.remove('all_dhanak_sales.html')

