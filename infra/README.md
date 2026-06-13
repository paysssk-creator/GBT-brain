# GBT Brain - AI认知引擎 一键部署

## 一行命令部署

### Windows (PowerShell)
```powershell
irm bit.ly/gbt-brain-win | iex
```

### Mac / Linux / WSL
```bash
curl -fsSL bit.ly/gbt-brain | bash
```

### 任意系统 (Python环境已有)
```bash
pip install gbt-brain && gbt-brain init
```

---

## 系统能力

| 模块 | 功能 |
|------|------|
| Brain | AI记忆持久化 (零断连) |
| MindSpace | 思维空间 (GitHub+HN+Dev.to+Reddit实时采集) |
| DimensionSpace | 9维度推演分析 |
| MindMap | 多维思维导图延伸 |
| SelfEvolve | 每日自我进化 |
| BrainMirror | 3D认知图谱可视化 |

## 手动启动

```bash
cd vector_db
python mindspace.py       # 扫描全球技术热点
python self_evolve.py     # 自我进化分析
python brain_mirror.py    # 打开3D大脑镜像
python run_dimensions.py  # 全维度推演
```

## 数据库

- SQLite: vectors.db (永不停用)
- PostgreSQL+pgvector: Docker部署 (无限扩容)

## Brain统计
- 笔记: 79 | 学习: 80 | 模式: 32 | 决策: 2
- 镜像节点: 137 | 连接: 4200 | 维度: 9
