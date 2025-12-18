#!/usr/bin/env python3
import requests
import re
import subprocess

HTML_SOURCE = "https://ip.164746.xyz/ipTop.html"
OUTPUT_FILE = "best_cf_ip.txt"

def fetch_ip_list():
    try:
        resp = requests.get(HTML_SOURCE, timeout=10)
        if resp.status_code == 200:
            html = resp.text
            # 从 HTML 中提取 IPv4
            ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", html)
            return list(set(ips))  # 去重
    except Exception as e:
        print("获取 IP 列表失败:", e)
    return []

def ping_ip(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "3", "-W", "1", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in result.stdout.split("\n"):
            if "avg" in line:
                avg = line.split("/")[4]
                return float(avg)
    except:
        pass
    return 9999.0

def main():
    print("=== 获取 Cloudflare IP 列表（HTML） ===")
    ips = fetch_ip_list()

    if not ips:
        print("❌ 未获取到 IP，生成空文件")
        open(OUTPUT_FILE, "w").close()
        return

    print(f"获取到 {len(ips)} 个 IP，开始测试延迟…")

    best_ip = None
    best_rtt = 9999.0

    for ip in ips[:50]:  # 限制前 50 个，避免 Actions 超时
        print(f"测试 {ip} ...")
        rtt = ping_ip(ip)
        print(f"RTT = {rtt} ms")

        if rtt < best_rtt:
            best_rtt = rtt
            best_ip = ip

    print("\n=== 最终结果 ===")
    print("最快 IP:", best_ip)
    print("延迟:", best_rtt)

    with open(OUTPUT_FILE, "w") as f:
        f.write(best_ip + "\n")

    print(f"✅ 已写入 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
