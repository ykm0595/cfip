#!/usr/bin/env python3
import requests
import traceback

# -------------------------------
# 获取优选 IP 列表
# -------------------------------
def get_ip_list(timeout=10, max_retries=5):
    url = "https://ip.164746.xyz/ipTop.html"
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.status_code == 200:
                return [ip.strip() for ip in resp.text.split(",") if ip.strip()]
        except Exception as e:
            print(f"获取 IP 失败 (尝试 {attempt+1}/{max_retries}): {e}")
            traceback.print_exc()
    return []

# -------------------------------
# 查询 IP 归属地（国家简写）
# -------------------------------
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

# -------------------------------
# 主函数：生成 TXT
# -------------------------------
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

# -------------------------------
if __name__ == "__main__":
    main()
