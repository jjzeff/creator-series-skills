#!/usr/bin/env python3
"""
🪞 LXBI — mirror.skill 命令行入口

用法：
  python3 run.py --name "用户名"                # 自动检测环境，能生图就生图
  python3 run.py --name "用户名" --text-only     # 强制只输出文字
  python3 run.py --name "用户名" --image          # 强制生成图片（环境不满足会报错）
  python3 run.py --check-env                      # 仅检测图片生成环境
  python3 run.py --soul xxx.md --memory yyy.md --agents zzz.md
"""

import argparse
import sys
from pathlib import Path

# 确保能导入同目录模块
sys.path.insert(0, str(Path(__file__).parent))

from analyzer import get_personality_result, RARITY_CONFIG, SOUL_COMMENTS, BEST_PARTNERS


def check_image_env() -> tuple:
    """
    检测当前环境是否支持图片生成。
    返回 (can_generate: bool, reason: str)
    
    需要满足：
    1. PIL/Pillow 可导入
    2. numpy 可导入
    3. 自带中文字体文件存在
    """
    issues = []
    
    # 检查 Pillow
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        issues.append("缺少 Pillow 库（pip install Pillow）")
    
    # 检查 numpy
    try:
        import numpy as np
    except ImportError:
        issues.append("缺少 numpy 库（pip install numpy）")
    
    # 检查自带字体
    font_path = Path(__file__).parent / "fonts" / "NotoSansSC-Regular.otf"
    if not font_path.exists():
        issues.append(f"缺少中文字体文件: {font_path}")
    
    # 检查 requests（图片上传用）
    try:
        import requests
    except ImportError:
        issues.append("缺少 requests 库（pip install requests），图片上传功能不可用")
    
    if issues:
        return False, "；".join(issues)
    return True, "图片生成环境就绪"


