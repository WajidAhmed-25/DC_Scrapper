import requests
from bs4 import BeautifulSoup
import time
import json
import os




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






def scrape_outfitters_sales(num_pages, output_file):

    base_url = "https://outfitters.com.pk/collections/men-end-of-season-sale?page="


    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('<html><body>')
        file.write('<h1>Sale Items</h1>')
        file.write('<div class="products">')  

      
        for page in range(1, num_pages + 1):
        
            url = f"{base_url}{page}"
            
         
            response = requests.get(url)

    
            if response.status_code == 200:
             
                soup = BeautifulSoup(response.content, 'html.parser')

             
                
                sale_items = soup.find_all('li', class_='grid__item grid-item-list')
               

           
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
    
    product_items = soup.find_all("li", class_="grid__item grid-item-list")
    
    for item in product_items:
        product_data = {}
        
        title_tag = item.find("h3", class_="card__heading h5")
        if title_tag:
            link_tag = title_tag.find("a", class_="product-link-main")
            if link_tag:
                product_data['product_page'] = "https://outfitters.com.pk" + link_tag.get("href")
                product_data['title'] = link_tag.get_text(strip=True)

     
        color_fit_tag = item.find("div", class_="item-label item-swatch-more color-count")
        if color_fit_tag:
            product_data['color'] = color_fit_tag.get_text(strip=True)
            fit_span = color_fit_tag.find("span", class_="fit-meta-span")
            if fit_span:
                fit_text = fit_span.find("span")
                if fit_text:
                    product_data['fit'] = fit_text.get_text(strip=True)
        
      
        image_container = item.find("div", class_="media media--transparent media--hover-effect swiper-slide")
        if image_container:
            image_tag = image_container.find("img", class_="motion-reduce image-second")
            if image_tag and image_tag.get("srcset"):
                result = get_last_url(image_tag.get("srcset"))
                product_data['image_url'] = result

                
                
        price_div = item.find("div", class_="price__sale")
        if price_div:
          
            original_price_tag = price_div.find("s", class_="price-item price-item--regular")
            if original_price_tag:
                money_tag = original_price_tag.find("span", class_="money")
                if money_tag:
                    product_data['original_price'] = money_tag.get_text(strip=True)

          
            sale_price_tag = price_div.find("span", class_="price-item--sale")
            if sale_price_tag:
                    sales_price_value = sale_price_tag.get_text(strip=True)    
                    clean_price = sales_price_value.split('-')[0]
                    product_data['sale_price'] =clean_price
                


        product_data['Brand_Name'] = "Outfitters Clothing"
        

        products.append(product_data)
    

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(products, json_file, ensure_ascii=False, indent=4)

    print(f"Data has been saved to {output_file}")




#----------------------------------------------------------- Function Calling ==============================================================#
 
 
scrape_outfitters_sales(num_pages=37, output_file='all_outfitters_sales.html')    

time.sleep(2)




file_path = "all_outfitters_sales.html"
output_file = "all_outfitters_sales.json"
extract_product_data_from_file(file_path, output_file)

time.sleep(2)

os.remove("all_outfitters_sales.html")


