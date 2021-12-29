import requests
import json
from bs4 import BeautifulSoup

eng_speak_country_ip = '102.129.134.0'

def get_html_page(page_url):
    """Returns html code of a page for given URL"""
    headers = {'Accept-Language': 'en', 'X-FORWARDED-FOR': eng_speak_country_ip}
    response = requests.get(page_url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def get_soup(page_code):
    """Returns soup object from html page code"""
    try:
        soup = BeautifulSoup(page_code, features="html.parser")
        return soup
    except Exception:
        return None

def are_common_films(film_1, film_2):
    '''Takes as parameters two lists.
    Returns True, if they have elements in common, False otherwise.
    '''
    return bool(set(film_1).intersection(film_2))

def get_cached_data(file):
    ''' Parameter file path: str
    Returns dictionary where key is film/acrtor name, value - html page code
    '''
    with open(file) as f:
        raw_data = '{' + f.read()[:-1] + '}'
        data = json.loads(raw_data)
    return data

def save_page_to_file(file, html_page, page_name):
    ''' Saves film/actor name as key, html code as value in json format
    Writes this string to file. File should already exist!
    '''
    with open(file, 'a') as fw:
        fw.write(f'"{page_name}": {json.dumps(html_page)},')