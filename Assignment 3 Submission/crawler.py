import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["crawler_db"]
pages_collection = db["pages"]

#getting HTML content
def retrieveHTML(url):
    try:
        response = urllib.request.urlopen(url)
        if response.headers.get_content_type() in ['text/html', 'application/xhtml+xml']:
            return response.read().decode('utf-8')
        else:
            return None
    except Exception as e:
        print(f"Error retrieving URL {url}: {e}")
        return None
#storing HTML content in mongodb
def storePage(url, html):
    pages_collection.insert_one({"url": url, "html": html}) #insert document into pages collection
#checking if page is target page
def target_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1', class_='cpp-h1')
    return h1_tag and h1_tag.text.strip() == 'Permanent Faculty'
#parsing HTML and extracting URLs
def parse(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/') or not urllib.parse.urlparse(href).netloc:
            href = urllib.parse.urljoin(base_url, href)
        if href.startswith("https://www.cpp.edu/sci/computer-science") and href.endswith(('.html', '.shtml')):
            urls.add(href)
    return urls

def crawlerThread(frontier):
    visited = set()
    while frontier:
        url = frontier.pop(0)
        if url in visited:
            continue
        visited.add(url)
        html = retrieveHTML(url)
        if html:
            storePage(url, html)
            if target_page(html):
                print(f"Target page found: {url}")
                break
            else:
                new_urls = parse(html, url)
                for new_url in new_urls:
                    if new_url not in visited:
                        frontier.append(new_url)
frontier = ["https://www.cpp.edu/sci/computer-science/"]
crawlerThread(frontier)