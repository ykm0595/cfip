#!/usr/bin/env python3
import requests
import subprocess

URL = "https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestCF/ipv4.csv"
OUTPUT_FILE = "best_cf_ip.txt"

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

def test_speed(ip):
    try:
        result = subprocess.run(
            [
                "curl",
                "-o", "/dev/null",
                "-s",
                "-w", "%{speed_download}",
                "--max-time", "3",
                f"https://{ip}/cdn-cgi/trace",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        speed_str = result.stdout.strip()
        if not speed_str:
            return 0.0
        return float(speed_str)
    except:
        return 0.0

def main():
    print("=== 从 IPDB 获取 Cloudflare IP 列表 ===")
    ips = fetch_ip_list()

    if not ips:
        print("❌ 未获取到 IP，生成空文件")
        open(OUTPUT_FILE, "w").close()
        return

    print(f"获取到 {len(ips)} 个 IP，开始测速…")

    best_ip = None
    best_speed = 0.0

    for ip in ips[:50]:  # 限制前 50 个，避免 GitHub Actions 超时
        print(f"测速 {ip} ...")
        speed = test_speed(ip)
        print(f"Speed = {speed}")

        if speed > best_speed:
            best_speed = speed
            best_ip = ip

    print("\n=== 最终结果 ===")
    print("测速最快 IP:", best_ip)
    print("速度:", best_speed)

    # 兜底：如果测速全失败，直接用第一个 IP
    if best_ip is None:
        print("⚠ 所有测速为 0，使用第一个 IP 作为结果")
        best_ip = ips[0]

    with open(OUTPUT_FILE, "w") as f:
        f.write(best_ip + "\n")

    print(f"✅ 已写入 {OUTPUT_FILE}: {best_ip}")

if __name__ == "__main__":
    main()
