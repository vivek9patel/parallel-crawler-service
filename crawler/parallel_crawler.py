import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import concurrent.futures
import os

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def fetch_url(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return url, response.content
    except requests.RequestException as e:
        print(f"[PARALLEL_CRAWLER] Error fetching {url}: {e}")
    return url, None

def parse_links(base_url, content):
    urls = set()
    soup = BeautifulSoup(content, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        full_url = urljoin(base_url, link)
        normalized_url, _ = urldefrag(full_url)
        if is_valid_url(normalized_url) and base_url in full_url:
            urls.add(normalized_url)
    return urls

def crawl(base_url, logs):
    visited = set()
    to_visit = {base_url}
    all_urls = set()
    max_workers = os.cpu_count()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        while to_visit:
            futures = {executor.submit(fetch_url, url) for url in to_visit}
            to_visit = set()
            
            for future in concurrent.futures.as_completed(futures):
                url, content = future.result()
                if content:
                    if logs:
                        print("Visited: ", url)
                    visited.add(url)
                    all_urls.add(url)
                    new_urls = parse_links(base_url, content)
                    to_visit.update(new_urls - visited)

    return all_urls

def generate_sitemap(urls, output_file):
    from xml.etree.ElementTree import Element, SubElement, ElementTree

    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for url in urls:
        url_elem = SubElement(urlset, "url")
        loc_elem = SubElement(url_elem, "loc")
        loc_elem.text = url

    tree = ElementTree(urlset)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def crawl_and_generate_sitemap(base_url, output_file, logs=False):
    try:
        print(f"[PARALLEL_CRAWLER] Starting crawl for {base_url}")
        urls = crawl(base_url, logs)
        print(f"[PARALLEL_CRAWLER] Generating sitemaps for {len(urls)} URLs")
        generate_sitemap(urls, output_file)
        print(f"[PARALLEL_CRAWLER] Sitemaps saved to {output_file}")
        return True
    except Exception as e:
        print(f"[PARALLEL_CRAWLER] Error crawling {base_url}: {e}")
        return False