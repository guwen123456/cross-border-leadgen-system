# 外贸跨境获客系统 · Cross-Border Lead-Gen System

> 一套已经在实战中跑过的海外买家开发系统：采集 → 核验打分 → 质量门 → 个性化开发信 → 分波跟进。
> 开源的是**系统、模板和方法论**；真实客户名单是商业资产，不在本仓库内（样例数据全部为虚构）。

## 核心理念：买家先行

先找工厂比价、再拿价格找买家，是最常见的弯路 —— 买家对价格的了解不比你少。
本系统的顺序反过来：先核验买家 → 首信只问三个问题（价格带 / 认证要求 / 试单量）→
拿买家回复形成的真实需求单，再反向询工厂。完整方法论见 [docs/WORKFLOW.md](docs/WORKFLOW.md)。

## 系统组成

| 模块 | 内容 |
|---|---|
| `templates/` | 四张数据表结构（供应商 29 列 / 买家 19 列 / 订单利润 / 联系日志）、100 分制评分标准、开发信与询价模板 |
| `pipeline/validate_buyers.py` | 质量门：必填、打分理由、联系方式出处、品类不许猜；输出 tier1/2/3/hold 分层名单 |
| `pipeline/dedupe_merge.py` | 多批次合并去重（域名写法规范化），重复行出报告不静默删 |
| `pipeline/gen_outreach.py` | 逐封生成个性化开发信草稿；**没有事实钩子的行拒绝生成**；品类未确认的不许声称对方在卖耳机 |
| `pipeline/make_waves.py` | 按收件人时区分波，控制发送节奏（只做计划，不自动发送） |
| `sample_data/` + `examples/` | 虚构样例数据与完整演示运行记录 |

## 快速开始

```bash
# 合并两个批次并去重
python3 pipeline/dedupe_merge.py sample_data/buyers_all_sample.csv sample_data/buyers_batch_a.csv sample_data/buyers_batch_b.csv
# 质量门 + 分层
python3 pipeline/validate_buyers.py sample_data/buyers_all_sample.csv examples/
# 生成开发信草稿（人工审核后逐封发送）
python3 pipeline/gen_outreach.py examples/buyers_tier1.csv examples/letters/
# 分波计划
python3 pipeline/make_waves.py examples/buyers_tier1.csv
```

只依赖 Python 3 标准库，无需安装任何包。演示输出见 [examples/demo_run.md](examples/demo_run.md)。

## 实战验证（仅汇总数字，不含任何客户身份）

这套系统已用于一批蓝牙耳机品类的真实开发：两批共采集 146 家海外买家并逐家核验打分
（官网在售品类、公开商务联系方式出处逐项记录），识别并剔除了跨批次重复记录与
个别处于破产程序、不适合联系的目标；开发信按时区分波、逐封人工审核发送，全程留日志。

## 获客服务（试点）

系统作者同时提供人工核验版服务 —— 不是卖名单，是把买家一家家核验过并配好可直接用的开发信：

- **试点包 299 元**：30 家已核验买家 + 10 封个性化英文开发信 + 跟进信模板
- 先免费看 5 家样例，觉得质量行再决定
- 说清边界：保证核验质量和开发信可直接用，**不承诺回复或成交**

联系：邮箱 2671329805@qq.com · 微信 GGBondql

## 合规与边界

- 只采集企业在官网公开的商务联系方式，不采集私人信息
- 全部邮件逐封人工审核发送，不群发轰炸；对方明确拒绝立即停止
- 请遵守你所在法域与目标市场的反垃圾邮件法规（如 GDPR、CAN-SPAM）
- 名单是线索 + 核验记录，不是成交保证

## English summary

A working B2B cross-border lead-generation system: buyer-first sourcing, public-info verification with a 100-point scoring rubric, hard quality gates (no score without a stated basis, no contact without a source, no outreach without a company-specific hook), per-buyer personalized draft letters, and time-zone wave planning. Python 3 stdlib only. All sample data is fictional; real client lists are not included. A manually-verified buyer research service (30 verified buyers + 10 personalized outreach letters, 299 CNY pilot) is available — contact above.
