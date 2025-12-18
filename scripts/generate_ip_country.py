#!/usr/bin/env python3
import requests
import random

URL = "https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestCF/ipv4.csv"

GLOBAL_FILE = "cf_ipv4.txt"   # ✅ 随机 15 个全球 CF IP
HK_FILE = "cf_hk.txt"         # ✅ 随机 50 个香港 CF IP


def fetch_ipdb():
    try:
        resp = requests.get(URL, timeout=10)
        if resp.status_code == 200:
            lines = resp.text.split("\n")
            parsed = []
            for line in lines:
                parts = line.split(",")
                if len(parts) >= 3:
                    ip = parts[0].strip()
                    country = parts[1].strip()
                    asn = parts[2].strip()
                    if ip.count(".") == 3:
                        parsed.append((ip, country, asn))
            return parsed
    except Exception as e:
        print("获取 IPDB 失败:", e)
    return []


def generate_global_ips(ipdb):
    """随机抽取 15 个全球 Cloudflare IP"""
    ips = [ip for ip, _, _ in ipdb]
    count = min(15, len(ips))
    selected = random.sample(ips, count)

    with open(GLOBAL_FILE, "w") as f:
        for ip in selected:
            f.write(ip + "\n")

    print(f"✅ 已写入 {GLOBAL_FILE} 共 {len(selected)} 个 IP")


def generate_hk_ips(ipdb):
    """随机抽取 50 个香港 Cloudflare IP（HK + AS13335）"""
    hk_ips = [ip for ip, country, asn in ipdb if country == "HK" and asn == "AS13335"]

    if not hk_ips:
        print("❌ 未找到香港 Cloudflare IP，生成空文件")
        open(HK_FILE, "w").close()
        return

    count = min(50, len(hk_ips))
    selected = random.sample(hk_ips, count)

    with open(HK_FILE, "w") as f:
        for ip in selected:
            f.write(ip + "\n")

    print(f"✅ 已写入 {HK_FILE} 共 {len(selected)} 个香港 IP")


def main():
    print("=== 从 IPDB 获取 Cloudflare IP 列表 ===")
    ipdb = fetch_ipdb()

    if not ipdb:
        print("❌ IPDB 获取失败，两个文件均生成空内容")
        open(GLOBAL_FILE, "w").close()
        open(HK_FILE, "w").close()
        return

    print(f"✅ 成功解析 {len(ipdb)} 条 IPDB 数据")

    generate_global_ips(ipdb)
    generate_hk_ips(ipdb)


if __name__ == "__main__":
    main()
