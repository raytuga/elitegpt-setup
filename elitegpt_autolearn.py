
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Çekilecek örnek sayfa: güncel bir haber sitesi (değiştirilebilir)
URL = 'https://www.bbc.com/news'

# Bellek dosyası
OUTPUT = 'memory_scraped.json'

# Sayfayı çek
def fetch_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=10)
    return response.text if response.status_code == 200 else None

# Temiz metinleri ayıkla
def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    headlines = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3']) if len(h.get_text().strip()) > 20]
    return headlines

# JSON formatına çevir
def build_memory(entries):
    now = datetime.utcnow().isoformat()
    return {
        "memory": [
            {
                "role": "system",
                "content": f"Bugün ({now}) elde edilen bilgiler şunlardır:"
            }
        ] + [
            {"role": "user", "content": e} for e in entries
        ]
    }

# Çalıştır
def main():
    html = fetch_page(URL)
    if not html:
        print("❌ Sayfa alınamadı.")
        return
    entries = extract_text(html)
    if not entries:
        print("⚠️ Uygun veri bulunamadı.")
        return
    memory = build_memory(entries)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(entries)} içerik belleğe yazıldı → {OUTPUT}")

if __name__ == "__main__":
    main()
