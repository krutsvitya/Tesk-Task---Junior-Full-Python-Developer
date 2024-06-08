import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Collecting all links from main page
url = 'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 "
                   "Safari/537.36"

}

req = requests.get(url, headers=headers)

links = list()
src = req.text
soup = BeautifulSoup(src, features="html.parser")
all_products_links = soup.find_all('a', class_="cmp-category__item-link")
for link in all_products_links:
    links.append('https://www.mcdonalds.com/' + link.get('href'))


#Collecting all data from pages with items
all_data = []
for link in links:
    req = requests.get(link, headers=headers)

    src = req.text

    driver_path = 'E:/chromedriver-win64/chromedriver.exe'

    service = Service(executable_path=driver_path)

    driver = webdriver.Chrome(service=service)

    driver.get(link)

    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.ID, 'accordion-29309a7a60-item-9ea8a10642-button')))

    button.click()

    wait.until(EC.visibility_of_element_located((By.ID, 'accordion-29309a7a60-item-9ea8a10642')))

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser'
                               '')
    list_content = soup.find_all(class_='sr-only sr-only-pd')
    list_content2 = soup.find_all(class_='label-item')

    all_content = list_content + list_content2

    energy_value = list()
    for content in all_content:
        if content not in energy_value:
            energy_value.append(content.text.strip())

    nutrient_content = list()
    for content in list_content2:
        item_content = content.find('span', class_='sr-only')
        if item_content not in nutrient_content:
            nutrient_content.append(item_content)

    #Group all data in dict
    data = {
        'name': soup.find('title').text,
        'description': soup.find(class_='cmp-text').text.replace('\xa0', ' ').replace('\n', ' ').replace('\t', ' ')
    }
    if len(nutrient_content) > 2:
        data['calories'] = energy_value[3]
        data['fats'] = energy_value[6]
        data['carbs'] = energy_value[9]
        data['proteins'] = energy_value[12]
        data['unsaturated fats'] = nutrient_content[0].text.splitlines()[1].strip()
        data['sugar'] = nutrient_content[1].text.splitlines()[1].strip()
        data['salt'] = nutrient_content[2].text.splitlines()[1].strip()
        if len(nutrient_content) > 3:
            data['portion'] = nutrient_content[3].text.splitlines()[1].strip()

    all_data.append(data)

# Write data in json
with open('data.json', 'a') as file:
    json.dump(all_data, file, indent=4)
    file.write('\n')

with open('data.json', 'r') as file:
    data = json.load(file)

print(data)


