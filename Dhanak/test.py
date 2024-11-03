import requests
from bs4 import BeautifulSoup
import os
import json
import time 



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

