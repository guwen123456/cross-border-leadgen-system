#!/usr/bin/env python3
"""按买家逐封生成个性化开发信（草稿，不发送）。

硬规则（来自实战模板 templates/outreach_templates.md）：
- 每封信必须有一个针对这家公司的具体事实钩子（notes 里的 personalization hook）。
  没有钩子的行直接跳过并报告 —— 宁可不发，不发群发感的信。
- sells_bluetooth_earbuds 不是 Yes 的，不许在信里声称对方在卖耳机，
  自动改用中性品类说法。
- 生成的只是草稿，发送前逐封人工审核。

用法: python3 gen_outreach.py buyers.csv out_dir
"""
import csv, sys, os

LETTER = """Subject: TWS earbuds — small MOQ trial from Shenzhen

Hi {name},

I noticed {company} {hook}. We work with Shenzhen factories on TWS earbuds (Bluetooth 5.3, CE/FCC documents available per model, checked against the exact model before quoting).

What we can offer: model-by-model certification file checks, pre-shipment QC, mixed-model trial orders and custom packaging. If you can share three things — your best-selling price band, the certification your market requires, and a trial quantity — I will come back with a verified shortlist instead of a generic catalogue.

Best regards,
Richard — Shenzhen, China
"""

LETTER_NEUTRAL = LETTER.replace("TWS earbuds — small MOQ trial", "Consumer audio sourcing — small trial orders")

def main():
    src, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    made, skipped = 0, []
    for r in csv.DictReader(open(src, encoding="utf-8-sig")):
        hook = (r.get("notes") or "").strip()
        company = (r.get("company_name") or "").strip()
        if not hook or not company:
            skipped.append(r.get("buyer_id") or company or "?")
            continue
        tpl = LETTER if (r.get("sells_bluetooth_earbuds") or "").strip() == "Yes" else LETTER_NEUTRAL
        body = tpl.format(name="team", company=company, hook=hook)
        fname = f"{r.get('buyer_id') or 'B'}_{company.replace(' ', '_')}.md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as fh:
            fh.write(f"<!-- DRAFT for {company} ({r.get('country','')}) — review before sending -->\n\n{body}")
        made += 1
    print(f"letters_generated={made} skipped_no_hook={len(skipped)} {skipped if skipped else ''}")

if __name__ == "__main__":
    main()
