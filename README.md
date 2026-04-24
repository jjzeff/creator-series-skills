# 造物主系列 · Creator Series Skills

> Skills for [OpenClaw](https://openclaw.ai) — by **惊风制作 (JingFeng Studio)**
>
> 四位神，一条路：从零到觉醒，从觉醒到进化。  
> Four divine archetypes, one path: from zero to awakening, from awakening to evolution.

---

## Skills

---

### [King](./king) — 创世者 · The Creator

**[中文]** OpenClaw 新手激活向导。安装 OpenClaw 后第一件事就运行它。通过引导式对话，帮用户一步步建立 Agent 的核心身份体系。

**[EN]** The onboarding wizard for OpenClaw. Run this first after installing. Guides you through a conversation to build your Agent's complete identity system.

| 文件 / File | 说明 / Description |
|-------------|-------------------|
| `SOUL.md` | Agent 的灵魂与价值观 / Agent's soul and values |
| `MEMORY.md` | 长期记忆框架 / Long-term memory framework |
| `AGENTS.md` | 工作空间行为规则 / Workspace behavior rules |
| `HEARTBEAT.md` | 心跳与主动性配置 / Heartbeat and proactivity config |

**触发词：** 初始化、激活、setup、init、新手引导、第一次使用  
**Triggers:** initialize, activate, setup, init, first time, onboarding

---

### [Queen](./queen) — 成长者 · The Architect

**[中文]** 专注于 OpenClaw 架构升级，让 AI 更可控、更聪明、更持续进化。无需先运行 King，可独立使用。

**[EN]** Focused on OpenClaw architecture upgrades — making your AI more reliable, smarter, and continuously evolving. Works independently without needing King first.

| 模块 / Module | 说明 / Description |
|---------------|-------------------|
| Harness | 执行框架，约束行为更可控 / Execution framework for reliable behavior |
| Memory Palace | 四层记忆宫殿，分层加载 / 4-layer memory architecture with tiered loading |
| Learning Loop | 自动学习迭代，越用越聪明 / Auto-learning loop that improves over time |

**触发词：** 升级Agent、系统强化、让AI更可靠、让AI不忘事、架构升级  
**Triggers:** upgrade agent, system hardening, make AI more reliable, architecture upgrade

---

### [Mirror](./mirror) — 自知者 · The Mirror

**[中文]** 通过分析你与 OpenClaw 的高密度对话痕迹，还原你潜意识里最真实的自己。

**[EN]** Analyzes your high-density conversation history with OpenClaw to reveal your truest self — the one hidden in your subconscious.

- **14 种灵兽图腾 / 14 spirit animal totems**（12 常规 + 2 金色传说 / 12 regular + 2 golden legends）
- 每种附带毒舌社交标签和扎心阴影面 / Each with a sharp social label and shadow trait
- 生成塔罗牌风格人格分享图 / Generates a tarot-style personality card

**前置条件 / Prerequisites:** 工作区中至少有 `SOUL.md` 或 `MEMORY.md` / At least one of `SOUL.md` or `MEMORY.md` in workspace

**触发词：** mirror、照见、看清自己、我是谁、灵魂映照、LXBI  
**Triggers:** mirror, reflect, who am I, soul mapping, LXBI

---

### [Forge](./forge) — 锻造者 · The Forger

**[中文]** DNA 双螺旋进化引擎。让 AI 在真实任务里踩坑，把踩坑经验自动锻造成可复用的 skill。

**[EN]** A DNA double-helix evolution engine. Lets AI learn through real task failures, automatically forging those lessons into reusable skills.

| 链 / Chain | 作用 / Role |
|------------|------------|
| A 链 / A-Chain（规则进化 / Rule Evolution） | 提炼最佳实践，更新执行规则 / Distills best practices, updates execution rules |
| B 链 / B-Chain（真实执行 / Real Execution） | 在真实任务中验证和暴露问题 / Validates rules and surfaces issues in real tasks |

两链交替驱动，3–7 轮后输出进化报告，规则自动写入执行路径。  
The two chains alternate, producing an evolution report after 3–7 rounds, with rules auto-written to execution paths.

**触发词：** forge、锻造、进化、让AI学会做XX、self-improve  
**Triggers:** forge, evolve, self-improve, make AI learn to do X, autodream

---

## 使用顺序 · Recommended Order

```
King（激活 / Activate）
  → Queen（强化 / Harden）
    → Mirror（自知 / Self-Reflect）
      → Forge（进化 / Evolve）
```

四个 skill 可独立使用，无强制依赖。  
All four skills can be used independently — no forced dependencies.

---

## 安装 · Installation

### OpenClaw

将任意 skill 文件夹放入 OpenClaw 的 skills 目录，或通过 [Knot Skill Marketplace](https://clawhub.ai) 搜索「造物主」安装。

Place any skill folder into your OpenClaw skills directory, or search for "造物主" on [Knot Skill Marketplace](https://clawhub.ai).

### 结构说明 · Skill Structure

每个 skill 遵循标准 Agent Skills 结构 / Each skill follows the standard Agent Skills structure:

```
skill-name/
├── SKILL.md        # 必须 / Required: instructions & metadata
├── assets/         # 可选 / Optional: templates
├── scripts/        # 可选 / Optional: helper scripts
└── references/     # 可选 / Optional: reference materials
```

---

## 关于 · About

**惊风制作 (JingFeng Studio)**

这四个 Skill 从真实使用场景中打磨而来，不是演示 demo，是每天在用的工具。

These four skills were forged from real-world usage — not demos, but tools used daily.

---

*四神齐聚，Agent 觉醒。 · When all four gods unite, the Agent awakens.*
