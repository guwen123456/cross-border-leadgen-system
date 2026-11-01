#!/usr/bin/env python3
"""买家名单质量门：校验 + 分层。

按 templates/scoring.md 的规则检查 buyers.csv：
- 必填：company_name / country / website / buyer_type
- match_score >= 60 的行必须写 score_basis（一行一句的打分理由，只有数字不算数）
- 有 public_contact 的行必须写 contact_source（联系方式出处）
- sells_bluetooth_earbuds 只能是 Yes / No / Unknown，不许猜
输出一份分层名单（tier1 >= 85, tier2 70-84, tier3 60-69, hold < 60）和问题清单。

用法: python3 validate_buyers.py buyers.csv [out_dir]
"""
import csv, sys, os
from collections import Counter

REQUIRED = ["company_name", "country", "website", "buyer_type"]

def tier(score):
    if score >= 85: return "tier1"
    if score >= 70: return "tier2"
    if score >= 60: return "tier3"
    return "hold"

def main():
    src = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(out_dir, exist_ok=True)
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    problems, tiers = [], Counter()
    for i, r in enumerate(rows, 1):
        bid = r.get("buyer_id") or f"row{i}"
        for f in REQUIRED:
            if not (r.get(f) or "").strip():
                problems.append(f"{bid}: missing required field {f}")
        try:
            score = int(r.get("match_score") or 0)
        except ValueError:
            problems.append(f"{bid}: match_score not a number: {r.get('match_score')!r}")
            score = 0
        if score >= 60 and not (r.get("score_basis") or "").strip():
            problems.append(f"{bid}: score>=60 but score_basis is empty")
        if (r.get("public_contact") or "").strip() and not (r.get("contact_source") or "").strip():
            problems.append(f"{bid}: has public_contact but no contact_source")
        if (r.get("sells_bluetooth_earbuds") or "").strip() not in ("Yes", "No", "Unknown", ""):
            problems.append(f"{bid}: sells_bluetooth_earbuds must be Yes/No/Unknown")
        r["_tier"] = tier(score)
        tiers[r["_tier"]] += 1
    fields = [f for f in rows[0].keys() if f != "_tier"] if rows else []
    for t in ("tier1", "tier2", "tier3", "hold"):
        sub = [r for r in rows if r["_tier"] == t]
        if not sub:
            continue
        with open(os.path.join(out_dir, f"buyers_{t}.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            for r in sorted(sub, key=lambda x: -int(x.get("match_score") or 0)):
                w.writerow({k: r.get(k, "") for k in fields})
    print(f"rows={len(rows)} tiers={dict(tiers)}")
    print(f"problems={len(problems)}")
    for p in problems:
        print("  !", p)
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
