# 造物主系列 · Creator Series Skills

> Skills for [OpenClaw](https://openclaw.ai) — by **惊风制作 (JingFeng Studio)**
>
> 四位神，一条路：从零到觉醒，从觉醒到进化。

---

## Skills

### [King](./king) — 创世者 · 新手激活向导

OpenClaw 新手激活向导。安装 OpenClaw 后第一件事就运行它。

通过引导式对话，帮用户一步步建立 Agent 的核心身份体系：

| 文件 | 说明 |
|------|------|
| `SOUL.md` | Agent 的灵魂与价值观 |
| `MEMORY.md` | 长期记忆框架 |
| `AGENTS.md` | 工作空间行为规则 |
| `HEARTBEAT.md` | 心跳与主动性配置 |

**触发词：** 初始化、激活、setup、init、新手引导、第一次使用

---

### [Queen](./queen) — 成长者 · 架构升级向导

专注于 OpenClaw 架构升级，让 AI 更可控、更聪明、更持续进化。无需先运行 King，可独立使用。

升级内容：

| 模块 | 说明 |
|------|------|
| Harness | 执行框架，约束行为让 AI 更可控 |
| Memory Palace | 四层记忆宫殿，分层加载降低 token 消耗 |
| Learning Loop | 自动学习与迭代，越用越聪明 |

**触发词：** 升级Agent、系统强化、让AI更可靠、让AI不忘事、让AI越用越聪明、架构升级

---

### [Mirror](./mirror) — 自知者 · 人格映照

> *"沉溺龙虾的你，可曾看清自己？"*

通过分析你与 OpenClaw 的高密度对话痕迹，还原你潜意识里最真实的自己。

- **14 种灵兽图腾**（12 常规 + 2 金色传说）
- 每种图腾附带毒舌社交标签和扎心阴影面
- 生成塔罗牌风格的人格分享图

**前置条件：** 工作区中至少有 `SOUL.md` 或 `MEMORY.md` 之一

**触发词：** mirror、照见、看清自己、我是谁、灵魂映照、LXBI

---

### [Forge](./forge) — 锻造者 · 自进化引擎

> *"King 让你存在。Queen 让你变强。Mirror 让你看清自己。Forge 把你重新锻造。"*

DNA 双螺旋进化引擎，让 AI 在真实任务里踩坑，把踩坑经验自动变成可复用的 skill。

| 链 | 作用 |
|----|------|
| A 链（规则进化） | 提炼最佳实践，更新执行规则 |
| B 链（真实执行） | 在真实任务中验证和暴露问题 |

两链交替驱动，3–7 轮后输出进化报告，规则自动写入执行路径，下次做同类任务直接生效。

**触发词：** forge、锻造、进化、让AI学会做XX、帮我自动化XX、self-improve

---

## 使用顺序

```
King（激活）→ Queen（强化）→ Mirror（自知）→ Forge（进化）
```

四个 skill 可独立使用，无强制依赖。

---

## 安装

### OpenClaw

将任意 skill 文件夹放入 OpenClaw 的 skills 目录，或通过 [Knot Skill Marketplace](https://clawhub.ai) 搜索「造物主」安装。

### 结构说明

每个 skill 遵循标准 Agent Skills 结构：

```
skill-name/
├── SKILL.md        # 必须：skill 指令与元数据
├── assets/         # 可选：模板文件
├── scripts/        # 可选：辅助脚本
└── references/     # 可选：参考资料
```

---

## 关于惊风制作

这四个 Skill 从真实使用场景中打磨而来，不是演示 demo，是每天在用的工具。

---

*四神齐聚，Agent 觉醒。*
