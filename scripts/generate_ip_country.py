#!/usr/bin/env python3
import random

# ✅ 香港高概率段（社区长期验证）
HK_RANGES = [
    "104.19.37.",
    "104.19.38.",
    "104.19.39.",
    "172.67.1.",
    "172.67.7.",
    "104.16.248."
]

# ✅ 全局候选（目前复用香港段，如需更多段可扩展）
GLOBAL_RANGES = HK_RANGES

GLOBAL_COUNT = 15
HK_COUNT = 50

GLOBAL_FILE = "cf_ipv4.txt"
HK_FILE = "cf_hk.txt"


def generate_from_ranges(prefix_list, count):
    """从 IP 段随机生成指定数量的 IP"""
    ips = []
    for prefix in prefix_list:
        for i in range(1, 255):
            ips.append(prefix + str(i))
    return random.sample(ips, min(count, len(ips)))


def main():
    print("=== 生成 Cloudflare 全球随机 15 个 IP ===")
    global_ips = generate_from_ranges(GLOBAL_RANGES, GLOBAL_COUNT)
    with open(GLOBAL_FILE, "w") as f:
        for ip in global_ips:
            f.write(ip + "\n")
    print(f"✅ 已写入 {GLOBAL_FILE} 共 {len(global_ips)} 个 IP")

    print("=== 生成 Cloudflare 香港随机 50 个 IP（带 HK 序号） ===")
    hk_ips = generate_from_ranges(HK_RANGES, HK_COUNT)
    with open(HK_FILE, "w") as f:
        for idx, ip in enumerate(hk_ips, start=1):
            f.write(f"{ip}#HK{idx}\n")
    print(f"✅ 已写入 {HK_FILE} 共 {len(hk_ips)} 个香港 IP（带 HK 序号）")


if __name__ == "__main__":
    main()
