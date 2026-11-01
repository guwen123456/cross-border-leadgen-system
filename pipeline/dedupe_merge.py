#!/usr/bin/env python3
"""多批次买家表合并去重。

按规范化后的官网域名 + 公司名去重（跨批次采集时同一家公司常被采到两次，
域名写法还不一致：带 www / 带 https / 大小写）。先出现的行保留，
被去掉的重复行单独输出一份报告，不静默删除。

用法: python3 dedupe_merge.py out.csv in1.csv in2.csv [...]
"""
import csv, sys, re
from urllib.parse import urlparse

def norm_site(url):
    url = (url or "").strip().lower()
    if not url:
        return ""
    if "://" not in url:
        url = "http://" + url
    host = urlparse(url).netloc or urlparse(url).path
    return host[4:] if host.startswith("www.") else host

def norm_name(name):
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", (name or "").lower())

def main():
    out_path, inputs = sys.argv[1], sys.argv[2:]
    seen, kept, dups = {}, [], []
    fields = None
    for path in inputs:
        for r in csv.DictReader(open(path, encoding="utf-8-sig")):
            if fields is None:
                fields = list(r.keys())
            key = norm_site(r.get("website")) or norm_name(r.get("company_name"))
            if key and key in seen:
                dups.append({**r, "_dup_of": seen[key]})
            else:
                if key:
                    seen[key] = r.get("buyer_id") or r.get("company_name")
                kept.append(r)
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(kept)
    if dups:
        with open(out_path.replace(".csv", "_duplicates.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields + ["_dup_of"])
            w.writeheader()
            w.writerows(dups)
    print(f"kept={len(kept)} duplicates_removed={len(dups)}")

if __name__ == "__main__":
    main()
