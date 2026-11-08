# PickLens · 出海选品实验室

PickLens 是面向跨境卖家与新手的免费选品初筛工具，作为本仓库的独立静态子工具。

## 当前版本

- 单件贡献利润测算：售价、采购、物流包装、平台支付费、广告获客与售后预留。
- 100 分初筛模型：需求证据 30、利润空间 25、竞争环境 15、差异化 10、供应链可靠度 10、风险控制 10。
- 人工记录 Google Trends、平台成交、内容 / 广告等证据来源。
- 本地候选池、JSON 评估导出、CSV 候选池导出。
- 公开数据源快捷入口。
- 无登录、无后端、无埋点。候选池只保存在当前浏览器 localStorage。

## 重要边界

1. 当前版本不自动抓取 Google Trends、Amazon、TikTok、Meta、eBay 或 AliExpress 的数据。每个分数都来自使用者自行调研和输入。
2. Google Trends 反映相对搜索兴趣，不代表购买或成交。广告、短视频热度也不等于实际需求。
3. Amazon Best Sellers 榜单排名不能直接换算成销量。eBay Product Research 需要卖家账号权限。
4. 贡献利润没有扣除 VAT / 关税、仓储、人工、软件和固定管理成本。
5. 评分只用于候选品排序，不预测销量、不保证利润、不构成合规或投资意见。
6. Bluetooth earbuds 演示案例的价格、成本、渠道评分均为虚构演示数值，不是实时市场研究结果。

## GitHub Pages 部署

仓库 Settings → Pages → Build and deployment → Source 选择 GitHub Actions。完成后，推送 product-scout/ 目录的改动会自动触发部署。

部署成功后网址：
https://guwen123456.github.io/cross-border-leadgen-system/

如未启用 Pages，第一次部署可能失败。设置 Source 为 GitHub Actions 后，到 Actions 查看 Deploy PickLens to GitHub Pages 的运行结果。

## 小红书测试建议

先招募 20–30 位测试者，集中收集四类反馈：
- 是否能在 3 分钟内完成第一次评估；
- 哪个字段最难理解、最难找到数据；
- 评分结果是否与实际经营经验相符；
- 是否需要增加平台费用模板、类目风险检查或竞品对比。

建议测试者导出 JSON 报告后，自愿通过小红书私信回传；请勿在公开评论区提交个人联系方式、账号密码或商业机密。
