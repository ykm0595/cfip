#!/bin/bash

set -e

echo "=== 获取 Cloudflare IP 列表 ==="
curl -s https://ip.164746.xyz/ipTop.txt > all_ip.txt

echo "=== 开始 ICMP 延迟测试 ==="
> ping_result.txt

while read -r ip; do
    if [ -n "$ip" ]; then
        rtt=$(ping -c 3 -W 1 $ip 2>/dev/null | grep avg | awk -F'/' '{print $5}')
        if [ -z "$rtt" ]; then
            rtt=9999
        fi
        echo "$rtt $ip" >> ping_result.txt
    fi
done < all_ip.txt

echo "=== 按延迟排序，取前 10 个 ==="
sort -n ping_result.txt | head -n 10 | awk '{print $2}' > top10.txt

echo "=== 开始 curl 下载测速 ==="
> speed_result.txt

for ip in $(cat top10.txt); do
    echo "测速 $ip"
    speed=$(curl -o /dev/null -s -w "%{speed_download}" --connect-timeout 2 --max-time 5 https://$ip/cdn-cgi/trace || echo 0)
    echo "$speed $ip" >> speed_result.txt
done

echo "=== 选出最快的 IP ==="
best_ip=$(sort -nr speed_result.txt | head -n 1 | awk '{print $2}')

echo "最佳 IP: $best_ip"
echo "$best_ip" > best_cf_ip.txt
