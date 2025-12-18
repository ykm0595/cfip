#!/usr/bin/env python3
import os
import re
import sys
import time
import socket
import ipaddress
import urllib.request
import json

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

def get_ip_location(ip: str) -> str:
    """
    返回格式：国家-地区-城市
    """
    url = f"https://ipinfo.io/{ip}/json"
    try:
        with urllib.request.urlopen(url, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            country = data.get("country", "")
            region = data.get("region", "")
            city = data.get("city", "")
            loc = "-".join([x for x in [country, region, city] if x])
            return loc if loc else "Unknown"
    except:
        return "Unknown"

def main():
    all_ips = set()

    for url in SOURCES:
        text = fetch_url(url)
        ips = extract_ipv4(text)
        for ip in ips:
            n = normalize_ipv4(ip)
            if n:
                all_ips.add(n)

    print(f"[INFO] unique IP count: {len(all_ips)}")

    reachable = []
    for ip in sorted(all_ips):
        if basic_reachable(ip):
            reachable.append(ip)
        time.sleep(0.01)

    print(f"[INFO] reachable IP count: {len(reachable)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for ip in reachable:
            loc = get_ip_location(ip)
            f.write(f"{ip}#{loc}\n")

    print(f"[INFO] write {len(reachable)} lines to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
