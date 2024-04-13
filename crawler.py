from bs4 import BeautifulSoup
from datetime import date
import requests
import json
import traceback
import re
import os                                                                                     
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# import string
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("KEY")

MAX_LINKS = 100
CURRENT_LINKS = 0

class Scholarship:
    def __init__(self, link, content):
        self.link = link
        self.content = content

sub_links_list = ["https://www.daad.de/en/studying-in-germany/scholarships/daad-scholarships/", "https://saidfoundation.org/apply/", "https://www.chevening.org/"]

visited_links = []

scholarships_list = []

def crawler(url, MAX_LINKS, CURRENT_LINKS, scholarships_list):
    try:
        if CURRENT_LINKS >= MAX_LINKS:
            raise Exception("Error: maximum Number of crawled links reached, stopping crawler...")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        # sub_links = soup.findAll("a")
        sub_links = soup.findAll(('a', {'href' : re.compile('^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$')}))
        
        # visited_links.append()
        
        for link in sub_links:
            # print(link["href"])
            # if not link["href"] in sub_links_list and link["href"].startswith('#') == False and link["href"].startswith('/') == False and link["href"].startswith('javascript') == False and link["href"].startswith('tel') == False and link["href"].startswith('apply') == False:
            # print(link["href"])
            sub_links_list.append(link["href"])
            content_response = requests.get(link["href"])
            content_response.raise_for_status()
            content_soup = BeautifulSoup(content_response.text, 'lxml')
            # print(content_soup)
            content = []
            content_divs = content_soup.find_all("div")
            # print("link \n", link, "content \n", content)
            for div in content_divs:
                # print(div.text.split())
                content = content + div.text.split()
            # print("link \n", link, "content \n", content)
            scholarships_list.append(Scholarship(link["href"], content))
        # print(sub_links_list)
        # content = soup.findAll("div")
        # print("link is: \n", url, "content is: \n", content)
        # for div in content:
        #     # tagless_content.extend(div.text.split())
        #     print(div)
    except requests.exceptions.RequestException as err:
        # print("Error: ", err)
        print(err)
    CURRENT_LINKS = CURRENT_LINKS + 1


link = f"https://www.googleapis.com/customsearch/v1?key={key}&cx=b043b2f15aecd42bb&q=scholarships"

# initial_response = requests.get(f"{link} {date.today()}").text
initial_response = json.loads(requests.get(f"{link} {date.today()}").text)["items"]
initial_links = []

for item in initial_response:
    initial_links.append(item["link"])

# print("initial links are: \n", initial_links)
# print(intialResponse)
# print(f"{link} {date.today()}")
# print(requests.get(f"{link} {date.today()}").text)
# print(json.loads(requests.get(f"{link} {date.today()}").text)["items"][1]["link"])
# print(json.loads(requests.get(f"{link} {date.today()}").text)["items"])

for link in initial_links:
    try:
        crawler(link, MAX_LINKS, CURRENT_LINKS, scholarships_list)
        print(CURRENT_LINKS)
    except:
        traceback.print_exc()
        # print(" ")


print(sub_links_list)
for scholarship in scholarships_list:
    # print("link: ", scholarship.link, "content: \n", scholarship.content)
    print("link: \n", scholarship.link, "\n")
# print(scholarships_list)