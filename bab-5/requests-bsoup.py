import requests
from bs4 import BeautifulSoup

def fetch_and_parse_url(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  return soup

def print_links(soup):
  # Find all anchor tags
  links = soup.find_all('a')
  for link in links:
    href = link.get('href')
    text = link.text.strip()
    print(f"Link: {href}, Text: {text}")

url = 'http://www.python.org'
soup = fetch_and_parse_url(url)
print_links(soup)