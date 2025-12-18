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
            ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", html)
            return list(set(ips))
    except Exception as e:
        print("获取 IP 列表失败:", e)
    return []

def test_speed(ip):
    try:
        result = subprocess.run(
            ["curl", "-o", "/dev/null", "-s", "-w", "%{speed_download}", "--max-time", "3", f"https://{ip}/cdn-cgi/trace"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        speed = float(result.stdout.strip())
        return speed
    except:
        return 0.0

def main():
    print("=== 获取 Cloudflare IP 列表（HTML） ===")
    ips = fetch_ip_list()

    if not ips:
        print("❌ 未获取到 IP，生成空文件")
        open(OUTPUT_FILE, "w").close()
        return

    print(f"获取到 {len(ips)} 个 IP，开始测速…")

    best_ip = None
    best_speed = 0.0

    for ip in ips[:50]:
        print(f"测速 {ip} ...")
        speed = test_speed(ip)
        print(f"Speed = {speed}")

        if speed > best_speed:
            best_speed = speed
            best_ip = ip

    print("\n=== 最终结果 ===")
    print("最快 IP:", best_ip)
    print("速度:", best_speed)

    with open(OUTPUT_FILE, "w") as f:
        f.write(best_ip + "\n")

    print(f"✅ 已写入 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
