import requests
from bs4 import BeautifulSoup
from extraction_helpers import *
from selenium_driver import *
from csv_helpers import *


domains_list = read_domains('./data/sample-websites.csv')       # read domains from csv
# print(domains_list[1])

url = "http://" + domains_list[8]
print(url)
page = requests.get(url)                            # make request to url
page_html = str(page.content) 

soup = BeautifulSoup(page.content, "lxml")          # parsing with lxml for speed vs. html.parser

body = soup.find('body').get_text()
print(len(body))
if(len(body) < 100):        # server side rendered website that needs to be accessed through selenium. TODO: find better metric to evaluate whether a site is client side rendered or not
    print(True)
    rendered_html = get_rendered_html(url)
    soup = BeautifulSoup(rendered_html, "lxml")

links = [link['href'] for link in soup.find_all('a', href = True)]           # getting all the links before extracting just the text from the bs object

soup_text = soup.get_text(" ", strip=True)           # converting to text in order to match phone and address


social_media, contact_page = extract_links(links, url)
phone = extract_phone(soup_text)
address = extract_address(soup.get_text())

print(contact_page)
print(social_media)
print(phone)
print(address)

with open('soup.txt', 'w', encoding="utf-8") as f:
    f.write(soup_text)

# with open('soup.txt', 'w', encoding="utf-8") as f:
#     for item in links:
#         f.write(item+'\n')

driver.quit()