#!/usr/bin/env python3
import requests, re

URL = "https://www.wetest.vip/page/cloudflare/addressv4.html"

def fetch_cf_ips():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36"
    }
    resp = requests.get(URL, headers=headers, timeout=15)
    resp.raise_for_status()
    html = resp.text
    # 用正则匹配 IPv4 地址
    ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", html)
    # 去重
    return list(dict.fromkeys(ips))

def save_txt(ips):
    with open("cf_ipv4.txt", "w") as f:
        for idx, ip in enumerate(ips, start=1):
            f.write(f"{ip}#优选{idx}\n")

    with open("cf_hk.txt", "w") as f:
        for idx, ip in enumerate(ips, start=1):
            f.write(f"{ip}#优选{idx}\n")

if __name__ == "__main__":
    ips = fetch_cf_ips()
    if not ips:
        print("没有抓到任何 IP")
    else:
        save_txt(ips)
        print(f"成功生成 {len(ips)} 个 IP 到 cf_ipv4.txt 和 cf_hk.txt")
