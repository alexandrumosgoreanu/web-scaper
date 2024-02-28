import csv
import requests
from bs4 import BeautifulSoup
import re

# Read csv file with the domain names and return the array containg the URL as strings
def read_csv(file_name):
    domain = []
    with open(file_name, mode='r', newline='') as csv_file:
        data = csv.reader(csv_file)
        line_count = 0
        for row in data:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                # print(type("".join(row)))
                domain.append("".join(row).replace("[","").replace("]",""))
            line_count += 1
            # print(f'\t{row["domain"]}')
        print(f'Processed {line_count} lines.')
    return domain



domains_list = read_csv('./data/sample-websites.csv')
# print(domains_list[1])

phone_regex = re.compile(r'''(
                        (?:\+?(\d{1,3}))?
                        (\d{3}|\(\d{3}\))+
                        (\s|-|\.)+
                        (\d{3})+
                        (\s|-|\.)+
                        (\d{4})+
                        (\s*(ext|x|ext.)\s*(\d{2,5}))?)''', re.VERBOSE)

address_regex = re.compile(r'''(
                           [0-9]+
                           [\s]*
                           [a-zA-Z\s.\-\,\#]+
                           (\b([A|a]venue|[A|a]ve|[C|c]ourt|[C|c]t|[S|s]treet|[S|s]t|[D|d]rive|[D|d]r|[L|l]ane|[L|l]n|[R|r]oad|[R|r]d|[B|b]lvd|[P|p]laza|[P|p]arkway|[P|p]kwy))+
                           [\s]?
                           [a-zA-Z0-9.\-\,\#]+
                           [a-zA-Z0-9\s.\-\,\#]*
                           [0-9]{5})''', re.VERBOSE)
pobox_regex = re.compile(r'''(\b(PO|Post)+[a-zA-Z\s0-9.\-\,\#]*[0-9]{5})''')
                         
# email_regex = re.compile(r'''(
#                         [a-zA-Z0-9._%+-]+
#                         @
#                         [a-zA-Z0-9.-]+
#                         (\.[a-zA-Z]{2,4}))''', re.VERBOSE)

social_media_regex = re.compile(r'^(http[s])?(://)?(www.)?(facebook|instagram|twitter|tiktok|linkedin|youtube)+(.com[/in])+[/a-zA-Z0-9.\-\,\#]*$')


url = "http://" + domains_list[3]
print(url)
page = requests.get(url)
page_html = str(page.content) 

def extract_phone(soup):
    matches = set()
    for groups in phone_regex.findall(soup):
        print(groups)
        phone_numbers = '-'.join([groups[1], groups[3], groups[5]])
        if groups[8] != '':
                phone_numbers += ' x' + groups[8]            
        matches.add("".join(groups[0]))

    return matches

def extract_address(soup):
    matches = set()
    for groups in address_regex.findall(soup):
        matches.add("".join(groups[0]))
    if len(matches) == 0:
        for groups in pobox_regex.findall(soup):
            matches.add("".join(groups[0]))
    return matches

def extract_links(links, url):
    matches = set()
    contact_page_matches = set()
    contact_page_regex = re.compile(fr'(http[s]://)+(www.)?({url[7:]}/)+(contact|about)+[a-zA-Z0-9.\-\,\#]*')

    for link in links:
        if social_media_regex.match(link):
            matches.add(link)
        elif contact_page_regex.match(link):
            contact_page_matches.add(link)
    return matches, contact_page_matches

# def extract_email(soup):
#     matches = set()
#     for groups in email_regex.findall(soup):
#         matches.add("".join(groups[0]))
#     return matches


soup = BeautifulSoup(page.content, "lxml")          # parsing with lxml for speed vs. html.parser
links = [link['href'] for link in soup.find_all('a', href = True)]           # getting all the links
soup_text = soup.get_text(" ", strip=True)           # converting to text in order to match phone and address

with open('soup.txt', 'w', encoding="utf-8") as f:
    f.write(soup.prettify())

social_media, contact_page = extract_links(links, url)
phone = extract_phone(soup_text)
# address = extract_address(soup.get_text())

print(contact_page)
print(social_media)
print(phone)
# print(address)
# with open('soup.txt', 'w', encoding="utf-8") as f:
#     for item in links:
#         f.write(item+'\n')

# for result in soup.findAll('div'):
#     # title = result['title']
#     # link = result.find('a')['href']
#     snippet = result['snippet']

#     # match_email = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', snippet)
#     # email = ''.join(match_email)

#     match_phone = re.findall(phone_regex, snippet)
#     phone = ''.join(match_phone)
    
    # address = re.findall('\s[0-9]{5}\s+[a-zA-ZäöüÄÖÜ]+',html_text)
    
    # print('f\n{link}\n{phone}\n')
# results = soup.find()