def format_text_report(result: dict, name: str = "你") -> str:
    """
    生成精排文字版映照报告
    适用于企微等纯文字通道，保留仪式感和传播力
    """
    p = result['primary']
    s = result['secondary']
    r_cfg = RARITY_CONFIG[p.rarity]
    s_cfg = RARITY_CONFIG[s.rarity]

    # 最佳共鸣
    partner_info = BEST_PARTNERS.get(p.name, ("海豚", "完美互补", "你们是天生的搭档"))
    partner_name = partner_info[0]
    partner_comment = partner_info[2] if len(partner_info) > 2 else ""

    # 潜在自我短评
    soul_comment = SOUL_COMMENTS.get(s.name, s.title)

    # 匹配度进度条
    pct = result['primary_pct']
    filled = "█" * (pct // 5)
    empty = "░" * (20 - pct // 5)

    lines = []
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("🪞 LXBI — mirror.skill")
    lines.append("沉溺龙虾的你，可曾看清自己？")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")

    # ── 显性自我 ──
    lines.append(f"{r_cfg['icon']} {p.emoji} {p.name} · {p.title}")
    lines.append(f"「{p.social_tag}」")
    lines.append(f"匹配度 {filled}{empty} {pct}%")
    lines.append("")

    # ── 灵魂映照 ──
    lines.append("📜 灵魂映照")
    lines.append(p.deep_reading)
    lines.append("")

    # ── 阴影面 ──
    lines.append("🔥 阴影面")
    lines.append(p.shadow)
    lines.append("")

    # ── 核心特质 ──
    lines.append("✧ " + " · ".join(p.traits))
    lines.append("")

    # ── 能力星盘 ──
    lines.append("─── 能力星盘 ───")
    for d in result['dimensions']:
        bar_len = d['value'] // 5
        bar = "▓" * bar_len + "░" * (20 - bar_len)
        lines.append(f"  {d['emoji']} {d['name']:8s} {bar} {d['value']}")
    lines.append("")

    # ── 潜在自我 ──
    lines.append(f"🌗 潜在自我: {s_cfg['icon']} {s.emoji} {s.name} · {s.title}")
    lines.append(f"   {soul_comment}")
    lines.append("")

    # ── 最佳共鸣 ──
    lines.append(f"🤝 最佳共鸣: {partner_name}")
    if partner_comment:
        lines.append(f"   {partner_comment}")
    lines.append("")

    # ── 神谕金句 ──
    lines.append(f"  ✨「{p.quote}」")
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("惊风制作 × 造物主系列")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="🪞 LXBI — mirror.skill")
    parser.add_argument("--name", default="用户", help="Agent/用户名称")
    parser.add_argument("--soul", default=None, help="SOUL.md 文件路径")
    parser.add_argument("--memory", default=None, help="MEMORY.md 文件路径")
    parser.add_argument("--agents", default=None, help="AGENTS.md 文件路径")
    parser.add_argument("--image", action="store_true", help="强制生成映照图")
    parser.add_argument("--text-only", action="store_true", help="强制只输出文字版")
    parser.add_argument("--output", default=None, help="映照图输出路径")
    parser.add_argument("--check-env", action="store_true", help="仅检测图片生成环境并退出")
    args = parser.parse_args()

    # ═══ 仅检测环境 ═══
    if args.check_env:
        can, reason = check_image_env()
        if can:
            print(f"IMG_ENV=YES")
            print(f"  ✅ {reason}")
        else:
            print(f"IMG_ENV=NO")
            print(f"  ⚠️ {reason}")
        sys.exit(0 if can else 1)

    # ═══ 自动检测图片环境 ═══
    if args.text_only:
        generate_image = False
    elif args.image:
        generate_image = True
    else:
        # 默认行为：自动检测
        can, reason = check_image_env()
        generate_image = can
        if not can:
            print(f"  💡 图片环境检测: {reason}")
            print(f"  💡 将输出文字版报告\n")

    # 默认路径
    ws = Path("/data/workspace")
    soul_path = Path(args.soul) if args.soul else ws / "SOUL.md"
    memory_path = Path(args.memory) if args.memory else ws / "MEMORY.md"
    agents_path = Path(args.agents) if args.agents else ws / "AGENTS.md"
    output_path = args.output or str(Path(__file__).parent / "share_card.png")

    # 读取文件
    soul = memory = agents = ""
    required_files = [(soul_path, "SOUL.md"), (memory_path, "MEMORY.md")]
    optional_files = [(agents_path, "AGENTS.md")]

    for fp, name in required_files:
        try:
            content = fp.read_text(encoding="utf-8")
            if "SOUL" in name: soul = content
            elif "MEMORY" in name: memory = content
            print(f"  ✅ 已读取 {name} ({len(content)} 字符)")
        except FileNotFoundError:
            print(f"  ⚠️ {name} 不存在: {fp}")
        except Exception as e:
            print(f"  ❌ 读取 {name} 失败: {e}")

    for fp, name in optional_files:
        try:
            content = fp.read_text(encoding="utf-8")
            agents = content
            print(f"  ✅ 已读取 {name} ({len(content)} 字符)")
        except FileNotFoundError:
            print(f"  💡 {name} 不存在（可选，跳过）")
        except Exception as e:
            print(f"  ❌ 读取 {name} 失败: {e}")

    if not (soul or memory):
        print("\n❌ SOUL.md 和 MEMORY.md 至少需要一个，无法映照。")
        sys.exit(1)

    # 分析
    print(f"\n🔍 正在映照 {args.name} 的灵魂...")
    result = get_personality_result(soul, memory, agents, args.name)

    # ═══ 输出文字版报告（始终输出） ═══
    report = format_text_report(result, args.name)
    print("")
    print(report)

    # ═══ 图片生成 ═══
    if generate_image:
        print(f"\n🎨 正在生成映照图...")
        try:
            from card_generator import generate
            from image_uploader import upload_image
            generate(result, output_path)
            print(f"  📱 映照图已保存: {output_path}")

            # 自动上传到图床
            print(f"\n📤 正在上传映照图...")
            img_url = upload_image(output_path)
            if img_url:
                print(f"\n🔗 映照图在线链接（可直接分享）:")
                print(f"   {img_url}")
                print(f"\n   💡 复制链接即可在浏览器/微信中打开查看")
            else:
                print(f"\n⚠️ 图床上传失败，图片已保存在本地: {output_path}")
                print(f"   请使用 display_download_links 工具提供下载链接")
            
            # 本地生成提示
            print(f"\n─── 📌 关于映照图 ───")
            print(f"  🏠 推荐方式：本地生成（图片已保存在当前环境）")
            print(f"     → 使用 display_download_links 工具直接下载到本地")
            print(f"  🌐 便捷方式：通过上方在线链接直接查看/分享")
            print(f"     → 适合快速预览或转发给朋友")
        except Exception as e:
            print(f"\n❌ 图片生成失败: {e}")
            print(f"   已输出文字版报告，可正常使用")
    else:
        print(f"\n📷 IMAGE_HINT: 当前环境不支持图片生成。如需生成塔罗牌映照图，可回复「生成映照图」")


if __name__ == "__main__":
    main()
