import os
import re
import urllib.request
from urllib.parse import urljoin

def download_assets():
    base_url = 'https://www.gutenberg.org/files/25344/25344-h/'
    html_url = urljoin(base_url, '25344-h.htm')
    dest_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(dest_dir, 'raw_source.html')
    images_dir = os.path.join(dest_dir, 'images')
    
    os.makedirs(images_dir, exist_ok=True)
    
    print("Downloading raw HTML source...")
    urllib.request.urlretrieve(html_url, html_path)
    print(f"HTML saved to {html_path}")
    
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()
        
    # Find image paths in both src="..." and href="..."
    matches_src = re.findall(r'src=["\'](images/[^"\']+)["\']', html_content, re.IGNORECASE)
    matches_href = re.findall(r'href=["\'](images/[^"\']+\.(?:jpg|png|gif|jpeg))["\']', html_content, re.IGNORECASE)
    
    all_matches = matches_src + matches_href
    unique_matches = sorted(list(set(all_matches)))
    print(f"Found {len(unique_matches)} unique assets to download.")
    
    for i, img_rel_path in enumerate(unique_matches, 1):
        img_url = urljoin(base_url, img_rel_path)
        local_img_path = os.path.join(dest_dir, img_rel_path.replace('/', os.sep))
        os.makedirs(os.path.dirname(local_img_path), exist_ok=True)
        
        # Skip if file already exists and is not empty to save bandwidth/time
        if os.path.exists(local_img_path) and os.path.getsize(local_img_path) > 0:
            continue
            
        print(f"[{i}/{len(unique_matches)}] Downloading {img_url} -> {local_img_path}")
        try:
            req = urllib.request.Request(
                img_url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req) as response, open(local_img_path, 'wb') as out_file:
                out_file.write(response.read())
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

if __name__ == '__main__':
    download_assets()
