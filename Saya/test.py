import requests
from bs4 import BeautifulSoup
import time
import json
import os


def scrape_saya_sales(num_pages, output_file):

    base_url = "https://saya.pk/collections/summer-season-end-sale-upto-50-off-on-stitched-unstitched-printed-embroidered-lawn-cotton-jacqaurd-cambric-chiffon-all-fabric?page="


    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('<html><body>')
        file.write('<h1>Sale Items</h1>')
        file.write('<div class="products">')  

      
        for page in range(1, num_pages + 1):
        
            url = f"{base_url}{page}"
            
         
            response = requests.get(url)

    
            if response.status_code == 200:
             
                soup = BeautifulSoup(response.content, 'html.parser')

             
                
                sale_items = soup.find_all('div', class_='t4s-product-wrapper')
               

           
                for item in sale_items:
                    
                    file.write(str(item))  
        
            else:
                print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

        file.write('</div>')  
        file.write('</body></html>')

    print(f"Data scraped and saved to {output_file}")
    
    
    
def extract_saya_data(file_path, output_file):

    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    

    soup = BeautifulSoup(html_content, "html.parser")
    products = []


    product_items = soup.find_all("div", class_="t4s-product-wrapper")
    
    for item in product_items:
        product_data = {}

   
        # image_tag = item.find("img", class_="t4s-product-main-img")
        # if image_tag:
        product_data['image_url'] = item.find("noscript").find("img", class_="t4s-product-main-img")['src'] if item.find("noscript") else None

     
        link_tag = item.find("a", class_="t4s-full-width-link")
        if link_tag:
            product_data['product_page'] = "https://saya.pk/collections/summer-season-end-sale-upto-50-off-on-stitched-unstitched-printed-embroidered-lawn-cotton-jacqaurd-cambric-chiffon-all-fabric"+link_tag.get("href")

 
        title_tag = item.find("h3", class_="t4s-product-title").find("a")
        if title_tag:
            product_data['title'] = title_tag.get_text(strip=True)

      
        price_div = item.find("div", class_="t4s-product-price")
        if price_div:
            price_spans = price_div.find_all("span", class_="money")
            if len(price_spans) > 1:
                product_data['sale_price'] = price_spans[0].get_text(strip=True)
                product_data['orignal_price'] = price_spans[1].get_text(strip=True)
                
                
        product_data['Brand_Name'] = "Saya Clothing"           

        products.append(product_data)


    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(products, json_file, ensure_ascii=False, indent=4)

    print(f"Data has been saved to {output_file}")
    
    
    
    
scrape_saya_sales(num_pages=164, output_file='all_saya_sales.html')        


time.sleep(2)


file_path = "all_saya_sales.html"
output_file = "saya.json"
extract_saya_data(file_path, output_file)

os.remove('all_saya_sales.html')