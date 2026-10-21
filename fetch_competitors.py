import urllib.request
import urllib.parse
import json
import re
from pathlib import Path

output_dir = Path(r"c:\Users\rkheu\Downloads\Aarogya jal reboot\competitor_images")
output_dir.mkdir(exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_ddg_images(query, max_results=3):
    url = f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = [r['image'] for r in data.get('results', [])[:max_results]]
            return results
    except Exception as e:
        print(f"Error fetching images for '{query}': {e}")
        return []

competitors = {
    "ketos_shield": "KETOS SHIELD water hardware kiosk",
    "ketos_software": "KETOS water quality dashboard analytics",
    "aquagenx_cbt": "Aquagenx Compartment Bag Test kit water",
    "omnivis_device": "OmniVis cholera pathogen detection smartphone",
    "cluix_analyzer": "CLUIX portable water quality analyzer India",
    "ysi_exo_sonde": "YSI EXO multiparameter sonde water quality probe",
    "hach_claros": "Hach SC200 Claros water controller dashboard",
    "scan_spectrolyser": "s::can spectro::lyser spectrometer water probe",
    "kando_pulse": "Kando wastewater intelligence IoT sensor",
    "aqvify_monitor": "Aqvify well water level sensor app"
}

downloaded = {}

for key, query in competitors.items():
    print(f"Searching for {key}...")
    imgs = get_ddg_images(query, max_results=5)
    success = False
    for img_url in imgs:
        try:
            req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                    ext = 'jpg'
                dest = output_dir / f"{key}.{ext}"
                with open(dest, 'wb') as f:
                    f.write(resp.read())
                if dest.stat().st_size > 5000:
                    print(f"  -> Successfully downloaded {dest.name} ({dest.stat().st_size/1024:.1f} KB)")
                    downloaded[key] = str(dest)
                    success = True
                    break
        except Exception as e:
            continue
    if not success:
        print(f"  -> Could not download image for {key}")

print("Downloaded summary:", downloaded)
