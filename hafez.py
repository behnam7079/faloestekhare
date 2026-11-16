import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor

TOTAL_GHAZALS = 495
BASE_URL = "https://cdn.jsdelivr.net/gh/ganjoor/ganjoor-data@main/poets/hafez/ghazal/sh{}.json"

def fetch_ghazal(index):
    url = BASE_URL.format(index)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return index, data
    except Exception:
        return index, None

def main():
    print(f"🚀 شروع دانلود هم‌زمان تمام {TOTAL_GHAZALS} غزل حافظ از مخزن رسمی گنجور...")
    
    results = {}
    # با ۲۰ اتصال هم‌زمان تا در چند ثانیه تمام شود
    with ThreadPoolExecutor(max_workers=20) as executor:
        for index, data in executor.map(fetch_ghazal, range(1, TOTAL_GHAZALS + 1)):
            if data:
                results[index] = data
                print(f"\rدریافت غزل شماره {index} (مجموع موفق: {len(results)}/{TOTAL_GHAZALS})", end="", flush=True)

    sorted_poems = [results[i] for i in sorted(results.keys())]

    output_data = {
        "record_count": len(sorted_poems),
        "poems": sorted_poems
    }

    with open("hafez.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n\n✅ پرونده بسته شد! {len(sorted_poems)} غزل کامل حافظ در hafez.json ذخیره شد.")

if __name__ == "__main__":
    main()
