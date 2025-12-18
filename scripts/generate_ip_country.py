#!/usr/bin/env python3
import requests

def get_ip_list():
    url = "https://ip.164746.xyz/ipTop.txt"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return [line.strip() for line in resp.text.split("\n") if line.strip()]
    except:
        pass
    return []

def get_country(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("country", "UN")
    except:
        pass
    return "UN"

def main():
    ip_list = get_ip_list()

    if not ip_list:
        print("未获取到 IP 列表")
        return

    print(f"获取到 {len(ip_list)} 个 IP，开始查询归属地…")

    with open("cf_ipv4.txt", "w", encoding="utf-8") as f:
        for ip in ip_list:
            country = get_country(ip)
            f.write(f"{ip}#{country}\n")
            print(f"{ip} → {country}")

    print("\n✅ 已生成 cf_ipv4.txt")

if __name__ == "__main__":
    main()
