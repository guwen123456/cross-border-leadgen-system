#!/usr/bin/env python3
"""把发送名单按收件人时区分波（wave），控制单日节奏。

原则：让邮件落在对方工作日上午（按 Asia/Shanghai 时间排波），
每波数量有上限，新账号尤其要慢。脚本只做计划和生成 outreach_log 行，
不实际发送 —— 发送逐封人工确认。

用法: python3 make_waves.py buyers_tier1.csv [per_wave_cap]
"""
import csv, sys

# region -> (建议发送的北京时间小时, 说明)
REGION_PLAN = {
    "MEAPAC": (14, "中东/亚太下午，对方上午"),
    "EU": (15, "欧洲下午，对方上午"),
    "AMERICAS": (21, "美洲晚间，对方上午"),
}
EU = {"DE","FR","PL","NL","ES","IT","SE","DK","NO","FI","CZ","SK","HU","RO","GR","PT","BE","AT","CH","IE","GB","UK"}
AMERICAS = {"US","CA","MX","BR","CL","CO","PE","AR"}
MEAPAC = {"AE","SA","SG","MY","IN","ID","TH","VN","PH","AU","NZ","JP","KR","TR","IL","EG","ZA"}

def region(country):
    c = (country or "").strip().upper()
    if c in EU: return "EU"
    if c in AMERICAS: return "AMERICAS"
    if c in MEAPAC: return "MEAPAC"
    return "MEAPAC"

def main():
    src = sys.argv[1]
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    waves = {}
    for r in rows:
        waves.setdefault(region(r.get("country")), []).append(r)
    for reg in ("MEAPAC", "EU", "AMERICAS"):
        sub = waves.get(reg, [])
        hour, note = REGION_PLAN[reg]
        for i in range(0, len(sub), cap):
            batch = sub[i:i + cap]
            print(f"wave {reg} #{i // cap + 1}: send ~{hour:02d}:00 CST ({note}), {len(batch)} letters: "
                  + ", ".join(b.get("company_name", "?") for b in batch))

if __name__ == "__main__":
    main()
