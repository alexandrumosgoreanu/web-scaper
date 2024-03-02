import time
import json
import math
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from extraction_helpers import *
from selenium_driver import *
from csv_helpers import *
import time
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from threading import Lock
import multiprocessing
from elasticsearch_helpers import *

cpu_count = multiprocessing.cpu_count()
# print(domains_list[1])

# url = "http://" + domains_list[3]
# print(url)
# page = requests.get(url)                            # make request to url
# page_html = str(page.content) 

# soup = BeautifulSoup(page.content, "lxml")          # parsing with lxml for speed vs. html.parser

# body = soup.find('body').get_text()
# print(len(body))
# if(len(body) < 10000):        # server side rendered website that needs to be accessed through selenium. TODO: find better metric to evaluate whether a site is client side rendered or not
    # print(True)
social = 0
ph = 0
adr = 0
down = 0
scraped_data = []
ph_lock = Lock()
social_lock = Lock()
down_lock = Lock()
adr_lock = Lock()
scraped_data_lock = Lock()
total = 0
total_lock = Lock()

def scrape(domains):
    global ph
    global adr
    global social
    global down
    global scraped_data
    global total
    driver = create_driver()
    # print(domains, flush=True)

    adapter = HTTPAdapter(max_retries=1)
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.trust_env = False
    
    for domain in domains:
        url = "http://" + domain
        client_rendered = False
        with total_lock:
            print(f"{total} : {url}", flush=True)
            total += 1

        try:
            page = session.get(url, timeout=10)                            # make request to url
            # if page.status_code != 200:
            #      raise Exception(f"Get failed for {url}")

            soup = BeautifulSoup(page.content, "lxml")          # parsing with lxml for speed vs. html.parser
            body = soup.find('body')
            if body:
                body = body.get_text()

            # Checking if a website is dynamically rendered or not
            if (body and len(body) < 500) or body == None:        # server side rendered website that needs to be accessed through selenium. TODO: find better metric to evaluate whether a site is client side rendered or not
                client_rendered = True
                print(f"_________{url} is client side rendered_____________")
                try:
                    driver.get(url)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    rendered_html = driver.page_source
                    soup = BeautifulSoup(rendered_html, "lxml")
                except Exception as e:
                    print(e)
                    # continue
        except Exception as e:
            print(e)
            with down_lock:
                print("______________Warning: " + url + " is down_______________", flush=True)
                down += 1
            with scraped_data_lock:
                website_data = {
                    "domain": domain,
                    "phone": "n/a",
                    "address": "n/a",
                    "social_media": "n/a"
                }
                scraped_data.append(website_data)
            continue


        links = [link['href'] for link in soup.find_all('a', href = True)]           # getting all the links before extracting just the text from the bs object

        soup_text = soup.get_text(" ", strip=True)           # converting to text in order to match phone and address
        soup_text = soup_text.replace("\n", " ").replace("\t", " ").replace("\t", "") 

        social_media, contact_pages = extract_links(links, url)
        phone = extract_phone(soup_text)
        address = extract_address(soup_text)

        # Contact page strategy if we didn't find any phone or email. Social links are usually in the header/footer of the landing page
        if len(phone) == 0 and len(address) == 0 and len(contact_pages) != 0:
            print(f'{url} has 0 data on the landing page')
            for page in contact_pages:
                if not (domain in page):
                    if '/' in page:
                        page = url + page
                    else:
                        page = url + '/' + page
                if '@' in page:         # to not open email client for links like contact@blabla.bla
                    continue

                print(f'Trying {page}')

                if client_rendered == False:
                    try:
                        page = session.get(page, timeout=10)                            # make request to url
                        soup = BeautifulSoup(page.content, "lxml")
                    except Exception as e:
                        print(e)
                        continue
                else:
                    try:
                        driver.get(page)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        rendered_html = driver.page_source
                        soup = BeautifulSoup(rendered_html, "lxml")
                    except Exception as e:
                        print(e)
                        continue
                soup_text = soup.get_text(" ", strip=True)           # converting to text in order to match phone and address
                soup_text = soup_text.replace("\n", " ").replace("\t", " ").replace("\t", "")

                social_media, contact_pages = extract_links(links, url)
                phone = extract_phone(soup_text)
                address = extract_address(soup_text)

        # Increasing counters
        if len(phone):
            with ph_lock:
                ph += 1
        if len(social_media):
            with social_lock:
                social += + 1
        if len(address):
            with adr_lock:
                adr += 1

        # Saving data in a dict
        with scraped_data_lock:
            website_data = {
                "domain": domain,
                "phone": phone or "",
                "address": address or "",
                "social_media": social_media or "",
                # "contact_page": contact_pages or ""
            }
            scraped_data.append(website_data)

        print(url + " is done_______________________________________________________________", flush=True)
    # with open('soup.txt', 'w', encoding="utf-8") as f:
    #     f.write(soup.prettify())
    driver.quit()    # Closing webdriver after the whole chunk has been scraped

