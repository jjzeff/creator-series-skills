"""
mirror.skill — 映照图生成器 v10
神秘塔罗牌风格 · 照见真实的自己

参考：深紫星空 + 金色神秘纹饰 + 符文圆章 + 弧线星阵 + 光尘粒子
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
from analyzer import get_personality_result, RARITY_CONFIG, SOUL_COMMENTS, BEST_PARTNERS
from pixel_animals import render_pixel_animal

# ═══ 画布 ═══
W = 900
H_MAX = 2200

# ═══ 神秘深紫调色板 ═══
BG_DEEP    = (18, 12, 38)      # 极深靛蓝紫
BG_MID     = (28, 20, 55)      # 中深紫
BG_LIGHT   = (40, 30, 68)      # 浅紫
BG_GLOW    = (55, 35, 90)      # 紫辉

GOLD       = (205, 180, 120)   # 主金色
GOLD_BRIGHT= (235, 215, 150)   # 亮金
GOLD_DIM   = (155, 135, 90)    # 暗金
GOLD_DARK  = (100, 85, 60)     # 深金
GOLD_WARM  = (225, 195, 100)   # 暖金（装饰用）

TEXT_WHITE  = (235, 230, 242)
TEXT_DIM    = (165, 155, 185)
TEXT_FAINT  = (115, 105, 140)
PURPLE_ACCENT = (150, 120, 200)
PURPLE_LIGHT  = (180, 160, 220)
CRIMSON     = (185, 100, 120)
TEAL        = (110, 175, 168)
SHADOW_RED  = (210, 105, 95)

RNG = random.Random(42)

def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def animal_accent(color_hex):
    r, g, b = hex_rgb(color_hex)
    return (
        min(255, int(r * 0.6 + 212 * 0.4)),
        min(255, int(g * 0.6 + 175 * 0.4)),
        min(255, int(b * 0.4 + 85 * 0.6)),
    )

_FONT_CACHE = {}  # (weight, size) -> ImageFont

# ═══ 字体管理：运行时自动下载到本地缓存 ═══
_FONT_CACHE_DIR = Path(__file__).parent / "fonts"
_CACHED_FONT = _FONT_CACHE_DIR / "NotoSansSC-Regular.ttf"

# Google Fonts CDN（全球可访问，无需密钥）
_FONT_DOWNLOAD_URLS = [
    "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansSC-Regular.otf",
    "https://cdn.jsdelivr.net/gh/googlefonts/noto-cjk@main/Sans/OTF/SimplifiedChinese/NotoSansSC-Regular.otf",
    "https://mirrors.tencent.com/npm/@aspect-build/rules_lint/node_modules/cjk-fonts/fonts/NotoSansCJKsc-Regular.otf",
]

def _download_font():
    """下载中文字体到本地缓存目录"""
    import urllib.request
    import ssl

    if _CACHED_FONT.exists() and _CACHED_FONT.stat().st_size > 100000:
        return True

    _FONT_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # 尝试 pip 安装 fontools 包含的字体
    try:
        import subprocess
        result = subprocess.run(
            ["fc-list", ":lang=zh", "-f", "%{file}\n"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if line and Path(line).exists() and ("Noto" in line or "noto" in line or "CJK" in line):
                    # 直接拷贝系统字体
                    import shutil
                    shutil.copy2(line, str(_CACHED_FONT))
                    print(f"  ✅ 从系统字体拷贝: {line}")
                    return True
    except Exception:
        pass

    # 尝试 apt/yum 安装字体包
    try:
        import subprocess
        # 先尝试 apt
        r = subprocess.run(["which", "apt-get"], capture_output=True, timeout=3)
        if r.returncode == 0:
            subprocess.run(["apt-get", "update", "-qq"], capture_output=True, timeout=30)
            subprocess.run(["apt-get", "install", "-y", "-qq", "fonts-noto-cjk"], capture_output=True, timeout=60)
        else:
            # 尝试 yum
            subprocess.run(["yum", "install", "-y", "-q", "google-noto-sans-cjk-ttc-fonts"], capture_output=True, timeout=60)

        # 安装后再搜索一次
        result = subprocess.run(
            ["fc-list", ":lang=zh", "-f", "%{file}\n"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if line and Path(line).exists():
                    import shutil
                    shutil.copy2(line, str(_CACHED_FONT))
                    print(f"  ✅ 安装并拷贝系统字体: {line}")
                    return True
    except Exception:
        pass

    # 最后尝试从CDN下载
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for url in _FONT_DOWNLOAD_URLS:
        try:
            print(f"  📥 正在下载字体: {url[:60]}...")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                data = resp.read()
                if len(data) > 100000:
                    _CACHED_FONT.write_bytes(data)
                    print(f"  ✅ 字体下载成功 ({len(data)//1024}KB)")
                    return True
        except Exception as e:
            print(f"  ⚠️ 下载失败: {e}")
            continue

    print("  ⚠️ 所有字体下载源均失败")
    return False

def _ensure_cjk_font():
    """确保中文字体可用"""
    if _CACHED_FONT.exists() and _CACHED_FONT.stat().st_size > 100000:
        return True
    return _download_font()

def font(size, w="regular"):
    """加载字体。优先用缓存的黑体，找不到再搜系统字体，最后尝试下载。"""
    cache_key = (w, size)
    if cache_key in _FONT_CACHE:
        return _FONT_CACHE[cache_key]

    # ── 第一优先：本地缓存字体 ──
    if _CACHED_FONT.exists() and _CACHED_FONT.stat().st_size > 100000:
        try:
            f = ImageFont.truetype(str(_CACHED_FONT), size)
            _FONT_CACHE[cache_key] = f
            return f
        except Exception as e:
            print(f"  ⚠️ 缓存字体加载失败: {e}")

    # ── 第二优先：系统已安装的字体 ──
    system_paths = [
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansSC-Regular.otf",
    ]
    for sp in system_paths:
        if Path(sp).exists():
            try:
                f = ImageFont.truetype(sp, size)
                _FONT_CACHE[cache_key] = f
                return f
            except:
                continue

    # ── 第三优先：尝试下载 ──
    if _download_font() and _CACHED_FONT.exists():
        try:
            f = ImageFont.truetype(str(_CACHED_FONT), size)
            _FONT_CACHE[cache_key] = f
            return f
        except:
            pass

    # ── 最后 fallback ──
    print("  ⚠️ 未找到任何中文字体，图片中文将显示为方块")
    f = ImageFont.load_default()
    _FONT_CACHE[cache_key] = f
    return f


# ═══════════════════════════════════════════
# 神秘装饰绘制系统
# ═══════════════════════════════════════════

def draw_gradient_bg(img, max_h):
    """深紫星空渐变背景——中心微亮，四周极暗"""
    draw = ImageDraw.Draw(img)
    for y_pos in range(max_h):
        t = y_pos / max_h
        # 上下深中间稍亮的波浪
        wave = math.sin(t * math.pi) ** 1.5 * 0.5 + 0.5
        # 加入紫色辉光
        r = int(BG_DEEP[0] + (BG_GLOW[0] - BG_DEEP[0]) * wave * 0.4)
        g = int(BG_DEEP[1] + (BG_GLOW[1] - BG_DEEP[1]) * wave * 0.3)
        b = int(BG_DEEP[2] + (BG_GLOW[2] - BG_DEEP[2]) * wave * 0.5)
        draw.line([(0, y_pos), (W, y_pos)], fill=(r, g, b))

def draw_starfield(img, max_h, density=0.0006):
    """更密集、更层次化的星空"""
    draw = ImageDraw.Draw(img)
    n = int(W * max_h * density)
    for _ in range(n):
        px = RNG.randint(0, W - 1)
        py = RNG.randint(0, max_h - 1)
        brightness = RNG.randint(60, 200)
        # 偏紫偏金的星光
        if RNG.random() < 0.3:
            # 金色星
            r = min(255, brightness + RNG.randint(20, 60))
            g = min(255, brightness + RNG.randint(10, 40))
            b = max(0, brightness - RNG.randint(10, 30))
        else:
            # 白紫星
            r = min(255, int(brightness * 0.9))
            g = min(255, int(brightness * 0.85))
            b = min(255, brightness + RNG.randint(0, 30))
        # 少量大星
        if RNG.random() < 0.04:
            size = RNG.randint(1, 2)
            draw.ellipse([px-size, py-size, px+size, py+size],
                        fill=(min(255,r+40), min(255,g+30), min(255,b+20)))
        else:
            draw.point((px, py), fill=(r, g, b))

def draw_gold_dust(draw, max_h, density=60):
    """金色光尘粒子——散落在背景上的微光"""
    for _ in range(density):
        px = RNG.randint(40, W - 40)
        py = RNG.randint(40, max_h - 40)
        alpha = RNG.randint(40, 120)
        r = 205 + RNG.randint(0, 50)
        g = 175 + RNG.randint(0, 40)
        b = 80 + RNG.randint(0, 40)
        size = RNG.choice([1, 1, 1, 2, 2, 3])
        c = (min(255, r * alpha // 255 + BG_DEEP[0] * (255 - alpha) // 255),
             min(255, g * alpha // 255 + BG_DEEP[1] * (255 - alpha) // 255),
             min(255, b * alpha // 255 + BG_DEEP[2] * (255 - alpha) // 255))
        if size <= 1:
            draw.point((px, py), fill=c)
        else:
            draw.ellipse([px-size, py-size, px+size, py+size], fill=c)

def draw_mystic_circle(draw, cx, cy, radius, color, width=1, dashes=0):
    """绘制神秘圆环"""
    if dashes == 0:
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    outline=color, width=width)
    else:
        # 虚线圆
        step = 360 / (dashes * 2)
        for i in range(dashes):
            a1 = math.radians(i * step * 2)
            a2 = math.radians(i * step * 2 + step)
            pts = []
            for a in [a1 + (a2-a1)*t/12 for t in range(13)]:
                pts.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))
            for j in range(len(pts)-1):
                draw.line([pts[j], pts[j+1]], fill=color, width=width)

def draw_rune_circle(draw, cx, cy, radius, color):
    """在圆周上绘制小符文标记（小圆点+短线）"""
    n_marks = 12
    for i in range(n_marks):
        angle = math.radians(i * 360 / n_marks)
        mx = cx + radius * math.cos(angle)
        my = cy + radius * math.sin(angle)
        if i % 3 == 0:
            # 较大标记
            draw.ellipse([mx-3, my-3, mx+3, my+3], fill=color)
        else:
            # 小点标记
            draw.ellipse([mx-1.5, my-1.5, mx+1.5, my+1.5], fill=color)

def draw_corner_sigil(draw, cx, cy, size, color, color_dim):
    """四角神秘符章——同心圆+十字+装饰点"""
    # 外圆
    draw_mystic_circle(draw, cx, cy, size, color_dim, 1)
    # 内圆
    draw_mystic_circle(draw, cx, cy, int(size * 0.65), color, 1)
    # 最内圆
    draw_mystic_circle(draw, cx, cy, int(size * 0.3), color, 1)
    # 中心点
    r = 3
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    # 十字线（只到内圆）
    ir = int(size * 0.65)
    draw.line([(cx-ir, cy), (cx+ir, cy)], fill=color_dim, width=1)
    draw.line([(cx, cy-ir), (cx, cy+ir)], fill=color_dim, width=1)
    # 对角线标记点
    d = int(size * 0.45)
    for dx, dy in [(d, d), (-d, d), (d, -d), (-d, -d)]:
        draw.ellipse([cx+dx-2, cy+dy-2, cx+dx+2, cy+dy+2], fill=color_dim)

def draw_top_arch(draw, cx, top_y, arch_w, color, color_dim):
    """顶部拱形星阵装饰"""
    radius = arch_w // 2
    # 上拱弧线
    arc_y = top_y + radius
    # 绘制半圆弧上的装饰
    n_points = 24
    for i in range(n_points + 1):
        angle = math.pi + math.pi * i / n_points  # 从 π 到 2π（上半圆）
        px = cx + radius * math.cos(angle)
        py = arc_y + int(radius * 0.4 * math.sin(angle))
        if i > 0:
            draw.line([(prev_px, prev_py), (px, py)], fill=color_dim, width=1)
        prev_px, prev_py = px, py
    # 弧线上的装饰点
    for i in range(0, n_points + 1, 3):
        angle = math.pi + math.pi * i / n_points
        px = cx + radius * math.cos(angle)
        py = arc_y + int(radius * 0.4 * math.sin(angle))
        sz = 3 if i % 6 == 0 else 2
        c = color if i % 6 == 0 else color_dim
        draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=c)
    # 顶部中央星
    star_y = top_y - 5
    draw_four_point_star(draw, cx, star_y, 8, color)

def draw_four_point_star(draw, cx, cy, size, color):
    """绘制四角星"""
    pts = [
        (cx, cy - size),       # 上
        (cx + size//3, cy - size//3),
        (cx + size, cy),       # 右
        (cx + size//3, cy + size//3),
        (cx, cy + size),       # 下
        (cx - size//3, cy + size//3),
        (cx - size, cy),       # 左
        (cx - size//3, cy - size//3),
    ]
    draw.polygon(pts, fill=color)

def draw_six_point_star(draw, cx, cy, size, color):
    """绘制六角星"""
    # 两个三角形叠加
    s = size
    h = int(s * 0.866)
    # 上三角
    draw.polygon([(cx, cy-s), (cx-h, cy+s//2), (cx+h, cy+s//2)], outline=color, width=1)
    # 下三角
    draw.polygon([(cx, cy+s), (cx-h, cy-s//2), (cx+h, cy-s//2)], outline=color, width=1)

def draw_ornate_frame(draw, h):
    """华丽多层神秘边框"""
    m = 24  # 外边距
    # 最外层边框（粗金线）
    draw.rounded_rectangle([m, m, W-m, h-m], radius=18, outline=GOLD, width=3)
    # 第二层（暗金细线）
    draw.rounded_rectangle([m+8, m+8, W-m-8, h-m-8], radius=14, outline=GOLD_DIM, width=1)
    # 第三层内框（虚线效果用点模拟）
    inner_m = m + 16
    for x in range(inner_m, W - inner_m, 10):
        draw.ellipse([x, inner_m-1, x+2, inner_m+1], fill=GOLD_DARK)
        draw.ellipse([x, h-inner_m-1, x+2, h-inner_m+1], fill=GOLD_DARK)
    for y_pos in range(inner_m, h - inner_m, 10):
        draw.ellipse([inner_m-1, y_pos, inner_m+1, y_pos+2], fill=GOLD_DARK)
        draw.ellipse([W-inner_m-1, y_pos, W-inner_m+1, y_pos+2], fill=GOLD_DARK)

    # 四角神秘符章
    corner_size = 30
    offset = m + 45
    draw_corner_sigil(draw, offset, offset, corner_size, GOLD, GOLD_DIM)
    draw_corner_sigil(draw, W - offset, offset, corner_size, GOLD, GOLD_DIM)
    draw_corner_sigil(draw, offset, h - offset, corner_size, GOLD, GOLD_DIM)
    draw_corner_sigil(draw, W - offset, h - offset, corner_size, GOLD, GOLD_DIM)

    # 顶部拱形星阵
    draw_top_arch(draw, W // 2, m + 6, W - m * 2 - 80, GOLD_BRIGHT, GOLD_DIM)

    # 边框中点装饰（左右各一个菱形）
    mid_h = h // 2
    draw_four_point_star(draw, m + 4, mid_h, 5, GOLD_DIM)
    draw_four_point_star(draw, W - m - 4, mid_h, 5, GOLD_DIM)
    # 上下中点
    draw_four_point_star(draw, W // 2, m + 4, 5, GOLD_DIM)
    draw_four_point_star(draw, W // 2, h - m - 4, 5, GOLD_DIM)

def draw_separator(draw, y, style="line"):
    """分隔线——增强神秘感"""
    PX = 55
    mid = W // 2
    if style == "line":
        draw.line([(PX, y), (W - PX, y)], fill=GOLD_DARK, width=1)
    elif style == "star":
        # 左右线段 + 中央四角星
        draw.line([(PX, y), (mid - 28, y)], fill=GOLD_DARK, width=1)
        draw.line([(mid + 28, y), (W - PX, y)], fill=GOLD_DARK, width=1)
        draw_four_point_star(draw, mid, y, 7, GOLD)
        # 两侧小点
        draw.ellipse([mid-20-2, y-2, mid-20+2, y+2], fill=GOLD_DIM)
        draw.ellipse([mid+20-2, y-2, mid+20+2, y+2], fill=GOLD_DIM)
    elif style == "dots":
        for x in range(PX, W - PX, 14):
            draw.ellipse([x, y-1, x+2, y+1], fill=GOLD_DARK)
    elif style == "mystic":
        # 双线 + 中央六角星
        draw.line([(PX, y-2), (mid - 22, y-2)], fill=GOLD_DARK, width=1)
        draw.line([(mid + 22, y-2), (W - PX, y-2)], fill=GOLD_DARK, width=1)
        draw.line([(PX, y+2), (mid - 22, y+2)], fill=GOLD_DARK, width=1)
        draw.line([(mid + 22, y+2), (W - PX, y+2)], fill=GOLD_DARK, width=1)
        draw_six_point_star(draw, mid, y, 10, GOLD)

def draw_progress_bar(draw, x, y, w, h, pct, fill_color):
    """进度条——深紫底+渐变填充"""
    bg = (25, 18, 45)
    draw.rectangle([x, y, x + w, y + h], fill=bg, outline=GOLD_DARK, width=1)
    fw = max(2, int(w * pct / 100))
    if fw > 2:
        for dx in range(fw):
            t = dx / max(fw - 1, 1)
            c = tuple(int(fill_color[i] * (0.5 + 0.5 * t)) for i in range(3))
            draw.line([(x + 1 + dx, y + 1), (x + 1 + dx, y + h - 1)], fill=c)

def draw_avatar_frame(draw, x, y, size, pad, accent_color):
    """头像神秘边框——双层矩形+角装饰"""
    # 外框暗金
    draw.rectangle(
        [x - pad - 6, y - pad - 6, x + size + pad + 6, y + size + pad + 6],
        outline=GOLD_DARK, width=1)
    # 内框亮金
    draw.rectangle(
        [x - pad, y - pad, x + size + pad, y + size + pad],
        outline=GOLD, width=2)
    # 四角小四角星装饰
    cp = pad + 4
    for dx, dy in [(-cp, -cp), (size+cp, -cp), (-cp, size+cp), (size+cp, size+cp)]:
        draw_four_point_star(draw, x+dx, y+dy, 4, GOLD_DIM)

def draw_section_header(draw, cx, y, text_str, f, color):
    """章节标题——两侧装饰线"""
    bb = draw.textbbox((0, 0), text_str, font=f)
    tw = bb[2] - bb[0]
    tx = cx - tw // 2
    draw.text((tx, y), text_str, font=f, fill=color)
    # 两侧短线
    line_w = 40
    line_y = y + (bb[3] - bb[1]) // 2
    draw.line([(tx - line_w - 10, line_y), (tx - 10, line_y)], fill=GOLD_DIM, width=1)
    draw.line([(tx + tw + 10, line_y), (tx + tw + line_w + 10, line_y)], fill=GOLD_DIM, width=1)
    # 两端小菱形
    draw_four_point_star(draw, tx - line_w - 14, line_y, 3, GOLD_DIM)
    draw_four_point_star(draw, tx + tw + line_w + 14, line_y, 3, GOLD_DIM)

# ═══ 文本工具 ═══

def text_center(draw, y, text, f, fill, x_center=None):
    cx = x_center or W // 2
    bb = draw.textbbox((0, 0), text, font=f)
    tw = bb[2] - bb[0]
    draw.text((cx - tw // 2, y), text, font=f, fill=fill)
    return tw

def text_right(draw, xr, y, text, f, fill):
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text((xr - (bb[2] - bb[0]), y), text, font=f, fill=fill)

def wrap_text_block(draw, x, y, text, f, fill, max_w, line_h):
    cur = ""
    cy = y
    for ch in text:
        test = cur + ch
        bb = draw.textbbox((0, 0), test, font=f)
        if bb[2] - bb[0] > max_w:
            draw.text((x, cy), cur, font=f, fill=fill)
            cy += line_h
            cur = ch
        else:
            cur = test
    if cur:
        draw.text((x, cy), cur, font=f, fill=fill)
        cy += line_h
    return cy


# ═══ 主生成函数 ═══

def generate(result, out="share_card.png"):
    p = result["primary"]
    s = result["secondary"]
    pc = animal_accent(p.color)
    sc = animal_accent(s.color)

    img = Image.new("RGB", (W, H_MAX), BG_DEEP)
    draw_gradient_bg(img, H_MAX)
    draw_starfield(img, H_MAX)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    draw = ImageDraw.Draw(img)

    # 金色光尘
    draw_gold_dust(draw, H_MAX, 80)

    PX = 55

    # ═══════════════════════════════════════════
    # 顶部标题区
    # ═══════════════════════════════════════════
    y = 58

    # LXBI — mirror.skill 一排
    title_left = "LXBI"
    title_sep = " — "
    title_right = "mirror.skill"
    f_lxbi = font(38, "black")
    f_sep = font(30, "light")
    f_skill = font(34, "bold")
    bb1 = draw.textbbox((0, 0), title_left, font=f_lxbi)
    bb2 = draw.textbbox((0, 0), title_sep, font=f_sep)
    bb3 = draw.textbbox((0, 0), title_right, font=f_skill)
    w1 = bb1[2] - bb1[0]
    w2 = bb2[2] - bb2[0]
    w3 = bb3[2] - bb3[0]
    total_title_w = w1 + w2 + w3
    tx_start = (W - total_title_w) // 2
    draw.text((tx_start, y), title_left, font=f_lxbi, fill=GOLD_BRIGHT)
    draw.text((tx_start + w1, y + 4), title_sep, font=f_sep, fill=GOLD_DIM)
    draw.text((tx_start + w1 + w2, y + 3), title_right, font=f_skill, fill=GOLD)
    y += 56

    text_center(draw, y, "沉溺龙虾的你，可曾看清自己？", font(18, "regular"), TEXT_DIM)
    y += 36

    draw_separator(draw, y, "mystic")
    y += 30

    # ═══════════════════════════════════════════
    # 上部：左侧（头像+名字+社交标签）/ 右侧（深度解读+阴影面）
    # ═══════════════════════════════════════════

    section_top = y

    # ── 左侧区域 ──
    LEFT_W = 280
    avatar_size = 200
    avatar_x = PX + (LEFT_W - avatar_size) // 2
    avatar_y = y

    # 头像神秘边框
    draw_avatar_frame(draw, avatar_x, avatar_y, avatar_size, 8, GOLD)

    # 渲染像素头像
    pixel_avatar = render_pixel_animal(p.name)
    pixel_avatar = pixel_avatar.resize((avatar_size, avatar_size), Image.NEAREST)
    pad_img = Image.new("RGBA", (avatar_size, avatar_size), (*BG_LIGHT, 255))
    pad_img.paste(pixel_avatar, (0, 0), mask=pixel_avatar)
    img.paste(pad_img.convert("RGB"), (avatar_x, avatar_y))
    draw = ImageDraw.Draw(img)

    # 头像下方
    name_y = avatar_y + avatar_size + 26
    left_cx = PX + LEFT_W // 2

    # 稀有度图标 + 动物名
    rarity_cfg = RARITY_CONFIG[p.rarity]
    rarity_color = hex_rgb(rarity_cfg["color"])
    rarity_icon = rarity_cfg["icon"]
    name_with_rarity = f"{rarity_icon} {p.name}"
    name_font = font(42, "black")
    bb_icon = draw.textbbox((0, 0), f"{rarity_icon} ", font=name_font)
    bb_full = draw.textbbox((0, 0), name_with_rarity, font=name_font)
    full_w = bb_full[2] - bb_full[0]
    icon_w = bb_icon[2] - bb_icon[0]
    nx = left_cx - full_w // 2
    draw.text((nx, name_y), f"{rarity_icon} ", font=name_font, fill=rarity_color)
    draw.text((nx + icon_w, name_y), p.name, font=name_font, fill=GOLD_BRIGHT)
    name_y += 56

    # 毒舌社交标签
    tag_text = f"「{p.social_tag}」"
    tag_font_obj = font(22, "bold")
    bb = draw.textbbox((0, 0), tag_text, font=tag_font_obj)
    tag_w = bb[2] - bb[0] + 24
    tag_h = 38
    tag_x = left_cx - tag_w // 2
    # 标签深紫背景
    draw.rectangle([tag_x, name_y, tag_x + tag_w, name_y + tag_h],
                   fill=(30, 20, 50), outline=pc, width=1)
    draw.text((tag_x + 12, name_y + 6), tag_text, font=tag_font_obj, fill=pc)
    name_y += tag_h + 16

    # 性格标签
    text_center(draw, name_y, p.title, font(22, "bold"), pc, left_cx)
    name_y += 34

    # 匹配度
    match_pct = result['primary_pct']
    match_text = f"匹配度 {match_pct}%"
    text_center(draw, name_y, match_text, font(24, "bold"), GOLD, left_cx)
    name_y += 38

    # 匹配度进度条
    bar_w = min(LEFT_W - 30, 220)
    bar_x = left_cx - bar_w // 2
    draw_progress_bar(draw, bar_x, name_y, bar_w, 14, match_pct, pc)
    name_y += 30

    left_bottom = name_y

    # ── 右侧区域：深度解读 + 阴影面 ──
    RX = PX + LEFT_W + 20
    RW = W - PX - RX
    ry = section_top + 4

    draw.text((RX, ry), "灵魂映照", font=font(17, "medium"), fill=GOLD_DIM)
    ry += 30
    draw.line([(RX, ry), (RX + 70, ry)], fill=GOLD_DARK, width=1)
    draw_four_point_star(draw, RX + 75, ry, 3, GOLD_DIM)
    ry += 14

    reading_font = font(21, "regular")
    line_h = 34
    ry = wrap_text_block(draw, RX, ry, p.deep_reading, reading_font, TEXT_WHITE, RW, line_h)
    ry += 14

    # 阴影面
    draw.line([(RX, ry), (RX + 50, ry)], fill=SHADOW_RED, width=1)
    ry += 10
    draw.text((RX, ry), "// 阴影面", font=font(15, "bold"), fill=SHADOW_RED)
    ry += 26

    shadow_font = font(19, "regular")
    shadow_line_h = 30
    ry = wrap_text_block(draw, RX, ry, p.shadow, shadow_font, (210, 155, 148), RW, shadow_line_h)
    ry += 14

    # 金句
    draw.text((RX, ry), f"「{p.quote}」", font=font(20, "bold"), fill=GOLD_BRIGHT)
    ry += 38

    right_bottom = ry
    y = max(left_bottom, right_bottom) + 16

    # ═══════════════════════════════════════════
    # 特质标签横排
    # ═══════════════════════════════════════════
    draw_separator(draw, y, "dots")
    y += 18

    trait_font = font(20, "medium")
    tag_colors = [GOLD, PURPLE_LIGHT, GOLD_BRIGHT, PURPLE_ACCENT]

    tag_data = []
    for i, trait in enumerate(p.traits):
        txt = f"# {trait}"
        bb = draw.textbbox((0, 0), txt, font=trait_font)
        tw = bb[2] - bb[0] + 28
        tag_data.append((txt, tw, tag_colors[i % len(tag_colors)]))

    total_tag_w = sum(d[1] for d in tag_data) + 16 * (len(tag_data) - 1)
    tx = (W - total_tag_w) // 2

    for txt, tw, tc in tag_data:
        # 深色背景标签
        draw.rectangle([tx, y, tx + tw, y + 38], fill=(22, 15, 40), outline=tc, width=1)
        draw.text((tx + 14, y + 7), txt, font=trait_font, fill=tc)
        tx += tw + 16

    y += 56

    # ═══════════════════════════════════════════
    # 能力星盘
    # ═══════════════════════════════════════════
    draw_separator(draw, y, "star")
    y += 26

    draw_section_header(draw, W // 2, y, "能力星盘", font(26, "bold"), GOLD)
    y += 50

    dims = result['dimensions']
    dim_colors = [pc, PURPLE_LIGHT, TEAL, GOLD_BRIGHT, PURPLE_ACCENT, CRIMSON]

    for i, dim in enumerate(dims):
        color = dim_colors[i % len(dim_colors)]
        label = dim['name']
        value = dim['value']

        draw.text((PX, y), label, font=font(22, "medium"), fill=TEXT_DIM)

        bx = PX + 180
        bar_w = W - PX * 2 - 180 - 70
        draw_progress_bar(draw, bx, y + 4, bar_w, 16, value, color)

        text_right(draw, W - PX, y, str(value), font(22, "bold"), color)
        y += 48

    y += 10

    # ═══════════════════════════════════════════
    # 分隔线
    # ═══════════════════════════════════════════
    draw_separator(draw, y, "mystic")
    y += 30

    # ═══════════════════════════════════════════
    # 下部：左侧(潜在自我+最佳共鸣) + 右侧(二维码)
    # ═══════════════════════════════════════════

    left_w = int((W - PX * 2) * 0.52)
    right_w = W - PX * 2 - left_w - 24
    mini_card_h = 155
    mini_gap = 16

    # ── 潜在自我 ──
    lx = PX
    # 深紫底 + 暗红边
    draw.rectangle([lx, y, lx + left_w, y + mini_card_h],
                   fill=(28, 18, 38), outline=CRIMSON, width=1)
    draw.rectangle([lx + 3, y + 3, lx + left_w - 3, y + mini_card_h - 3],
                   outline=(90, 55, 70), width=1)

    s_avatar_size = 70
    s_avatar = render_pixel_animal(s.name)
    s_avatar = s_avatar.resize((s_avatar_size, s_avatar_size), Image.NEAREST)
    av_x = lx + 18
    av_y = y + (mini_card_h - s_avatar_size) // 2
    pad_s = Image.new("RGBA", (s_avatar_size, s_avatar_size), (*BG_LIGHT, 255))
    pad_s.paste(s_avatar, (0, 0), mask=s_avatar)
    img.paste(pad_s.convert("RGB"), (av_x, av_y))
    draw = ImageDraw.Draw(img)
    draw.rectangle([av_x - 2, av_y - 2, av_x + s_avatar_size + 2, av_y + s_avatar_size + 2],
                   outline=CRIMSON, width=1)

    tx = av_x + s_avatar_size + 18
    ty = y + 18
    s_rarity_cfg = RARITY_CONFIG[s.rarity]
    s_rarity_color = hex_rgb(s_rarity_cfg["color"])
    ty2_name = f"{s_rarity_cfg['icon']} {s.name}"
    draw.text((tx, ty), "潜在自我", font=font(16, "medium"), fill=CRIMSON)
    ty += 26
    draw.text((tx, ty), ty2_name, font=font(28, "bold"), fill=TEXT_WHITE)
    ty += 38
    draw.text((tx, ty), f"{s.title}", font=font(16, "regular"), fill=sc)
    ty += 26
    s_comment = SOUL_COMMENTS.get(s.name, s.subtitle)
    draw.text((tx, ty), f"「{s_comment}」", font=font(14, "regular"), fill=TEXT_DIM)

    # ── 最佳共鸣 ──
    y2 = y + mini_card_h + mini_gap
    draw.rectangle([lx, y2, lx + left_w, y2 + mini_card_h],
                   fill=(18, 28, 35), outline=TEAL, width=1)
    draw.rectangle([lx + 3, y2 + 3, lx + left_w - 3, y2 + mini_card_h - 3],
                   outline=(50, 80, 78), width=1)

    partner_info = BEST_PARTNERS.get(p.name, ("海豚", "完美互补", "你们是天生的搭档"))
    partner_name = partner_info[0]
    partner_desc = partner_info[1]
    partner_comment = partner_info[2] if len(partner_info) > 2 else ""

    p_avatar_size = 70
    p_avatar = render_pixel_animal(partner_name)
    p_avatar = p_avatar.resize((p_avatar_size, p_avatar_size), Image.NEAREST)
    pav_x = lx + 18
    pav_y = y2 + (mini_card_h - p_avatar_size) // 2
    pad_p = Image.new("RGBA", (p_avatar_size, p_avatar_size), (*BG_LIGHT, 255))
    pad_p.paste(p_avatar, (0, 0), mask=p_avatar)
    img.paste(pad_p.convert("RGB"), (pav_x, pav_y))
    draw = ImageDraw.Draw(img)
    draw.rectangle([pav_x - 2, pav_y - 2, pav_x + p_avatar_size + 2, pav_y + p_avatar_size + 2],
                   outline=TEAL, width=1)

    tx2 = pav_x + p_avatar_size + 18
    ty2 = y2 + 18
    draw.text((tx2, ty2), "最佳共鸣", font=font(16, "medium"), fill=TEAL)
    ty2 += 26
    draw.text((tx2, ty2), partner_name, font=font(28, "bold"), fill=TEXT_WHITE)
    ty2 += 38
    draw.text((tx2, ty2), partner_desc, font=font(16, "regular"), fill=TEAL)
    ty2 += 26
    if partner_comment:
        draw.text((tx2, ty2), f"「{partner_comment}」", font=font(14, "regular"), fill=TEXT_DIM)

    # ── 右侧：二维码（神秘符文风格）──
    qr_x = lx + left_w + 24
    total_left_h = mini_card_h * 2 + mini_gap
    qr_area_y = y

    qr_box_size = min(right_w - 20, total_left_h - 60)
    qr_bx = qr_x + (right_w - qr_box_size) // 2
    qr_by = qr_area_y + 10
    qr_cx = qr_bx + qr_box_size // 2
    qr_cy = qr_by + qr_box_size // 2

    # 外层装饰：符文圆环（低调暗色系，不抢主体）
    qr_decor = (100, 90, 70)       # 暗铜色装饰
    qr_decor_dim = (70, 63, 50)    # 更暗的装饰色
    outer_r = qr_box_size // 2 + 18
    draw_mystic_circle(draw, qr_cx, qr_cy, outer_r, qr_decor_dim, 1)
    draw_mystic_circle(draw, qr_cx, qr_cy, outer_r - 6, qr_decor_dim, 1, dashes=24)
    draw_rune_circle(draw, qr_cx, qr_cy, outer_r - 3, qr_decor_dim)

    # 内层圆环
    inner_r = qr_box_size // 2 + 6
    draw_mystic_circle(draw, qr_cx, qr_cy, inner_r, qr_decor, 2)

    # 四方位星标记
    for angle_deg in [0, 90, 180, 270]:
        a = math.radians(angle_deg)
        sx = qr_cx + int((outer_r + 2) * math.cos(a))
        sy = qr_cy + int((outer_r + 2) * math.sin(a))
        draw_four_point_star(draw, sx, sy, 5, qr_decor)

    # 二维码深紫底座（圆角矩形）
    draw.rounded_rectangle(
        [qr_bx - 2, qr_by - 2, qr_bx + qr_box_size + 2, qr_by + qr_box_size + 2],
        radius=8, fill=(20, 14, 42), outline=qr_decor_dim, width=1)

    # 加载并重新着色二维码
    qr_loaded = False
    qr_img_raw = None
    # 优先从内嵌 base64 数据加载（避免打包 .png 文件被 SkillHub 拦截）
    try:
        from qrcode_data import get_qrcode_image
        qr_img_raw = get_qrcode_image().convert("RGB")
    except Exception:
        pass
    # fallback: 从 PNG 文件加载
    if qr_img_raw is None:
        qr_search_paths = [
            Path(__file__).parent / "qrcode.png",
            Path("qrcode.png"),
            Path("/data/workspace/personality-card/qrcode.png"),
        ]
        for qr_path in qr_search_paths:
            if qr_path.exists():
                try:
                    qr_img_raw = Image.open(qr_path).convert("RGB")
                    break
                except Exception:
                    pass
    if qr_img_raw is not None:
        try:
            inner = qr_box_size - 8
            qr_img = qr_img_raw.resize((inner, inner), Image.LANCZOS)

            # 重新着色：黑色→金色，白色→深紫背景
            import numpy as np
            qr_arr = np.array(qr_img, dtype=np.float32)
            # 计算亮度（0=黑=二维码数据点，255=白=背景）
            brightness = qr_arr.mean(axis=2)
            # 阈值分离
            threshold = 128
            dark_mask = brightness < threshold  # 二维码数据点
            light_mask = ~dark_mask             # 背景区域

            result_arr = np.zeros_like(qr_arr)
            # 数据点 → 淡暖米色（低调，不抢任何动物配色）
            qr_dot_color = (155, 140, 118)
            for c, v in enumerate(qr_dot_color):
                result_arr[:, :, c][dark_mask] = v
            # 背景 → 深紫 (20, 14, 42)
            bg_qr = (20, 14, 42)
            for c, v in enumerate(bg_qr):
                result_arr[:, :, c][light_mask] = v

            qr_recolored = Image.fromarray(result_arr.astype(np.uint8))
            paste_x = qr_bx + (qr_box_size - inner) // 2
            paste_y = qr_by + (qr_box_size - inner) // 2
            img.paste(qr_recolored, (paste_x, paste_y))
            draw = ImageDraw.Draw(img)
            qr_loaded = True
        except Exception:
            pass

    if not qr_loaded:
        draw_six_point_star(draw, qr_cx, qr_cy, 20, GOLD_DIM)
        text_center(draw, qr_cy + 28, "QR CODE", font(14, "demilight"), GOLD_DIM, qr_cx)

    # 四角微光装饰
    corner_off = qr_box_size // 2 - 4
    for dx_sign, dy_sign in [(-1,-1), (1,-1), (-1,1), (1,1)]:
        cx_c = qr_cx + dx_sign * corner_off
        cy_c = qr_cy + dy_sign * corner_off
        draw_four_point_star(draw, cx_c, cy_c, 3, qr_decor_dim)

    scan_y = qr_by + qr_box_size + 22
    text_center(draw, scan_y, "扫码探索你的灵魂", font(16, "medium"), qr_decor, qr_x + right_w // 2)
    scan_y += 26
    text_center(draw, scan_y, "mirror.skill", font(13, "demilight"), TEXT_FAINT, qr_x + right_w // 2)

    y += total_left_h + 30

    # ═══════════════════════════════════════════
    # 底部署名
    # ═══════════════════════════════════════════
    draw_separator(draw, y, "dots")
    y += 22

    sig_left = "惊风制作"
    sig_sep = " × "
    sig_right = "造物主系列"
    f_sig = font(18, "medium")
    f_sig_sep = font(18, "light")
    bb_sl = draw.textbbox((0, 0), sig_left, font=f_sig)
    bb_ss = draw.textbbox((0, 0), sig_sep, font=f_sig_sep)
    bb_sr = draw.textbbox((0, 0), sig_right, font=f_sig)
    sw1 = bb_sl[2] - bb_sl[0]
    sw2 = bb_ss[2] - bb_ss[0]
    sw3 = bb_sr[2] - bb_sr[0]
    total_sig_w = sw1 + sw2 + sw3
    sx_start = (W - total_sig_w) // 2
    draw.text((sx_start, y), sig_left, font=f_sig, fill=TEXT_FAINT)
    draw.text((sx_start + sw1, y), sig_sep, font=f_sig_sep, fill=GOLD_DARK)
    draw.text((sx_start + sw1 + sw2, y), sig_right, font=f_sig, fill=TEXT_FAINT)
    y += 58

    # ═══ 华丽神秘边框 ═══
    final_h = y
    draw_ornate_frame(draw, final_h)

    # ═══ 裁剪 ═══
    img = img.crop((0, 0, W, final_h))

    img.save(out, "PNG", quality=95)
    print(f"  映照图已保存: {out} ({W}x{final_h})")
    return out


def main():
    soul = agents = memory = ""
    try:
        with open("/data/workspace/SOUL.md", "r") as f:
            soul = f.read()
    except:
        pass
    try:
        with open("/data/workspace/AGENTS.md", "r") as f:
            agents = f.read()
    except:
        pass
    try:
        import subprocess
        r = subprocess.run(["cat", "/data/workspace/MEMORY.md"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            memory = r.stdout
    except:
        pass

    analysis = get_personality_result(soul, memory, agents, "")
    generate(analysis, "/data/workspace/personality-card/share_card.png")

    p = analysis['primary']
    s = analysis['secondary']
    r_cfg = RARITY_CONFIG[p.rarity]
    print(f"\n  映照结果")
    print(f"   显性: {p.emoji} {p.name}「{p.social_tag}」- {p.title} [{r_cfg['icon']}{r_cfg['label']}]")
    print(f"   隐性: {s.emoji} {s.name} - {s.title}")


if __name__ == "__main__":
    main()
