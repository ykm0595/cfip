#!/usr/bin/env python3
import requests

URL = "https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestCF/ipv4.csv"
OUTPUT_FILE = "cf_ipv4.txt"   # ✅ 你要的文件名

def fetch_ip_list():
    try:
        resp = requests.get(URL, timeout=10)
        if resp.status_code == 200:
            lines = resp.text.split("\n")
            ips = []
            for line in lines:
                parts = line.split(",")
                if len(parts) >= 1:
                    ip = parts[0].strip()
                    if ip.count(".") == 3:
                        ips.append(ip)
            return ips
    except Exception as e:
        print("获取 IP 列表失败:", e)
    return []

def main():
    print("=== 从 IPDB 获取 Cloudflare IP 列表 ===")
    ips = fetch_ip_list()

    if not ips:
        print("❌ 未获取到 IP，生成空文件")
        open(OUTPUT_FILE, "w").close()
        return

    print(f"获取到 {len(ips)} 个 IP，写入前 15 个…")

    top15 = ips[:15]

    with open(OUTPUT_FILE, "w") as f:
        for ip in top15:
            f.write(ip + "\n")

    print(f"✅ 已写入 {OUTPUT_FILE} 共 {len(top15)} 个 IP")

if __name__ == "__main__":
    main()
