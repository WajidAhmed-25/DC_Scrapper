import json
import re

def calculate_discount_and_difference():

    with open('all_dhanak_sales.json', 'r') as file:
        data = json.load(file)
    
    modified_data = []

    for product in data:
     
        original_price = float(re.sub(r'\D', '', product['original_price']))
        sale_price = float(re.sub(r'\D', '', product['sale_price']))
        

        amount_difference = original_price - sale_price
        discount_percentage = (amount_difference / original_price) * 100
        
        modified_product = product.copy()
        modified_product['amount_difference'] = amount_difference
        modified_product['discount_percentage'] = discount_percentage
        
        modified_data.append(modified_product)
    

    with open('modified_all_dhanak_sales.json', 'w') as file:
        json.dump(modified_data, file, indent=4)


calculate_discount_and_difference()
