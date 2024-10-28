import json
import re

def calculate_discount_percentage(original_price, sale_price):

    if original_price is None or sale_price is None:
        return None, None
 
    original_price = float(re.sub(r"[^\d.]", "", str(original_price)))
    sale_price = float(re.sub(r"[^\d.]", "", str(sale_price)))
    
 
    discount_percentage = ((original_price - sale_price) / original_price) * 100

    cost_difference = original_price - sale_price
    return round(discount_percentage, 2), round(cost_difference, 2)

def add_discount_to_products(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    for item in data:
        original_price = item.get("original_price")
        sale_price = item.get("sale_price")
        

        if original_price is not None and sale_price is not None:
            discount_percentage, cost_difference = calculate_discount_percentage(original_price, sale_price)
            item["discount_percentage"] = discount_percentage
            item["cost_difference"] = cost_difference
        else:
            item["discount_percentage"] = None  
            item["cost_difference"] = None 
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Discounted data saved to {output_file}")


add_discount_to_products("all_Alkaram_sales.json", "Alkaram_Discount_Chart.json")
