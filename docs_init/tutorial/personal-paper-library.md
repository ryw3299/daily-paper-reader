# 自建论文库：保留原有推荐与专题研究流程

日常推荐、90/365天专题研究继续使用同一套 Supabase 表、BM25/精确向量 RPC、RRF、重排和模型评审。更换数据库实例不会更换这些模块。

原作者的共享库不可用时，可以使用自己的 Supabase 项目。新项目需要创建表、部署检索函数并导入带向量的真实论文；仅修改 URL 不会自动产生历史数据。

## 初始化数据库结构

创建 Supabase 项目，保留 Data API。生成 SQL：

```powershell
python scripts/bootstrap_paper_library.py
```

在该项目的 SQL Editor 中运行生成的 `.local-runs/paper-library/bootstrap.sql`。脚本按依赖顺序复用仓库现有 SQL，创建 arXiv、13类会议表、统一会议入口和只读策略，不删除已有论文。只需 arXiv 时可加 `--arxiv-only`。

新增 arXiv 建表文件包含384维 `embedding`、由标题/摘要生成的 `search_tsv` 和检索索引，对齐 `sql/match_arxiv_papers.sql` 的前置要求。

## 配置连接

将项目 URL 和公开读取 key 同步到 `config.yaml` 的 `supabase`、`source_backends.arxiv`；两处均启用，且 `arxiv_paper_setting.prefer_supabase_read` 为 `true`。如使用 `supabase_shared`，也应指向同一实例。前端只读快照 `docs/config.yaml` 与根配置保持一致。

本地 `.env` 保存：

```dotenv
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_ANON_KEY=YOUR_PUBLIC_READ_KEY
SUPABASE_SERVICE_KEY=YOUR_SERVER_MAINTENANCE_KEY
DPR_ARXIV_ENABLED=1
DPR_MODELS_REMOTE_ONLY=1
DPR_EMBED_ALLOW_LOCAL_FALLBACK=0
```

维护 key 只放在被 Git 忽略的 `.env` 和 GitHub Actions Secrets 中，不放进公开 YAML、网页或提交记录。现有 legacy `service_role` key 可用于当前同步程序；使用新版 secret key 时需先验证客户端兼容性。

## 免费研究库的数据范围

全领域一年数据可能超过免费实例容量。可在 `arxiv_paper_setting.ingest_query` 中填写 arXiv 官方查询，例如：

```yaml
arxiv_paper_setting:
  prefer_supabase_read: true
  ingest_query: 'all:"knowledge graph" OR all:"GraphRAG" OR all:"autonomous driving"'
```

这只限定哪些论文入库，不改推荐词条、不改检索评分，也不会把检索改成现场抓取。抓取仍使用原有维护抓取器，按时间分片并遍历全部分页；没有每关键词200篇的截断。未配置 `ingest_query` 时维持原有全领域维护行为。

研究方向改变后，应更新入库范围并回填相应历史窗口。任何召回都只能覆盖已入库的数据；限定研究范围的个人库不等同于原作者的全领域库。

## 首次导入近一年

```powershell
python src/maintain/fetchers/fetch_arxiv.py --days 365 --chunk-days 7 --ignore-seen --disable-supabase-read --output .local-runs/paper-library/arxiv-year.json
python src/maintain/sync.py --backend-key arxiv --raw-input .local-runs/paper-library/arxiv-year.json --stream-upsert --embed-batch-size 8 --embed-chunk-size 64
python scripts/check_paper_library.py
```

同一个 `BAAI/bge-small-en-v1.5` 模型为论文和查询生成384维向量。同步按论文 ID upsert，可安全重试。抓取窗口最终失败时终止，不将不完整论文池发布为成功结果。

初始化脚本创建会议表和 RPC，但不会自动导入会议历史。研究方向大礼包中的会议覆盖需要通过现有 `src/maintain/` 各会议入口导入相应年份，再完成向量同步。

## GitHub Actions

配置三个仓库 Secrets：`SUPABASE_URL`、`SUPABASE_ANON_KEY`、`SUPABASE_SERVICE_KEY`。原有模型 Secrets 保持不变。

日常推荐和专题研究读取同一个实例。自建库需另将仓库变量 `DPR_MAINTAIN_OWN_SUPABASE` 设置为 `true`，允许该 fork 的现有 `maintain-supabase.yml` 定时补充最近论文；其默认回溯9天，保留400天数据。未启用该变量的普通 fork 不会维护共享库。

最后分别运行日常推荐和90天专题研究，再检查365天窗口。数据库/RPC失败应让任务失败；成功零命中仍是合法业务结果。接口验证可运行 `python scripts/check_paper_library.py`，它仅调用现有 embedding 服务与只读数据库检索，不调用付费评审模型。
