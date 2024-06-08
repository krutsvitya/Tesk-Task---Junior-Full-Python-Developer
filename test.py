import requests

URL = 'http://127.0.0.1:5000'

response = requests.get(f'{URL}/all_products/')

if response.status_code == 200:
    print(response.json())

else:
    print(f"Error: {response.status_code}")

response = requests.get(f'{URL}/products/Роял Чізбургер')
if response.status_code == 200:
    product_data = response.json()
    print(product_data)

else:
    print(f"Error: {response.status_code}")


response = requests.get(f'{URL}/products/Курячі Стріпси, 3 штуки/description')
if response.status_code == 200:
    product_data = response.json()
    print(product_data)

else:
    print(f"Error: {response.status_code}")

