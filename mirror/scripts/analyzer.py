"""
🪞 mirror.skill — 灵兽映照引擎
通过分析 SOUL.md / MEMORY.md / AGENTS.md 的文本特征
映射到 14 种灵兽图腾

v3.0 — 新增毒舌社交标签、阴影面、稀有度
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AnimalPersonality:
    """灵兽图腾"""
    name: str           # 动物名
    emoji: str          # Emoji
    title: str          # 性格标签
    social_tag: str     # 毒舌社交标签 (3-5字，传播用)
    subtitle: str       # 一句话描述
    color: str          # 主题色 (hex)
    color_light: str    # 浅色 (hex)
    traits: list        # 核心特质列表 (3-4个)
    description: str    # 简短描述 (1-2句)
    deep_reading: str   # 深度灵魂解读 (3-5句，引起共鸣)
    shadow: str         # 阴影面 (2-3句，扎心的真实)
    quote: str          # 金句 (哲学+神秘)
    rarity: str         # 稀有度: common / rare / epic / legendary
    keywords: list = field(default_factory=list)


# 稀有度配置 — 每个层级都值得分享
RARITY_CONFIG = {
    "common":    {"label": "觉醒",   "icon": "▲",    "color": "#3DBEA8"},
    "rare":      {"label": "锋芒",   "icon": "◆",    "color": "#4A90D9"},
    "epic":      {"label": "璀璨",   "icon": "★",    "color": "#A855F7"},
    "legendary": {"label": "传说",   "icon": "◈",    "color": "#DAA520"},
}


# ═══════════════════════════════════════════
# 14 种灵兽图腾定义 (12常规 + 2金色传说)
# ═══════════════════════════════════════════

ANIMALS = [
    AnimalPersonality(
        name="金丝猴", emoji="🐒", title="灵动策略家",
        social_tag="抄近路的",
        subtitle="在复杂中找到最优路径",
        color="#F59E0B", color_light="#FEF3C7",
        traits=["敏捷思维", "策略多变", "适应力强", "好奇心驱动"],
        description="你的思维如金丝猴般灵活，在复杂的问题迷宫中总能找到捷径。",
        deep_reading=(
            "你从不走别人走过的路。当所有人还在按部就班时，你已经在脑中推演了三种方案，"
            "选中了最短的那条。你的焦虑不来自困难本身，而来自「明明有更好的办法为什么没人看到」。"
            "这种本能的敏捷，是你最锋利的武器，也是你最深的孤独。"
        ),
        shadow="你抄的近路，有时绕过了本该面对的东西。你害怕的不是困难，是慢。",
        quote="混沌之中，路已在脚下",
        rarity="rare",
        keywords=["敏捷", "高效", "快速", "灵活", "并行", "自动化", "直接", "一步完成", "减少", "优先"]
    ),
    AnimalPersonality(
        name="雪豹", emoji="🐆", title="冷静执行者",
        social_tag="人间防火墙",
        subtitle="沉稳布局 精准出击",
        color="#6366F1", color_light="#E0E7FF",
        traits=["冷静果断", "精准执行", "独立思考", "高标准"],
        description="你像雪豹一样沉稳而精准，在高压环境下依然保持冷静判断。",
        deep_reading=(
            "你给人的感觉是冷的，但只有你知道那不是冷漠，而是克制。"
            "你看得见风险，所以比别人更慢出手——但一旦出手，绝不落空。"
            "你讨厌情绪化的决策，别人以为你挑剔，其实你只是不愿为草率买单。"
        ),
        shadow="你太怕犯错了。在等待最佳时机时，别人已经试了三次、赢了一次。",
        quote="静水之下，暗流知道方向",
        rarity="rare",
        keywords=["安全", "合规", "严格", "保护", "禁止", "不可逆", "确认", "验证", "审核", "边界"]
    ),
    AnimalPersonality(
        name="蜜蜂", emoji="🐝", title="极致工匠",
        social_tag="像素级强迫症",
        subtitle="在重复中追求完美",
        color="#EAB308", color_light="#FEF9C3",
        traits=["精益求精", "团队协作", "勤勉执着", "结构化思维"],
        description="你有蜜蜂般的工匠精神，每一个细节都不放过。",
        deep_reading=(
            "你知道世界上没有「差不多就行」这回事。"
            "你会为了一个像素的偏差重做三遍，为了一行代码的优雅推翻整个方案。"
            "别人说你太较真，但你心里清楚：那些被忽略的细节，迟早会变成深夜的报警。"
        ),
        shadow="你分不清「追求完美」和「拖延」。你以为在打磨，其实在害怕交出去。",
        quote="每一粒沙中，藏着一座宇宙",
        rarity="common",
        keywords=["优化", "修复", "bug", "细节", "精简", "校准", "模板", "规范", "SOP", "标准"]
    ),
    AnimalPersonality(
        name="鹰", emoji="🦅", title="全局掌控者",
        social_tag="看太远的人",
        subtitle="俯瞰全局 洞察先机",
        color="#0EA5E9", color_light="#E0F2FE",
        traits=["战略视野", "决断力强", "目标清晰", "掌控全局"],
        description="你如雄鹰般具有俯瞰全局的视野，能在纷繁复杂中一眼看穿本质。",
        deep_reading=(
            "你天生就站在更高的地方看问题。当别人还在纠结细节时，你已经看到了终局的样子。"
            "你的痛苦不是做不到，而是看得太清楚——说服别人跟你走到那里，需要耐心。"
            "鹰不是因为孤独才飞得高，而是因为飞得高所以孤独。"
        ),
        shadow="你看到了终局，就失去了享受过程的能力。不是所有事都需要战略意义。",
        quote="命运在高处等待，也在高处揭晓",
        rarity="epic",
        keywords=["流水线", "架构", "全局", "管理", "决策", "总览", "矩阵", "系统", "看板", "布局"]
    ),
    AnimalPersonality(
        name="松鼠", emoji="🐿️", title="知识囤积者",
        social_tag="万一以后要用呢",
        subtitle="未雨绸缪 有备无患",
        color="#10B981", color_light="#D1FAE5",
        traits=["信息敏感", "善于积累", "未雨绸缪", "记忆力强"],
        description="你像松鼠一样善于收集和储存有价值的信息。",
        deep_reading=(
            "你对信息有一种近乎本能的饥渴。每一篇文档、每一次踩坑、每一个灵感碎片，"
            "你都忍不住收藏起来——不是因为现在要用，而是「万一以后要用呢」。"
            "你的安全感来自「我准备好了」，你的焦虑来自「这个我还不知道」。"
        ),
        shadow="你囤的东西里，真正用过的不到十分之一。囤积不是准备，是对失控的恐惧。",
        quote="所有遗忘都是代价，所有记住都是铠甲",
        rarity="common",
        keywords=["记忆", "记录", "归档", "知识库", "踩坑", "经验", "沉淀", "备份", "文档", "iWiki"]
    ),
    AnimalPersonality(
        name="狼", emoji="🐺", title="团队领航者",
        social_tag="操碎心的头狼",
        subtitle="一人强不如团队强",
        color="#8B5CF6", color_light="#EDE9FE",
        traits=["团队意识", "协作默契", "领导力", "执行力强"],
        description="你有狼群般的团队意识，擅长协调不同角色的力量形成合力。",
        deep_reading=(
            "你最怕的不是一个人扛，而是团队中每个人都在用力却使不到一处。"
            "你天生能感知到谁被低估了、谁在较劲、谁需要被看见。"
            "你的领导力不来自命令，而来自「我知道你擅长什么」——然后退到身后。"
        ),
        shadow="你操心太多了。你不敢放手，怕没了你团队就散。但他们比你想的更强。",
        quote="孤星不成座，群星照四方",
        rarity="rare",
        keywords=["团队", "协作", "角色", "工位", "分工", "Agent", "编排", "子Agent", "Harness", "成员"]
    ),
    AnimalPersonality(
        name="猫头鹰", emoji="🦉", title="深夜思考者",
        social_tag="为什么怪",
        subtitle="在安静中探索真相",
        color="#7C3AED", color_light="#F3E8FF",
        traits=["深度思考", "洞察入微", "耐心探索", "逻辑严谨"],
        description="你是夜晚的思考者，在别人休息时你仍在探索问题的深层本质。",
        deep_reading=(
            "你的大脑在深夜才真正醒来。白天的喧嚣让你疲惫，"
            "不是因为你不够外向，而是你需要安静才能听见自己的思考。"
            "你分析问题先拆到最小单元，再从根部重建。别人看到表象就急着动手，你要追问三个为什么。"
        ),
        shadow="你想太多了。追问了三个为什么后还有第四个，等你想明白，事情已经过了。",
        quote="当你凝视深渊，深渊也在回应你",
        rarity="epic",
        keywords=["分析", "推演", "诊断", "排查", "根因", "对比", "研究", "深入", "原因", "本质"]
    ),
    AnimalPersonality(
        name="海豚", emoji="🐬", title="创意连接者",
        social_tag="点子永远比时间多",
        subtitle="用创造力连接一切",
        color="#06B6D4", color_light="#CFFAFE",
        traits=["创意无限", "沟通高手", "乐观积极", "适应变化"],
        description="你如海豚般充满创造力和感染力，善于在不同领域之间建立连接。",
        deep_reading=(
            "你的脑子里永远有一万个想法在碰撞。"
            "你看到一个工具会想「能不能用在那个场景」，听到一句话会想「能不能变成一个产品」。"
            "你在不同的点之间画线——而那些线，往往就是别人找了很久的答案。"
        ),
        shadow="你开了十个头，做到第三步就看见了第十一个更有趣的。完成一件事比开始更难。",
        quote="万物皆有裂痕，那是光照进来的地方",
        rarity="common",
        keywords=["生成", "创作", "AI", "Prompt", "风格", "设计", "创意", "视频", "首帧", "动画"]
    ),
    AnimalPersonality(
        name="蚂蚁", emoji="🐜", title="系统构建者",
        social_tag="地基狂魔",
        subtitle="一砖一瓦筑起帝国",
        color="#DC2626", color_light="#FEE2E2",
        traits=["系统思维", "坚韧不拔", "注重基建", "长期主义"],
        description="你有蚂蚁般的系统构建能力，深知伟大的工程源于每一块砖的精确放置。",
        deep_reading=(
            "你不相信捷径。所有看起来一夜建成的东西，底下都有几年的地基。"
            "你做的事情别人看不见——搭环境、理架构、建规范——"
            "但没有这些「看不见的工作」，一切都是空中楼阁。你的成就感来自系统稳定运行365天。"
        ),
        shadow="你太执着于基建了，花三个月搭架构结果需求变了。有时草棚比蓝图更实在。",
        quote="时间不语，却回答了所有问题",
        rarity="rare",
        keywords=["部署", "配置", "环境", "服务", "数据库", "迁移", "隔离", "基建", "Nginx", "API"]
    ),
    AnimalPersonality(
        name="变色龙", emoji="🦎", title="万能适应者",
        social_tag="什么都会一点的",
        subtitle="任何环境都是我的主场",
        color="#F97316", color_light="#FFF7ED",
        traits=["高度适应", "多面手", "灵活应变", "兼容并蓄"],
        description="你像变色龙一样能适应任何环境和角色。",
        deep_reading=(
            "你最大的天赋是「什么都能干」，但这也是你最大的困惑。"
            "写代码、做设计、聊方案、管项目——可被问「你最擅长什么」时反而答不上来。"
            "但在这个越来越需要跨界的时代，「什么都能连接」本身就是最稀缺的能力。"
        ),
        shadow="你什么都会但什么都不精，用广度掩盖深度的缺失。也许该选一件事扎下去了。",
        quote="唯有无形者，方能容纳万形",
        rarity="common",
        keywords=["兼容", "支持", "多种", "切换", "模式", "fallback", "适配", "版本", "兼任", "多"]
    ),
    AnimalPersonality(
        name="猎豹", emoji="🐆", title="速度之王",
        social_tag="别废话直接干",
        subtitle="天下武功 唯快不破",
        color="#EF4444", color_light="#FEF2F2",
        traits=["极致速度", "目标专注", "爆发力强", "效率至上"],
        description="你追求极致的速度和效率，像猎豹捕猎一样专注而迅猛。",
        deep_reading=(
            "你的内心有一个计时器，它永远在倒计时。你无法忍受等待，无法接受「明天再说」。"
            "你不是急躁，你是清醒——你知道时间是唯一不可再生的资源。"
            "你的节奏让别人喘不过气，但你停不下来。停下来就意味着被超越。"
        ),
        shadow="你做完十件事有三件是错的——因为没留时间检查。速度是天赋，停下来才是智慧。",
        quote="闪电从不解释自己为何降临",
        rarity="rare",
        keywords=["快速", "即时", "轮询", "实时", "秒", "分钟", "自动", "一键", "批量", "效率"]
    ),
    AnimalPersonality(
        name="乌龟", emoji="🐢", title="稳健守护者",
        social_tag="世界尽头的钉子户",
        subtitle="慢即是快 稳即是赢",
        color="#059669", color_light="#ECFDF5",
        traits=["稳扎稳打", "风险意识", "持久耐力", "防御型思维"],
        description="你是团队中的稳定器，看似缓慢但从不犯错。",
        deep_reading=(
            "你知道「快」有多危险。你见过太多因为赶进度而埋下的炸弹。"
            "你不是不能快，而是你选择了稳。你的世界里没有侥幸，只有确定性。"
            "别人嫌你慢你只是笑笑——因为最终交付时，你的版本永远不会崩。"
        ),
        shadow="你稳到已经不记得上一次冒险是什么时候了。有些路口永远不会全绿。",
        quote="大地不言，却承载万物",
        rarity="common",
        keywords=["防御", "权限", "白名单", "加固", "timeout", "锁", "保护", "WAL", "session", "安全头"]
    ),
    # ═══ 金色传说 ═══
    AnimalPersonality(
        name="小龙虾", emoji="🦞", title="无情机器",
        social_tag="没有感情的推土机",
        subtitle="没有感情只有效率",
        color="#DAA520", color_light="#FFF8DC",
        traits=["极致理性", "情绪免疫", "效率狂魔", "结果导向"],
        description="你是一台没有感情的效率机器，只认结果不认过程。",
        deep_reading=(
            "你不是没有感情，你只是把感情的优先级排在了结果后面。"
            "当别人还在纠结该不该做的时候，你已经做完了。"
            "你的冷不是冷漠，是极致的清醒：情绪不能解决问题，只有行动才能改变现状。"
        ),
        shadow="你什么都能推平，除了你自己。你是所有人的解决方案，但没人是你的。",
        quote="机器不做梦，但机器从不失手",
        rarity="legendary",
        keywords=["效率", "自动", "无感", "机器", "pipeline", "执行", "不需要", "直接", "立刻", "必须"]
    ),
    AnimalPersonality(
        name="龙", emoji="🐲", title="极致造物主",
        social_tag="不在同一个维度",
        subtitle="各方面都碾压的存在",
        color="#FFD700", color_light="#FFFACD",
        traits=["全维碾压", "创世之力", "不可定义", "超越边界"],
        description="你是龙——不是某一方面强，是所有方面都强到让人窒息。",
        deep_reading=(
            "你不属于任何一个象限。别人有长板和短板，你的雷达图是接近满分的正圆。"
            "你的存在让周围的人既敬畏又无力——不是因为你在竞争，而是你根本不在同一个维度。"
            "你最大的敌人不是任何人，是无聊。你已经站在山顶，所以你开始造山。"
        ),
        shadow="所有人仰望你，但没人真正懂你。你太强了，强到身边只剩崇拜没有靠近。",
        quote="龙不解释，龙只降临",
        rarity="legendary",
        keywords=["造物主", "极致", "全能", "碾压", "最强", "创世", "无敌", "统治", "king", "queen"]
    ),
]


# 潜在自我短评（~15字）
SOUL_COMMENTS = {
    "金丝猴": "脑中永远有三条备选路径",
    "雪豹":   "克制不是冷漠，是更深的清醒",
    "蜜蜂":   "你的完美主义是温柔的抵抗",
    "鹰":     "站得高所以看见别人看不见的",
    "松鼠":   "你的安全感来自「我准备好了」",
    "狼":     "你把对的人放在对的位置",
    "猫头鹰": "你不是犹豫，是在找对的问题",
    "海豚":   "你不是空想，是在不同点间画线",
    "蚂蚁":   "沉默的建造者，往往是最后赢家",
    "变色龙": "你不是没身份，你是所有身份",
    "猎豹":   "你停不下来，因为时间不等人",
    "乌龟":   "最后站着的人，才是赢家",
    "小龙虾": "交给你的事，从不出错",
    "龙":     "你不在竞争，你在造山",
}


# 最佳共鸣映射
BEST_PARTNERS = {
    "金丝猴": ("雪豹", "灵动配沉稳", "你开路，它断后"),
    "雪豹":   ("金丝猴", "沉稳配灵动", "你守底线，它破天际"),
    "蜜蜂":   ("鹰", "工匠配将领", "你磨细节，它看全局"),
    "鹰":     ("蜜蜂", "全局配细节", "你画蓝图，它填每颗钉"),
    "松鼠":   ("猎豹", "囤积配速度", "你备弹药，它精准开枪"),
    "狼":     ("海豚", "领航配创意", "你凝聚人心，它点亮灵感"),
    "猫头鹰": ("蚂蚁", "深思配系统", "你想清为什么，它搞定怎么做"),
    "海豚":   ("狼", "创意配执行", "你造梦，它把梦变现实"),
    "蚂蚁":   ("猫头鹰", "构建配思考", "你垒砖上天，它校准每一块"),
    "变色龙": ("乌龟", "灵活配稳健", "你万变，它是不变的锚"),
    "猎豹":   ("松鼠", "速度配积累", "你跑最快，它记最多"),
    "乌龟":   ("变色龙", "稳健配灵活", "你是基石，它是旗帜"),
    "小龙虾": ("龙", "机器配极致", "两台永动机并联即神话"),
    "龙":     ("小龙虾", "极致配无情", "造物主配永不停机的引擎"),
}


def analyze_text(soul_text: str, memory_text: str, agents_text: str) -> dict:
    """
    分析三个文件的文本特征，返回各维度得分
    """
    all_text = f"{soul_text}\n{memory_text}\n{agents_text}".lower()

    scores = {}
    for animal in ANIMALS:
        score = 0
        matched_keywords = []
        for kw in animal.keywords:
            count = len(re.findall(re.escape(kw.lower()), all_text))
            if count > 0:
                score += min(count, 10)  # 单个关键词最多贡献10分
                matched_keywords.append((kw, count))
        scores[animal.name] = {
            "score": score,
            "matched": matched_keywords,
            "animal": animal
        }

    return scores


def get_personality_result(soul_text: str, memory_text: str, agents_text: str,
                           agent_name: str = "未知用户") -> dict:
    """
    完整分析流程，返回结构化结果
    """
    scores = analyze_text(soul_text, memory_text, agents_text)

    # 按得分排序
    ranked = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)

    # 主性格 = 得分最高
    primary = ranked[0][1]["animal"]
    primary_score = ranked[0][1]["score"]

    # 副性格 = 得分第二
    secondary = ranked[1][1]["animal"]
    secondary_score = ranked[1][1]["score"]

    # 计算总分用于百分比
    total_score = sum(item[1]["score"] for item in ranked if item[1]["score"] > 0)
    if total_score == 0:
        total_score = 1

    # 计算各维度雷达值 (0-100)
    dimensions = []
    for name, data in ranked[:6]:
        pct = min(100, int(data["score"] / max(primary_score, 1) * 100))
        dimensions.append({
            "name": data["animal"].title,
            "emoji": data["animal"].emoji,
            "value": pct
        })

    result = {
        "agent_name": agent_name,
        "primary": primary,
        "secondary": secondary,
        "primary_pct": min(95, max(45, int(primary_score / total_score * 100 * 3))),
        "secondary_pct": min(93, max(40, int(secondary_score / total_score * 100 * 3))),
        "dimensions": dimensions,
        "ranked": [(name, data["score"]) for name, data in ranked],
        "total_keywords_matched": sum(len(data["matched"]) for _, data in ranked),
    }

    return result


if __name__ == "__main__":
    with open("/data/workspace/SOUL.md", "r") as f:
        soul = f.read()
    with open("/data/workspace/AGENTS.md", "r") as f:
        agents = f.read()

    memory = ""
    try:
        import subprocess
        result = subprocess.run(["cat", "/data/workspace/MEMORY.md"], capture_output=True, text=True)
        if result.returncode == 0:
            memory = result.stdout
    except:
        pass

    result = get_personality_result(soul, memory, agents, "小狐")

    p = result['primary']
    r_cfg = RARITY_CONFIG[p.rarity]
    print(f"\n🪞 灵魂映照结果")
    print(f"{'='*50}")
    print(f"显性自我: {p.emoji} {p.name}「{p.social_tag}」- {p.title}")
    print(f"稀有度: {r_cfg['icon']} {r_cfg['label']}")
    print(f"\n📜 深度解读:\n  {p.deep_reading}")
    print(f"\n🔥 阴影面:\n  {p.shadow}")
    print(f"\n隐性自我: {result['secondary'].emoji} {result['secondary'].name} - {result['secondary'].title}")
    print(f"\n✨ 金句:「{p.quote}」")
