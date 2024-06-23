from flask import Flask, request, Response
from crawler import parallel_crawler, simple_crawler
from crawler.sitemaps import read_sitemap, check_if_exists
from middleware import middleware
import os

PORT = int(os.environ.get('PORT'))

app = Flask(__name__)
app.wsgi_app = middleware(app.wsgi_app)

@app.route('/')
def index():
    return "Crawler Service Up!"

@app.route('/api/parallel_crawler', methods=['POST'])
def parallel_crawler_api():
    url = request.json.get('url')
    domain = request.json.get('domain')
    sitemap_location = f'sitemaps/{domain}.xml'
    
    if check_if_exists(domain):
        result = True
    else:
        result = parallel_crawler.crawl_and_generate_sitemap(url, sitemap_location)

    if result:
        sitemap_content = read_sitemap(sitemap_location)
        return Response(sitemap_content, mimetype='application/xml')
    return Response('Failed to crawl', status=500)

@app.route('/api/simple_crawler', methods=['POST'])
def simple_crawler_api():
    url = request.json.get('url')
    domain = request.json.get('domain')
    sitemap_location = f'sitemaps/{domain}.xml'

    if check_if_exists(domain):
        result = True
    else:
        result = simple_crawler.crawl_and_generate_sitemap(url, sitemap_location)
    
    if result:
        sitemap_content = read_sitemap(sitemap_location)
        return Response(sitemap_content, mimetype='application/xml')
    return Response('Failed to crawl', status=500)
    

if __name__ == '__main__':
    app.run(port=PORT)