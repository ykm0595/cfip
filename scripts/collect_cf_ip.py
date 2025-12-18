#!/usr/bin/env python3
import os
import re
import sys
import time
import socket
import ipaddress
import urllib.request
import json

# -------------------------------
# Cloudflare 机房代码 → 国家简写
# -------------------------------
CLO_MAP = {
    "HKG": "HK", "TPE": "TW",
    "NRT": "JP", "KIX": "JP", "FUK": "JP",

    "LAX": "US", "SJC": "US", "SEA": "US",
    "ORD": "US", "IAD": "US", "DFW": "US",
    "MIA": "US", "ATL": "US", "BOS": "US",
    "EWR": "US",

    "FRA": "DE", "MUC": "DE", "HAM": "DE",

    "AMS": "NL", "CDG": "FR", "LHR": "GB",
    "MAD": "ES", "MXP": "IT",

    "SIN": "SG", "KUL": "MY", "BKK": "TH",
    "MNL": "PH",

    "SYD": "AU", "MEL": "AU",

    "GRU": "BR", "SCL": "CL",
}

# -------------------------------
# 数据源（可自行增删）
# -------------------------------
SOURCES = [
    "https://cf.vvhan.com",
    "https://cf.090227.xyz",
    "https://ip.164746.xyz",
    "https://stock.hostmonit.com/CloudFlareYes",
    "https://raw.githubusercontent.com/joname1/BestCFip/refs/heads/main/ipv4.txt",
]

OUTPUT_FILE = os.environ.get("CF_OUTPUT_FILE", "cf_ipv4.txt")

IPV4_REGEX = re.compile(
    r"\b(?:(?:2[0-4]\d|25[0-5]|1?\d?\d)\.){3}(?:2[0-4]\d|25[0-5]|1?\d?\d)\b"
)

# -------------------------------
# 工具函数
# -------------------------------
def fetch_url(url: str, timeout: int = 10) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="ignore")
    except:
        return ""

def extract_ipv4(text: str):
    return IPV4_REGEX.findall(text) if text else []

def normalize_ipv4(ip: str) -> str:
    try:
        return str(ipaddress.ip_address(ip.strip()))
    except:
        return ""

def basic_reachable(ip: str, port: int = 443, timeout: float = 0.8) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

# -------------------------------
# 获取 Cloudflare 真实机房
# -------------------------------
def get_cf_location(ip: str) -> str:
    """
    返回国家简写，如 US、HK、JP、DE
    """
    url = f"http://{ip}/cdn-cgi/trace"
    try:
        with urllib.request.urlopen(url, timeout=1.5) as resp:
            text = resp.read().decode("utf-8", errors="ignore")
            for line in text.split("\n"):
                if line.startswith("colo="):
                    colo = line.split("=")[1].strip().upper()
                    return CLO_MAP.get(colo, "UN")
    except:
        return "UN"

# -------------------------------
# 主流程
# -------------------------------
def main():
    all_ips = set()

    print(f"[INFO] Fetching from {len(SOURCES)} sources...")
    for url in SOURCES:
        text = fetch_url(url)
        ips = extract_ipv4(text)
        for ip in ips:
            n = normalize_ipv4(ip)
            if n:
                all_ips.add(n)

    print(f"[INFO] Unique IP count: {len(all_ips)}")

    reachable = []
    for ip in sorted(all_ips):
        if basic_reachable(ip):
            reachable.append(ip)
        time.sleep(0.01)

    print(f"[INFO] Reachable IP count: {len(reachable)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for ip in reachable:
            loc = get_cf_location(ip)
            f.write(f"{ip}#{loc}\n")

    print(f"[INFO] Write {len(reachable)} lines to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
