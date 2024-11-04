import json
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from decimal import Decimal, InvalidOperation
import os

def calculate_discount(original_price, sale_price):
    try:
        # Remove "Rs." and commas, and convert to decimal
        original_price_num = Decimal(re.sub(r'[^\d]', '', original_price)) / 100
        sale_price_num = Decimal(re.sub(r'[^\d]', '', sale_price)) / 100
        
        # Calculate amount difference and discount percentage
        amount_difference = original_price_num - sale_price_num
        discount_percentage = (amount_difference / original_price_num) * 100

        # Debug prints to check values
        print(f"Original Price: {original_price_num}, Sale Price: {sale_price_num}")
        print(f"Amount Difference: {amount_difference}, Discount Percentage: {discount_percentage}")

        return float(amount_difference), float(discount_percentage)
    except (InvalidOperation, ZeroDivisionError):
        # Return 0 for both fields if there is an error in conversion
        return 0, 0

def process_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    

    for item in data:
        original_price = item.get("original_price", "")
        sale_price = item.get("sale_price", "")
        
        amount_difference, discount_percentage = calculate_discount(original_price, sale_price)
        
        # Add the new fields
        item["amount_difference"] = f"Rs. {amount_difference:,.2f}"
        item["discount_percentage"] = f"{discount_percentage:.2f}%"
    
  
    output_file = os.path.join("all_dhanak_discount_Calculator.json")
    
   
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
    
    messagebox.showinfo("Success", f"File saved successfully as {output_file}")

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        process_file(file_path)


root = tk.Tk()
root.title("JSON Discount Calculator")


open_button = tk.Button(root, text="Select JSON File", command=open_file_dialog)
open_button.pack(pady=20)

root.geometry("300x150")
root.mainloop()
