# Phase 2：SkillHub 动态推荐与安装

## 开场白（固定）

> "你的 Agent 基础配置完成了 🎉
> 但光有身份和记忆还不够——**技能决定它能做什么**。
> 我来基于你的 SOUL.md，去 SkillHub 上给你找几个最值得装的 skill。稍等一下……"

---

## Step 1：读取 SOUL.md，提取检索关键词

从已生成的 SOUL.md 中提取：
- `{{USER_ROLE}}`：工作身份
- `{{PRIMARY_PURPOSE}}`：主要用途

转化为 2-3 个搜索关键词，例如：
- 游戏发行 → `"游戏 情报"` + `"排行榜"`
- 内容创作 → `"视频 创作"` + `"翻译"`
- 开发者 → `"代码 仓库"` + `"工程"`
- 通用 → `"搜索 新闻"` + `"效率"`

---

## Step 2：在 skillhub.cn 搜索

访问 `https://skillhub.cn/skills?search=<关键词>` 用 browser 工具获取搜索结果。

提取每个 skill 的：
- slug（URL 中的 `/skills/<slug>`）
- 名称、分类、下载量、收藏数
- 简短描述

多关键词搜索 2 次，合并结果，按下载量降序，去重，取前 8 个候选。

---

## Step 3：展示推荐列表

> "根据你的 SOUL.md（{{USER_ROLE}}，主要做{{PRIMARY_PURPOSE}}），我从 SkillHub 找到这些适合你的技能："

展示格式：

```
1. Weather — 获取当前天气和预报，无需 API Key（下载 15.7万）
2. News Summary — 国际新闻日报 + 语音摘要（下载 3.7万）
3. ...
```

> "你想怎么装？
> - 说「**全装**」→ 我帮你一个个装上
> - 说「装 1 3」→ 只装序号对应的
> - 说「**跳过**」→ 以后随时可以到 https://skillhub.cn 自己装"

---

## Step 4：执行安装

用户确认后，对每个要装的 skill，使用 `knot_skills install` 工具，传入对应的 skillId：

```
action: install
skillId: <skill 的数字 id>
```

如果 knot_skills 无法安装，退回到 SkillHub 的对话安装提示词方式：
告知用户把以下提示词发给 Agent：
> "请先检查是否已安装 SkillHub 商店，若未安装，请根据 https://skillhub.cn/install/skillhub.md 安装，然后安装 `<skill名>` 技能。"

每装完一个：
- 告知安装成功 ✅
- 一句话说明怎么触发（如："说'查天气'就能用"）

---

## 兜底逻辑

如果搜索无相关结果，展示 SkillHub 热榜前几名作为通用推荐：
- `self-improving-agent`（AI 增强，下载 45.7万）
- `find-skills`（技能发现工具，33.4万）
- `summarize`（信息处理，31.8万）
- `weather`（天气，15.7万）
- `news-summary`（新闻，3.7万）

---

## SkillHub 完成后 → 进入 STATE_T（腾讯员工专属增强）

SkillHub 安装完成后，**不要直接输出结束语**，先进入 `references/state-tencent.md` 的腾讯员工引导流程。

- 用户确认是腾讯员工 → 执行 STATE_T（安装 iWiki MCP + 建 iWiki 目录）
- 用户跳过 → 直接进入 STATE_END

---

## 结束语（STATE_END，固定）

> "全部完成 🎉
> **{{AGENT_NAME}}** 现在有了：
> ✅ 身份与原则（SOUL.md）
> ✅ 核心团队（AGENTS.md）
> ✅ 记忆系统（MEMORY.md）
> ✅ 定时情报站（HEARTBEAT.md）
> ✅ {{INSTALLED_COUNT}} 个专属技能
> {{IWIKI_LINE}}
>
> 直接跟它说话就行，它知道自己是谁，也知道该怎么帮你。
> 更多技能随时可以去 👉 https://skillhub.cn 自己探索。
>
> ——**惊风制作**出品"

> `{{IWIKI_LINE}}` 规则：
> - 如果完成了 STATE_T：`✅ iWiki 知识库（{{AGENT_NAME}}-智库目录已建好）`
> - 如果跳过 STATE_T：留空，不输出这一行
