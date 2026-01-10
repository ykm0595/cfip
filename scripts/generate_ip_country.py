#!/usr/bin/env python3
import requests

URL = "https://stock.hostmonit.com/CloudFlareYes"

def fetch_cf_ips():
    resp = requests.get(URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # 提取 IP 列表
    ips = [item["ip"] for item in data.get("data", [])]
    return ips

def save_txt(ips):
    # cf_ipv4.txt：ip#优选1
    with open("cf_ipv4.txt", "w") as f:
        for ip in ips:
            f.write(f"{ip}#优选1\n")

    # cf_hk.txt：ip#优选2
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
