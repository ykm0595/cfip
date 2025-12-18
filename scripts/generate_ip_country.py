#!/usr/bin/env python3
import requests
import json

# -------------------------------
# 1. 多个数据源（都用上）
# -------------------------------
SOURCES = [
    "https://ip.164746.xyz/ipTop.html",
    "https://ip.164746.xyz/ipTop.txt",
    "https://ip.164746.xyz/ipTop.json",
]

# -------------------------------
# 2. 从不同页面提取 IP
# -------------------------------
def fetch_text(url, timeout=10):
    try:
        resp = requests.get(url, timeout=timeout)
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        print(f"[WARN] 请求失败: {url} -> {e}")
    return ""

def parse_ips_from_html_or_txt(text):
    # 兼容：逗号分隔 / 换行分隔
    raw = text.replace("\r", "\n").replace(",", "\n")
    ips = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        # 简单判断是不是 IPv4
        parts = line.split(".")
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            ips.append(line)
    return ips

def parse_ips_from_json(text):
    try:
        data = json.loads(text)
        # 兼容格式：{"data": [...]} 或 ["1.1.1.1",...]
        if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
            return [ip.strip() for ip in data["data"] if isinstance(ip, str) and ip.strip()]
        if isinstance(data, list):
            return [ip.strip() for ip in data if isinstance(ip, str) and ip.strip()]
    except Exception as e:
        print(f"[WARN] 解析 JSON 失败: {e}")
    return []

def collect_all_ips():
    all_ips = set()
    for url in SOURCES:
        print(f"[INFO] 获取: {url}")
        text = fetch_text(url)
        if not text:
            continue

        if url.endswith(".json"):
            ips = parse_ips_from_json(text)
        else:
            ips = parse_ips_from_html_or_txt(text)

        print(f"[INFO] {url} 提取到 {len(ips)} 个 IP")
        all_ips.update(ips)

    print(f"[INFO] 合并去重后共 {len(all_ips)} 个 IP")
    return sorted(all_ips)

# -------------------------------
# 3. 查询 IP 归属地（国家简写）
# -------------------------------
def get_country(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("country", "UN")
    except Exception as e:
        print(f"[WARN] 查询归属地失败 {ip}: {e}")
    return "UN"

# -------------------------------
# 4. 主函数：生成 cf_ipv4.txt
# -------------------------------
def main():
    ips = collect_all_ips()
    if not ips:
        print("[ERROR] 未获取到任何 IP")
        return

    print("[INFO] 开始查询归属地并生成 cf_ipv4.txt ...")
    with open("cf_ipv4.txt", "w", encoding="utf-8") as f:
        for ip in ips:
            country = get_country(ip)
            line = f"{ip}#{country}"
            f.write(line + "\n")
            print(line)

    print("[DONE] 已生成 cf_ipv4.txt")

if __name__ == "__main__":
    main()
