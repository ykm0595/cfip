#!/usr/bin/env python3
import requests

URL = "https://stock.hostmonit.com/CloudFlareYes"

def fetch_cf_ips():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0 Safari/537.36"
    }
    resp = requests.get(URL, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [item["ip"] for item in data.get("data", [])]

def save_txt(ips):
    with open("cf_ipv4.txt", "w") as f:
        for ip in ips:
            f.write(f"{ip}#优选1\n")
    with open("cf_hk.txt", "w") as f:
        for ip in ips:
            f.write(f"{ip}#优选2\n")

if __name__ == "__main__":
    ips = fetch_cf_ips()
    if not ips:
        print("没有抓到任何 IP")
    else:
        save_txt(ips)
        print(f"生成 {len(ips)} 个 IP 到 cf_ipv4.txt 和 cf_hk.txt")