# Dividing an array into chunks of maximum size n
def divide_chunks(l, n): 
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


if __name__ == '__main__':
    #_____________________________________________________________________________________
    #_________________________________Scraping part ______________________________________
    #_____________________________________________________________________________________

    start = time.time()
    domains_list = read_domains('./data/sample-websites.csv')       # read domains from csv
    # domains_list = domains_list[501:]
    # domains_list = ["the-greenwich.com", "bostonzen.org"]
    # domains_list = ["kelleyroadrace.com"]
    # domains_list = ["foxtrailerservice.com", "hallmemphis.org"]
    # domains_list = ["redrhinomovers.com"]
    # domains_list = ["ccspatherapies.com"]

    # Getting the available amount of physical threads on the cpu
    cpu_cores = multiprocessing.cpu_count()

    # Dividing the domains into (somehwat) equal chunks to be passed to a thread
    chunks = list(divide_chunks(domains_list, math.floor(len(domains_list)/cpu_cores) + 1))               

    with ThreadPoolExecutor(max_workers=cpu_cores*2) as executor:       # starting a thread pool with 2xnumber of threads as there are physical ones
        futures = [executor.submit(scrape, chunk) for chunk in chunks]  # submitting a chunk for each thread
        for future in futures:
            future.result()         # waiting for all threads to finish

    end = time.time()
   

    # for data in scraped_data:
    #     print(data)
    # print(f'Total scraped: Phone numbers: {ph}, Addresses: {adr}, Social media links: {social}, Websites down: {down}')
    # print(f'Statistics: Phone numbers: {round(ph/total, 1)} %, Addresses: {round(adr/total, 1)} %, Social media links: {round(social/total, 1)} %, Websites down: {round(down/total,1)} %')
    # json_file = json.dumps(scraped_data)
    # with open("data.json", "w") as outfile: 
    #     outfile.write(json_file)

    # print(f'Processed {len(scraped_data)} domains')
    # print(f'It took %d seconds', end - start)

    # #_____________________________________________________________________________________
    # #_______________________________Pushing data to ES____________________________________
    # #_____________________________________________________________________________________

    # es = connect_to_elastic()
    # # for item in scraped_data:
    # #     es.index(index = INDEX_NAME, id = item['domain'], body = item)


    # #_____________________________________________________________________________________
    # #_____________________________Reading company names___________________________________
    # #_____________________________________________________________________________________

    # company_list = read_company_data('./data/sample-websites-company-names.csv')


    # for company in company_list:
    #     keys = company.keys()
    #     vals = company.values()
    #     doc = {
    #             'doc': {
    #             }
    #     }
    #     for key, val in zip(keys, vals):        # wrapping the keys and values in the "doc" key 
    #         doc['doc'][key] = (val)

    #     es.update(index = INDEX_NAME, id = company['domain'], body = doc)   # updating the documents by the domain id
