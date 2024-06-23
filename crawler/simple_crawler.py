import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_urls(base_url, logs):
    urls = set()
    to_visit = {base_url}
    visited = set()

    while to_visit:
        url = to_visit.pop()
        visited.add(url)
        if logs: 
            print(f"Visited: {url}")
        try:
            response = requests.get(url)
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']
                full_url = urljoin(base_url, link)
                if is_valid_url(full_url) and base_url in full_url and full_url not in visited:
                    to_visit.add(full_url)
                    urls.add(full_url)
        except Exception as e:
            print(f"[SIMPLE_CRAWLER] Error crawling {url}: {e}")

    return urls

def generate_sitemap(urls, output_file):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for url in urls:
        url_elem = ET.Element("url")
        loc_elem = ET.Element("loc")
        loc_elem.text = url
        url_elem.append(loc_elem)
        urlset.append(url_elem)

    tree = ET.ElementTree(urlset)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def crawl_and_generate_sitemap(base_url, output_file, logs=False):
    try:
        print(f"[SIMPLE_CRAWLER] Starting crawl for {base_url}")
        urls = get_all_urls(base_url, logs)
        print(f"[SIMPLE_CRAWLER] Generating sitemaps for {len(urls)} URLs")
        generate_sitemap(urls, output_file)
        print(f"[SIMPLE_CRAWLER] Sitemaps saved to {output_file}")
        return True
    except Exception as e:
        print(f"[SIMPLE_CRAWLER] Error crawling {base_url}: {e}")
        return False