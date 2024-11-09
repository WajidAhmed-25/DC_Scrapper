from bs4 import BeautifulSoup

def extract_and_save_deals(input_html, output_html, div_ids_and_classes):
    """
    Extract specific <div> elements from an HTML file and save them to a new HTML file.

    Parameters:
    - input_html (str): Path to the input HTML file.
    - output_html (str): Path to the output HTML file where the result will be saved.
    - div_ids_and_classes (list of dicts): A list of dictionaries containing 'id' and 'class' keys
      for identifying the <div> elements to extract.

    Returns:
    - None
    """
    

    with open(input_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')


    new_soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
    new_body = new_soup.body


    for div_info in div_ids_and_classes:
        div = soup.find('div', div_info)
        if div:
            new_body.append(div)

 
    with open(output_html, 'w', encoding='utf-8') as file:
        file.write(str(new_soup))

    print(f"The specified divs have been saved to {output_html}.")


div_ids_and_classes = [
    {'id': '8376', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7319', 'class': 'item-category indolj-container list_menu_three'}
]

extract_and_save_deals('foodsinn.html', 'foodsinn_deals.html', div_ids_and_classes)
