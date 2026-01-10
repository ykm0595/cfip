#!/usr/bin/env python3
import requests
import re
from pathlib import Path

URL = "https://www.wetest.vip/page/cloudflare/addressv4.html"

def fetch_cf_ips():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36"
    }
    resp = requests.get(URL, headers=headers, timeout=15)
    resp.raise_for_status()
    html = resp.text
    # 匹配 IPv4 地址
    ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", html)
    # 去重保持顺序
    return list(dict.fromkeys(ips))

def save_txt(ips):
    Path(".").mkdir(parents=True, exist_ok=True)
    with open("cf_ipv4.txt", "w") as f:
        for idx, ip in enumerate(ips, start=1):
            f.write(f"{ip}#优选{idx}\n")

if __name__ == "__main__":
    try:
        ips = fetch_cf_ips()
        if not ips:
            print("没有抓到任何 IP")
        else:
            save_txt(ips)
            print(f"成功生成 {len(ips)} 个 IP 到 cf_ipv4.txt")
    except Exception as e:
        print(f"抓取失败: {e}")
