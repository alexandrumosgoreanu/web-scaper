import csv
import requests
from bs4 import BeautifulSoup
from lxml import etree
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
                           [0-9]{5})|(\b(PO|Post)+
                           [a-zA-Z0-9\s.\-\,\#]*
                           [0-9]{5})''', re.VERBOSE)
# email_regex = re.compile(r'''(
#                         [a-zA-Z0-9._%+-]+
#                         @
#                         [a-zA-Z0-9.-]+
#                         (\.[a-zA-Z]{2,4}))''', re.VERBOSE)


url = "http://" + domains_list[19]
print(url)
page = requests.get(url)
page_html = str(page.content) 

def search_phone(soup):
    matches = set()
    for groups in phone_regex.findall(soup):
        phone_numbers = '-'.join([groups[1], groups[3], groups[5]])
        if groups[8] != '':
                phone_numbers += ' x' + groups[8]            
        matches.add("".join(groups[0]))

    return matches

def search_address(soup):
    matches = set()
    for groups in address_regex.findall(soup):
        matches.add("".join(groups[0]))
        print(groups)
    return matches

# def search_email(soup):
#     matches = set()
#     for groups in email_regex.findall(soup):
#         matches.add("".join(groups[0]))
#     return matches


soup = BeautifulSoup(page.content, "lxml")



soup = soup.get_text(" ", strip=True)
with open('soup.txt', 'w', encoding="utf-8") as f:
    f.write(soup)
# phone = search_phone(soup)
address = search_address('''PO Box 971201 Boca Raton FL 33497 Top salon - Hair Salon in State College Top salon  View Menu  Call now  Get directions Updates Testimonials Gallery Contact Top salon Hair Salon in State College Opening at 10:00 AM View Menu Call  (814) 954-5812 Get directions WhatsApp  (814) 954-5812 Message  (814) 954-5812 Contact Us Get Quote Find Table Make Appointment Place Order Updates Posted on Feb 20, 2024 Testimonials 6 months ago  Flag as inappropriate I am so happy with my new style!
It was my first time getting a perm in the States. I was not sure because recently I got a bad haircut from a salon in the Magnificent Mile!
The stylist here cut off blunt end of my hair for free and he was super meticulous and detailed.
Yes, he asked for tip at the end but it is part of American culture, so be it. - KeyOne J 4 months ago  Flag as inappropriate Tommy is always very patient to my hair. He has been taking care of my hair for a few years and I am very happy with all the styles he has done for me. This is the most recent style. - Anna X 5 months ago  Flag as inappropriate Very accommodating and they fit you in the schedule quickly.  I appreciate that since I don’t always know my schedule too far in advance.  I think 15% tip is standard so I’m not sure why people are complaining.  Tommy spends a lot of time giving you a quality haircut. - Mary W Write a Review Read More Gallery Contact Us Contact Call now (814) 954-5812 Address Get directions 135 East Beaver Avenue State College, PA 16801 USA Business Hours 7 Mon: 10:00 AM – 8:00 PM Tue: 10:00 AM – 8:00 PM Wed: 10:00 AM – 8:00 PM Thu: 10:00 AM – 8:00 PM Fri: 10:00 AM – 8:00 PM Sat: 10:00 AM – 8:00 PM Sun: 10:00 AM – 8:00 PM Report abuse Header photo  230 Bayshore Blvd. San Francisco, CA 94124 by  Top salon Powered by  Google  Menu  Call  Directions Contact Us ✕ Message sent. We'll get back to you soon. This site uses cookies from Google. Learn more  552 Mass Ave #208, Second Floor, Cambridge, MA 02139. ''')
# print(phone)
print(address)


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