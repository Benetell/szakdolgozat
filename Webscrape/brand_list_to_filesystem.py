from bs4 import BeautifulSoup
import requests
import os
import re  # Import the re module for regular expressions

my_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, "
                  "like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}

url = "https://interbrand.com/best-global-brands/"
r = requests.get(url, headers=my_headers)
soup = BeautifulSoup(r.text, 'html.parser')

articles = soup.findAll('a', class_="wp-block-interbrand-best-brand-block__link")

for article in articles:
    name = article.find_all("span")[1].text
    worth = article.find_all("span")[3].text
    img = article.div.figure.img['src']

    # Sanitize brand name for a valid filename
    sanitized_name = re.sub(r'\W+', '', name)

    # Construct the file name
    file_name = f"{sanitized_name}.{img.split('.')[-1]}"

    # Use a relative path or provide the directory path as a parameter
    base_directory = r"\Users\bened\codes\images\val"
    directory_path = os.path.join(base_directory, sanitized_name)
    os.makedirs(directory_path, exist_ok=True)

    try:
        brand = requests.get(img, headers=my_headers)
        brand.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f'Error getting {file_name}: {e}')
    else:
        with open(os.path.join(directory_path, file_name), 'wb') as f:
            #f.write(brand.content)
            print(name)

