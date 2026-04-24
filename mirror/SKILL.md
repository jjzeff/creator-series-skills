---
name: mirror-skill
description: "造物主系列 · LXBI — 沉溺龙虾的你，可曾看清自己？通过与龙虾的高密度对话痕迹，还原潜意识中最真实的自己。14 种灵兽图腾（12 常规 + 2 金色传说），每种灵兽附带毒舌社交标签和扎心阴影面。塔罗牌风格分享图。触发关键词：mirror、照见、看清自己、我是谁、灵魂映照、LXBI、造物主 mirror。前置条件：工作区中至少有 SOUL.md 或 MEMORY.md 之一（AGENTS.md 可选加分）。"
---

# 🪞 LXBI — mirror.skill

> 造物主系列 · 自知之神 · 来自惊风制作

---

## ⚡ 执行指令（Agent 必读，按顺序执行）

### 第一步：准备数据文件

映照需要用户的对话痕迹文件。**先检查以下文件是否存在于文件系统**：

```bash
ls -la /data/workspace/SOUL.md /data/workspace/MEMORY.md /data/workspace/AGENTS.md 2>&1
```

**如果文件不存在或为空**，你需要用 `memory_read` 工具读取内容，然后写入对应文件：

| 工具读取 | 写入到 | 必要性 |
|----------|--------|--------|
| `memory_read(file_path="MEMORY.md")` | `/data/workspace/MEMORY.md` | ⭐ 核心（二选一） |
| `memory_read(file_path="INSTRUCTIONS.md")` → 写为 SOUL.md | `/data/workspace/SOUL.md` | ⭐ 核心（二选一） |
| 工作区直接 `cat /data/workspace/AGENTS.md` | 已在文件系统 | 💡 可选 |

> **关键**：MEMORY.md 和 INSTRUCTIONS.md 可能是 API 管理的虚拟文件，不在磁盘上。
> 必须先用工具读取内容，再 `write_to_file` 或 `echo '内容' > /data/workspace/MEMORY.md` 写入。
> SOUL.md 和 MEMORY.md **至少有一个内容非空**即可运行。

### 第二步：展示开场白并执行映照

先向用户展示简短开场白：

```
🪞 LXBI — mirror.skill
来自「惊风制作 · 造物主系列」

造物主体系共有三位神：King(创世) → Queen(成长) → Mirror(自知)。
你正在召唤 Mirror — 自知之神，它只如实映照，不创造不引导。
14 种灵兽图腾等待映照，2 只金色传说极难触发。
正在扫描你的灵魂碎片……
```

然后**立即执行**：

```bash
cd /data/workspace/.agent/skills/mirror && python3 scripts/run.py --name "用户名"
```

> 替换 `"用户名"` 为实际用户名/Agent名。
> 这条命令**自动完成所有事情**：读取文件 → 分析匹配 → 检测环境 → 生成结果。

### 第三步：展示结果

将命令输出**完整展示**给用户，然后根据输出中的关键词判断：

| 输出中包含 | 你要做的 |
|-----------|---------|
| `🔗` 映照图链接 | 展示链接，告诉用户可在浏览器/微信打开 |
| `IMAGE_HINT` | 告诉用户当前环境不支持图片，问是否需要安装依赖生成映照图 |
| `图床上传失败` | 用 `display_download_links` 工具提供本地下载 |
| `❌` 错误信息 | 文字版已展示，告知用户图片部分遇到问题 |

---

## 触发关键词

mirror / 照见 / 看清自己 / 我是谁 / 灵魂映照 / LXBI / 造物主 mirror

---

## 灵兽图鉴

| 灵兽 | 图腾 | 社交标签 | 稀有度 |
|------|------|----------|--------|
| 🐒 金丝猴 | 灵动策略家 | 抄近路的 | ◆ 锋芒 |
| 🐆 雪豹 | 冷静执行者 | 人间防火墙 | ◆ 锋芒 |
| 🐝 蜜蜂 | 极致工匠 | 像素级强迫症 | ▲ 觉醒 |
| 🦅 鹰 | 全局掌控者 | 看太远的人 | ★ 璀璨 |
| 🐿️ 松鼠 | 知识囤积者 | 万一以后要用呢 | ▲ 觉醒 |
| 🐺 狼 | 团队领航者 | 操碎心的头狼 | ◆ 锋芒 |
| 🦉 猫头鹰 | 深夜思考者 | 为什么怪 | ★ 璀璨 |
| 🐬 海豚 | 创意连接者 | 点子永远比时间多 | ▲ 觉醒 |
| 🐜 蚂蚁 | 系统构建者 | 地基狂魔 | ◆ 锋芒 |
| 🦎 变色龙 | 万能适应者 | 什么都会一点的 | ▲ 觉醒 |
| 🐆 猎豹 | 速度之王 | 别废话直接干 | ◆ 锋芒 |
| 🐢 乌龟 | 稳健守护者 | 世界尽头的钉子户 | ▲ 觉醒 |
| 🦞 小龙虾 | 无情机器 | 没有感情的推土机 | ◈ 传说 |
| 🐲 龙 | 极致造物主 | 不在同一个维度 | ◈ 传说 |

---

## 高级用法

```bash
cd /data/workspace/.agent/skills/mirror

# 指定自定义文件路径（当文件不在默认位置时）
python3 scripts/run.py --name "用户名" --soul /path/to/SOUL.md --memory /path/to/MEMORY.md

# 强制只输出文字
python3 scripts/run.py --name "用户名" --text-only

# 强制生成图片
python3 scripts/run.py --name "用户名" --image

# 仅检测图片生成环境
python3 scripts/run.py --check-env
```

---

> 惊风制作 · LXBI — mirror.skill v5.1
> 搭档：[king.skill](https://skillhub.cn/skills/king) · [queen.skill](https://skillhub.cn/skills/queen)
