
from bs4 import BeautifulSoup

def extract_and_save_menu(input_html, output_html, div_ids_and_classes):


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
    {'id': '7306', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7388', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7389', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '40363', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7310', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7328', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7311', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7312', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7313', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7314', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7315', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7329', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7316', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7320', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7338', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '402916', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7321', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7318', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7317', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '7322', 'class': 'item-category indolj-container list_menu_three'},
    {'id': '403522', 'class': 'item-category indolj-container'},
    {'id': '7323', 'class': 'item-category indolj-container list_menu_three'}
]


extract_and_save_menu('foodsinn.html', 'foodsinn_menu_items.html', div_ids_and_classes)
