import re

phone_regex = re.compile(r'''(
                         \(?\+?(\d{1,3})?\)?(-|\.)?
                         (\d{3}|\(\d{3}\))+
                         (\s|-|\.)+
                         (\d{3})+
                         (\s|-|\.)+
                         (\d{4})+
                         (\s*(ext|x|ext.)\s*(\d{2,5}))?)''', re.VERBOSE)

address_regex = re.compile(r'''(
                           ([0-9]{1,4}[\s](S.|W.|N.|E.)*[.\s])?
                           [0-9]{1,5}
                           [\s]+
                           [a-zA-Z\s.\.\-\,\#]{0,30}
                           (\b([A|a]venue|[A|a]ve|[C|c]ourt|[C|c]t|[S|s]treet|[S|s]t|[D|d]rive|[D|d]r|[L|l]ane|[L|l]n|[R|r]oad|[R|r]d|[B|b]lvd|[P|p]laza|[P|p]arkway|[P|p]kwy))?
                           [\s]?
                           [a-zA-Z0-9\s.\-\,\#\|]{0,20}
                           [a-zA-Z0-9\s.\-\,\#]{0,10}
                           [^0-9]{5}
                           [0-9]{5})''', re.VERBOSE) # ([0-9]+[\s]*[a-zA-Z\s.\-\,\#]+(\b([A|a]venue|[A|a]ve|[C|c]ourt|[C|c]t|[S|s]treet|[S|s]t|[D|d]rive|[D|d]r|[L|l]ane|[L|l]n|[R|r]oad|[R|r]d|[B|b]lvd|[P|p]laza|[P|p]arkway|[P|p]kwy))+[\s]?[a-zA-Z0-9.\-\,\#]+[a-zA-Z0-9\s.\-\,\#]*[0-9]{5})
pobox_regex = re.compile(r'''(\b(PO|Post)+[a-zA-Z\s0-9.\-\,\#]*[0-9]{5})''', re.VERBOSE)
                         
# email_regex = re.compile(r'''(
#                         [a-zA-Z0-9._%+-]+
#                         @
#                         [a-zA-Z0-9.-]+
#                         (\.[a-zA-Z]{2,4}))''', re.VERBOSE)

social_media_regex = re.compile(r'^(http[s]?)?(://)?(www.)?(facebook|instagram|twitter|tiktok|linkedin|youtube)+(.com[/in])+[/a-zA-Z0-9.\_\-\,\#]+$', re.VERBOSE)

def extract_phone(soup):
    matches = set()
    for groups in phone_regex.findall(soup):
        # prefix = groups[2].replace('(', '').replace(')', '')
        # phone_numbers = '-'.join([prefix, groups[4], groups[6]])
        # if groups[8] != '':
                # phone_numbers += ' x' + groups[8]            
        matches.add(groups[0])

    return list(matches)

def extract_address(soup):
    matches = set()
    for groups in address_regex.findall(soup):
        matches.add("".join(groups[0]))
    if len(matches) == 0:
        for groups in pobox_regex.findall(soup):
            matches.add("".join(groups[0]))
    return list(matches)

def extract_links(links, url):
    matches = set()
    contact_page_matches = set()
    contact_page_regex = re.compile(fr'[\:a-zA-Z0-9.\/\-\,\#]*(contact|about)+[a-zA-Z0-9.\-\,\#]*')

    for link in links:
        if social_media_regex.match(link):
            matches.add(link)
        elif contact_page_regex.match(link):
            contact_page_matches.add(link)
    return list(matches), list(contact_page_matches)

# def extract_email(soup):
#     matches = set()
#     for groups in email_regex.findall(soup):
#         matches.add("".join(groups[0]))
#     return matches