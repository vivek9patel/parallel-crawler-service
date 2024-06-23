import os

def read_sitemap(sitemap_location):
    # read content from sitemap_location
    with open(sitemap_location, 'r') as f:
        content = f.read()
    return content

def check_if_exists(domain):
    # check if sitemap exists for domain
    return os.path.exists(f'sitemaps/{domain}.xml')
