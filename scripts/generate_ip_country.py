#!/usr/bin/env python3
import requests

URL = "https://www.wetest.vip/api/cloudflare/address_v4"

def fetch_cf_ips():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0 Safari/537.36",
        "Referer": "https://www.wetest.vip/page/cloudflare/addressv4.html"
    }
    resp = requests.get(URL, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return [item["ip"] for item in data.get("data", [])]

def save_txt(ips):
    # cf_ipv4.txt → ip#优选1,2,3...
    with open("cf_ipv4.txt", "w") as f:
        for idx, ip in enumerate(ips, start=1):
            f.write(f"{ip}#优选{idx}\n")

    # cf_hk.txt → ip#优选1,2,3...
    with open("cf_hk.txt", "w") as f:
        for idx, ip in enumerate(ips, start=1):
            f.write(f"{ip}#优选{idx}\n")

if __name__ == "__main__":
    try:
        ips = fetch_cf_ips()
        if not ips:
            print("没有抓到任何 IP")
        else:
            save_txt(ips)
            print(f"成功生成 {len(ips)} 个 IP 到 cf_ipv4.txt 和 cf_hk.txt")
    except Exception as e:
        print(f"抓取失败: {e}")
