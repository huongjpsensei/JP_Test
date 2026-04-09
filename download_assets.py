import re
import os
import urllib.request
from urllib.parse import urlparse, unquote, quote

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(r'(?:src|href)="([^"]+?\.(?:png|jpg|jpeg|mp3|gif|svg))"', re.IGNORECASE)
urls = set(pattern.findall(html))

if not os.path.exists('assets'):
    os.makedirs('assets')

for url in urls:
    if not url.startswith('http'):
        continue
    
    # Extract filename
    parsed_url = urlparse(url)
    filename = unquote(os.path.basename(parsed_url.path))
    local_path = os.path.join('assets', filename)
    
    if os.path.exists(local_path):
        continue
    
    # encode url for request if it contains non-ascii
    try:
        url_ascii = url.encode('ascii').decode('ascii')
        request_url = url
    except UnicodeEncodeError:
        path = quote(parsed_url.path)
        request_url = f"{parsed_url.scheme}://{parsed_url.netloc}{path}"

    try:
        print("Downloading...", flush=True)
        req = urllib.request.Request(request_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
            
        local_url = "assets/" + filename
        html = html.replace(url, local_url)
    except Exception as e:
        print(f"Failed to download: {repr(e)}", flush=True)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
        
print("Done.")
