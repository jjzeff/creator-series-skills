"""
🦞 像素风动物头像生成器 v2
参考：每个动物用自然真实配色，大色块高辨识度
128×128 画布，像素块清晰可见
"""

from PIL import Image, ImageDraw, ImageFont

_ = None  # 透明


def _draw_animal(size, draw_fn):
    """通用绘制入口"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_fn(draw, size)
    return img


# ═══════════════════════════════════════════
#  12 常规 + 2 金色传说
# ═══════════════════════════════════════════

def draw_squirrel(draw, s):
    """松鼠 - 知识囤积者：棕色系，大耳朵，蓬松尾巴"""
    body = (160, 130, 100)
    light = (195, 165, 130)
    dark = (120, 95, 70)
    belly = (210, 190, 160)
    ear_in = (210, 180, 150)
    eye = (30, 30, 30)
    nose = (90, 60, 40)
    # 左耳
    draw.rectangle([20, 8, 40, 28], fill=body)
    draw.rectangle([24, 12, 36, 24], fill=ear_in)
    # 右耳
    draw.rectangle([88, 8, 108, 28], fill=body)
    draw.rectangle([92, 12, 104, 24], fill=ear_in)
    # 头
    draw.rectangle([24, 24, 104, 76], fill=body)
    draw.rectangle([32, 32, 96, 72], fill=light)
    # 眼睛
    draw.rectangle([36, 40, 52, 52], fill=(255, 255, 255))
    draw.rectangle([40, 44, 52, 52], fill=eye)
    draw.rectangle([76, 40, 92, 52], fill=(255, 255, 255))
    draw.rectangle([80, 44, 92, 52], fill=eye)
    # 鼻子
    draw.rectangle([56, 56, 72, 64], fill=nose)
    # 嘴
    draw.rectangle([52, 64, 76, 68], fill=belly)
    # 身体
    draw.rectangle([28, 72, 100, 108], fill=body)
    draw.rectangle([40, 76, 88, 104], fill=belly)
    # 尾巴（右侧蓬松大尾巴）
    draw.rectangle([96, 48, 120, 64], fill=dark)
    draw.rectangle([108, 36, 124, 56], fill=body)
    draw.rectangle([112, 28, 124, 44], fill=light)
    # 脚
    draw.rectangle([32, 104, 52, 116], fill=dark)
    draw.rectangle([76, 104, 96, 116], fill=dark)


def draw_golden_monkey(draw, s):
    """金丝猴 - 灵动策略家：金色毛发+蓝脸"""
    gold = (230, 190, 80)
    gold_l = (245, 215, 120)
    gold_d = (180, 140, 50)
    face = (140, 170, 210)
    face_l = (170, 195, 225)
    eye = (30, 25, 20)
    nose = (100, 130, 170)
    mouth = (180, 120, 100)
    # 头顶毛发
    draw.rectangle([28, 4, 100, 24], fill=gold)
    draw.rectangle([36, 0, 92, 12], fill=gold_l)
    # 头/脸
    draw.rectangle([24, 20, 104, 76], fill=gold)
    draw.rectangle([32, 28, 96, 72], fill=face)
    # 眼睛
    draw.rectangle([36, 36, 52, 48], fill=(255, 255, 255))
    draw.rectangle([40, 40, 52, 48], fill=eye)
    draw.rectangle([76, 36, 92, 48], fill=(255, 255, 255))
    draw.rectangle([80, 40, 92, 48], fill=eye)
    # 鼻子（金丝猴的翘鼻）
    draw.rectangle([56, 48, 72, 56], fill=nose)
    draw.rectangle([60, 44, 68, 52], fill=face_l)
    # 嘴
    draw.rectangle([52, 60, 76, 66], fill=mouth)
    # 身体
    draw.rectangle([28, 72, 100, 112], fill=gold_d)
    draw.rectangle([40, 76, 88, 108], fill=gold)
    # 脚
    draw.rectangle([32, 108, 52, 120], fill=gold_d)
    draw.rectangle([76, 108, 96, 120], fill=gold_d)


def draw_snow_leopard(draw, s):
    """雪豹 - 冷静执行者：银灰+深色斑点"""
    fur = (185, 190, 200)
    light = (210, 215, 225)
    dark = (120, 125, 135)
    spot = (80, 85, 95)
    eye = (80, 160, 130)
    nose = (140, 110, 120)
    ear_in = (170, 150, 160)
    # 左耳
    draw.rectangle([20, 8, 40, 28], fill=dark)
    draw.rectangle([24, 12, 36, 24], fill=ear_in)
    # 右耳
    draw.rectangle([88, 8, 108, 28], fill=dark)
    draw.rectangle([92, 12, 104, 24], fill=ear_in)
    # 头
    draw.rectangle([24, 24, 104, 76], fill=fur)
    draw.rectangle([32, 32, 96, 72], fill=light)
    # 眼睛（翠绿色）
    draw.rectangle([36, 38, 52, 50], fill=(200, 220, 210))
    draw.rectangle([40, 42, 52, 50], fill=eye)
    draw.rectangle([76, 38, 92, 50], fill=(200, 220, 210))
    draw.rectangle([80, 42, 92, 50], fill=eye)
    # 鼻子
    draw.rectangle([56, 54, 72, 62], fill=nose)
    # 嘴
    draw.rectangle([52, 62, 76, 66], fill=light)
    # 斑点
    draw.rectangle([28, 32, 36, 40], fill=spot)
    draw.rectangle([92, 36, 100, 44], fill=spot)
    draw.rectangle([44, 64, 52, 72], fill=spot)
    draw.rectangle([80, 64, 88, 72], fill=spot)
    # 身体
    draw.rectangle([28, 72, 100, 108], fill=fur)
    draw.rectangle([40, 80, 88, 104], fill=light)
    # 身体斑点
    draw.rectangle([32, 80, 40, 88], fill=spot)
    draw.rectangle([52, 92, 60, 100], fill=spot)
    draw.rectangle([84, 84, 92, 92], fill=spot)
    # 脚
    draw.rectangle([32, 104, 52, 116], fill=dark)
    draw.rectangle([76, 104, 96, 116], fill=dark)


def draw_bee(draw, s):
    """蜜蜂 - 极致工匠：黄黑条纹+翅膀"""
    yellow = (240, 200, 60)
    black = (50, 40, 30)
    wing = (200, 220, 245, 160)
    eye = (30, 30, 30)
    # 触角
    draw.rectangle([44, 4, 48, 20], fill=black)
    draw.rectangle([40, 0, 48, 8], fill=black)
    draw.rectangle([80, 4, 84, 20], fill=black)
    draw.rectangle([80, 0, 88, 8], fill=black)
    # 头
    draw.rectangle([32, 16, 96, 56], fill=yellow)
    # 眼睛（大圆眼）
    draw.rectangle([36, 24, 56, 44], fill=(255, 255, 255))
    draw.rectangle([44, 28, 56, 44], fill=eye)
    draw.rectangle([72, 24, 92, 44], fill=(255, 255, 255))
    draw.rectangle([76, 28, 88, 44], fill=eye)
    # 嘴
    draw.rectangle([52, 46, 76, 52], fill=(200, 160, 40))
    # 翅膀
    draw.rectangle([4, 52, 32, 76], fill=(200, 220, 245))
    draw.rectangle([8, 56, 28, 72], fill=(220, 235, 250))
    draw.rectangle([96, 52, 124, 76], fill=(200, 220, 245))
    draw.rectangle([100, 56, 120, 72], fill=(220, 235, 250))
    # 身体（黄黑条纹）
    draw.rectangle([32, 56, 96, 68], fill=yellow)
    draw.rectangle([32, 68, 96, 80], fill=black)
    draw.rectangle([32, 80, 96, 92], fill=yellow)
    draw.rectangle([32, 92, 96, 104], fill=black)
    draw.rectangle([32, 104, 96, 112], fill=yellow)
    # 尾针
    draw.rectangle([56, 112, 72, 124], fill=(60, 50, 40))


def draw_eagle(draw, s):
    """鹰 - 全局掌控者：深褐+白头+黄喙"""
    brown = (100, 70, 45)
    brown_l = (140, 105, 70)
    white = (240, 240, 235)
    beak = (230, 180, 50)
    eye = (30, 25, 10)
    # 头（白色）
    draw.rectangle([28, 12, 100, 60], fill=white)
    # 眼睛（锐利）
    draw.rectangle([36, 28, 52, 40], fill=(255, 255, 220))
    draw.rectangle([40, 32, 52, 40], fill=eye)
    draw.rectangle([76, 28, 92, 40], fill=(255, 255, 220))
    draw.rectangle([80, 32, 92, 40], fill=eye)
    # 眉骨突出
    draw.rectangle([32, 24, 56, 28], fill=(180, 170, 160))
    draw.rectangle([72, 24, 96, 28], fill=(180, 170, 160))
    # 喙（黄色弯钩）
    draw.rectangle([52, 44, 76, 56], fill=beak)
    draw.rectangle([56, 56, 72, 64], fill=(210, 160, 30))
    draw.rectangle([60, 64, 68, 68], fill=(190, 140, 20))
    # 身体（深褐）
    draw.rectangle([24, 60, 104, 108], fill=brown)
    draw.rectangle([36, 68, 92, 100], fill=brown_l)
    # 翅膀
    draw.rectangle([4, 64, 28, 96], fill=brown)
    draw.rectangle([100, 64, 124, 96], fill=brown)
    # 脚（黄色）
    draw.rectangle([36, 104, 52, 120], fill=beak)
    draw.rectangle([76, 104, 92, 120], fill=beak)


def draw_wolf(draw, s):
    """狼 - 团队领航者：灰色系"""
    fur = (130, 135, 145)
    light = (170, 175, 185)
    dark = (85, 90, 100)
    belly = (200, 200, 210)
    eye = (200, 170, 50)
    nose = (40, 35, 30)
    # 左耳（尖耳）
    draw.rectangle([16, 4, 36, 28], fill=fur)
    draw.rectangle([20, 8, 32, 24], fill=light)
    # 右耳
    draw.rectangle([92, 4, 112, 28], fill=fur)
    draw.rectangle([96, 8, 108, 24], fill=light)
    # 头
    draw.rectangle([24, 24, 104, 72], fill=fur)
    draw.rectangle([32, 32, 96, 68], fill=light)
    # 眼睛（琥珀色）
    draw.rectangle([36, 36, 52, 48], fill=eye)
    draw.rectangle([42, 38, 50, 46], fill=(30, 25, 15))
    draw.rectangle([76, 36, 92, 48], fill=eye)
    draw.rectangle([82, 38, 90, 46], fill=(30, 25, 15))
    # 鼻子/口鼻
    draw.rectangle([44, 52, 84, 72], fill=belly)
    draw.rectangle([56, 52, 72, 60], fill=nose)
    # 身体
    draw.rectangle([28, 68, 100, 108], fill=fur)
    draw.rectangle([40, 76, 88, 104], fill=belly)
    # 脚
    draw.rectangle([32, 104, 52, 120], fill=dark)
    draw.rectangle([76, 104, 96, 120], fill=dark)


def draw_owl(draw, s):
    """猫头鹰 - 深夜思考者：棕褐+大圆眼"""
    body = (130, 100, 70)
    light = (180, 155, 120)
    dark = (90, 65, 45)
    face_disk = (200, 185, 165)
    eye_ring = (220, 210, 190)
    eye = (40, 30, 10)
    beak = (200, 160, 60)
    # 耳朵（角状）
    draw.rectangle([20, 0, 36, 20], fill=dark)
    draw.rectangle([92, 0, 108, 20], fill=dark)
    # 头
    draw.rectangle([24, 16, 104, 72], fill=body)
    # 面盘
    draw.rectangle([28, 24, 100, 68], fill=face_disk)
    # 大眼框
    draw.rectangle([30, 28, 58, 56], fill=eye_ring)
    draw.rectangle([36, 32, 52, 48], fill=(240, 200, 60))
    draw.rectangle([40, 36, 48, 44], fill=eye)
    draw.rectangle([70, 28, 98, 56], fill=eye_ring)
    draw.rectangle([76, 32, 92, 48], fill=(240, 200, 60))
    draw.rectangle([80, 36, 88, 44], fill=eye)
    # 喙
    draw.rectangle([56, 52, 72, 64], fill=beak)
    # 身体
    draw.rectangle([28, 68, 100, 112], fill=body)
    draw.rectangle([36, 72, 92, 108], fill=light)
    # 胸纹（V形花纹）
    draw.rectangle([44, 76, 52, 84], fill=dark)
    draw.rectangle([76, 76, 84, 84], fill=dark)
    draw.rectangle([48, 84, 56, 92], fill=dark)
    draw.rectangle([72, 84, 80, 92], fill=dark)
    draw.rectangle([52, 92, 60, 100], fill=dark)
    draw.rectangle([68, 92, 76, 100], fill=dark)
    # 脚
    draw.rectangle([36, 108, 52, 120], fill=beak)
    draw.rectangle([76, 108, 92, 120], fill=beak)


def draw_dolphin(draw, s):
    """海豚 - 创意连接者：海蓝色+白肚"""
    body = (70, 140, 200)
    light = (100, 170, 225)
    belly = (210, 230, 245)
    dark = (45, 100, 160)
    eye = (25, 30, 40)
    # 头部（流线型）
    draw.rectangle([28, 28, 100, 68], fill=body)
    draw.rectangle([36, 32, 96, 64], fill=light)
    # 嘴（微笑长嘴）
    draw.rectangle([96, 40, 120, 52], fill=body)
    draw.rectangle([100, 44, 120, 52], fill=light)
    # 眼睛（友善的小眼）
    draw.rectangle([44, 40, 56, 48], fill=(255, 255, 255))
    draw.rectangle([48, 42, 56, 48], fill=eye)
    # 身体
    draw.rectangle([20, 64, 96, 100], fill=body)
    draw.rectangle([28, 72, 92, 96], fill=belly)
    # 背鳍
    draw.rectangle([52, 52, 68, 64], fill=dark)
    draw.rectangle([56, 44, 64, 56], fill=dark)
    # 尾鳍
    draw.rectangle([4, 72, 24, 84], fill=body)
    draw.rectangle([0, 64, 16, 76], fill=dark)
    draw.rectangle([0, 84, 16, 96], fill=dark)
    # 胸鳍
    draw.rectangle([36, 96, 56, 108], fill=dark)


def draw_ant(draw, s):
    """蚂蚁 - 系统构建者：深红棕+分段身体"""
    body = (140, 50, 40)
    dark = (100, 35, 25)
    light = (175, 75, 55)
    eye = (255, 255, 255)
    leg = (80, 30, 20)
    # 触角
    draw.rectangle([44, 0, 48, 20], fill=dark)
    draw.rectangle([36, 0, 44, 8], fill=dark)
    draw.rectangle([80, 0, 84, 20], fill=dark)
    draw.rectangle([84, 0, 92, 8], fill=dark)
    # 头
    draw.rectangle([32, 16, 96, 56], fill=body)
    draw.rectangle([36, 20, 92, 52], fill=light)
    # 眼睛
    draw.rectangle([40, 28, 52, 40], fill=eye)
    draw.rectangle([44, 32, 52, 40], fill=(30, 10, 5))
    draw.rectangle([76, 28, 88, 40], fill=eye)
    draw.rectangle([80, 32, 88, 40], fill=(30, 10, 5))
    # 下颚
    draw.rectangle([48, 48, 56, 60], fill=dark)
    draw.rectangle([72, 48, 80, 60], fill=dark)
    # 胸部（中段）
    draw.rectangle([40, 56, 88, 80], fill=body)
    draw.rectangle([44, 60, 84, 76], fill=light)
    # 腹部（大段）
    draw.rectangle([32, 80, 96, 112], fill=body)
    draw.rectangle([36, 84, 92, 108], fill=light)
    # 腿（6条）
    draw.rectangle([24, 60, 40, 64], fill=leg)
    draw.rectangle([20, 64, 28, 76], fill=leg)
    draw.rectangle([88, 60, 104, 64], fill=leg)
    draw.rectangle([100, 64, 108, 76], fill=leg)
    draw.rectangle([24, 80, 36, 84], fill=leg)
    draw.rectangle([20, 84, 28, 96], fill=leg)
    draw.rectangle([92, 80, 104, 84], fill=leg)
    draw.rectangle([100, 84, 108, 96], fill=leg)
    draw.rectangle([28, 100, 40, 104], fill=leg)
    draw.rectangle([24, 104, 32, 116], fill=leg)
    draw.rectangle([88, 100, 100, 104], fill=leg)
    draw.rectangle([96, 104, 104, 116], fill=leg)


def draw_chameleon(draw, s):
    """变色龙 - 万能适应者：绿色系+卷尾+大眼"""
    body = (80, 170, 100)
    light = (120, 200, 130)
    dark = (50, 120, 65)
    belly = (150, 210, 140)
    eye_outer = (180, 210, 120)
    eye = (30, 30, 25)
    # 冠（头顶隆起）
    draw.rectangle([52, 4, 76, 20], fill=dark)
    draw.rectangle([56, 0, 72, 12], fill=body)
    # 头
    draw.rectangle([28, 16, 96, 60], fill=body)
    draw.rectangle([32, 20, 92, 56], fill=light)
    # 大眼（突出的圆眼）
    draw.rectangle([32, 24, 56, 48], fill=eye_outer)
    draw.rectangle([38, 30, 50, 42], fill=(255, 255, 240))
    draw.rectangle([42, 34, 50, 42], fill=eye)
    # 嘴（长嘴微张）
    draw.rectangle([88, 36, 116, 48], fill=body)
    draw.rectangle([92, 40, 116, 48], fill=dark)
    # 身体
    draw.rectangle([24, 56, 92, 96], fill=body)
    draw.rectangle([32, 60, 88, 92], fill=light)
    draw.rectangle([40, 68, 84, 88], fill=belly)
    # 脊背条纹
    draw.rectangle([28, 56, 88, 60], fill=dark)
    # 脚
    draw.rectangle([28, 92, 48, 108], fill=dark)
    draw.rectangle([68, 92, 88, 108], fill=dark)
    # 卷尾
    draw.rectangle([8, 68, 28, 76], fill=body)
    draw.rectangle([4, 76, 16, 88], fill=body)
    draw.rectangle([8, 84, 24, 92], fill=body)
    draw.rectangle([16, 80, 28, 88], fill=dark)


def draw_cheetah(draw, s):
    """猎豹 - 速度之王：金黄+黑斑点+泪痕"""
    fur = (215, 180, 100)
    light = (235, 205, 140)
    dark = (170, 135, 65)
    spot = (50, 40, 25)
    belly = (240, 225, 190)
    eye = (35, 30, 10)
    nose = (40, 30, 25)
    # 耳朵
    draw.rectangle([20, 8, 40, 28], fill=dark)
    draw.rectangle([24, 12, 36, 24], fill=fur)
    draw.rectangle([88, 8, 108, 28], fill=dark)
    draw.rectangle([92, 12, 104, 24], fill=fur)
    # 头
    draw.rectangle([24, 24, 104, 72], fill=fur)
    draw.rectangle([32, 32, 96, 68], fill=light)
    # 眼睛
    draw.rectangle([36, 36, 52, 48], fill=(240, 220, 160))
    draw.rectangle([42, 38, 50, 46], fill=eye)
    draw.rectangle([76, 36, 92, 48], fill=(240, 220, 160))
    draw.rectangle([82, 38, 90, 46], fill=eye)
    # 泪痕（猎豹特征！）
    draw.rectangle([48, 44, 52, 68], fill=spot)
    draw.rectangle([76, 44, 80, 68], fill=spot)
    # 鼻子
    draw.rectangle([56, 52, 72, 60], fill=nose)
    # 嘴
    draw.rectangle([52, 60, 76, 66], fill=belly)
    # 身体
    draw.rectangle([24, 68, 104, 108], fill=fur)
    draw.rectangle([36, 76, 92, 104], fill=belly)
    # 斑点
    draw.rectangle([28, 76, 36, 84], fill=spot)
    draw.rectangle([44, 84, 52, 92], fill=spot)
    draw.rectangle([60, 80, 68, 88], fill=spot)
    draw.rectangle([80, 88, 88, 96], fill=spot)
    draw.rectangle([96, 76, 104, 84], fill=spot)
    draw.rectangle([72, 96, 80, 104], fill=spot)
    # 脚
    draw.rectangle([32, 104, 52, 120], fill=dark)
    draw.rectangle([76, 104, 96, 120], fill=dark)


def draw_turtle(draw, s):
    """乌龟 - 稳健守护者：绿壳+棕皮"""
    shell = (80, 130, 75)
    shell_l = (110, 165, 100)
    shell_d = (55, 95, 50)
    skin = (140, 130, 100)
    skin_l = (175, 165, 135)
    eye = (30, 30, 25)
    # 头
    draw.rectangle([72, 20, 112, 52], fill=skin)
    draw.rectangle([76, 24, 108, 48], fill=skin_l)
    # 眼
    draw.rectangle([88, 28, 100, 36], fill=(255, 255, 240))
    draw.rectangle([92, 30, 100, 36], fill=eye)
    # 嘴
    draw.rectangle([104, 36, 116, 44], fill=(120, 110, 80))
    # 龟壳（大椭圆）
    draw.rectangle([16, 44, 96, 100], fill=shell)
    draw.rectangle([20, 48, 92, 96], fill=shell_l)
    # 壳纹
    draw.rectangle([40, 52, 72, 56], fill=shell_d)
    draw.rectangle([28, 64, 84, 68], fill=shell_d)
    draw.rectangle([48, 56, 52, 92], fill=shell_d)
    draw.rectangle([64, 56, 68, 92], fill=shell_d)
    draw.rectangle([32, 76, 80, 80], fill=shell_d)
    draw.rectangle([40, 88, 72, 92], fill=shell_d)
    # 前脚
    draw.rectangle([8, 56, 24, 72], fill=skin)
    draw.rectangle([88, 56, 104, 72], fill=skin)
    # 后脚
    draw.rectangle([12, 88, 28, 104], fill=skin)
    draw.rectangle([84, 88, 100, 104], fill=skin)
    # 尾巴
    draw.rectangle([4, 72, 16, 80], fill=skin)


# ═══════════════════════════════════════════
#  🌟 金色传说 · 隐藏款
# ═══════════════════════════════════════════

def draw_lobster(draw, s):
    """小龙虾 - 木有感情的机器：红色+金色光泽"""
    body = (200, 55, 35)
    light = (230, 90, 60)
    dark = (150, 35, 20)
    gold = (255, 215, 80)
    gold_d = (220, 180, 50)
    eye = (20, 15, 10)
    # 触角
    draw.rectangle([24, 0, 28, 24], fill=dark)
    draw.rectangle([16, 0, 24, 8], fill=dark)
    draw.rectangle([100, 0, 104, 24], fill=dark)
    draw.rectangle([104, 0, 112, 8], fill=dark)
    # 眼睛柄
    draw.rectangle([32, 12, 40, 24], fill=body)
    draw.rectangle([88, 12, 96, 24], fill=body)
    draw.rectangle([28, 8, 40, 16], fill=(255, 255, 200))
    draw.rectangle([32, 10, 38, 14], fill=eye)
    draw.rectangle([88, 8, 100, 16], fill=(255, 255, 200))
    draw.rectangle([90, 10, 96, 14], fill=eye)
    # 头
    draw.rectangle([32, 24, 96, 64], fill=body)
    draw.rectangle([36, 28, 92, 60], fill=light)
    # 大钳子（左）
    draw.rectangle([0, 28, 32, 44], fill=body)
    draw.rectangle([0, 24, 16, 36], fill=dark)
    draw.rectangle([0, 36, 16, 48], fill=dark)
    draw.rectangle([4, 28, 28, 40], fill=light)
    # 大钳子（右）
    draw.rectangle([96, 28, 128, 44], fill=body)
    draw.rectangle([112, 24, 128, 36], fill=dark)
    draw.rectangle([112, 36, 128, 48], fill=dark)
    draw.rectangle([100, 28, 124, 40], fill=light)
    # 身体分节
    draw.rectangle([36, 64, 92, 76], fill=body)
    draw.rectangle([40, 68, 88, 76], fill=gold)
    draw.rectangle([36, 76, 92, 88], fill=body)
    draw.rectangle([40, 80, 88, 88], fill=gold_d)
    draw.rectangle([36, 88, 92, 100], fill=body)
    draw.rectangle([40, 92, 88, 100], fill=gold)
    # 尾扇
    draw.rectangle([40, 100, 56, 116], fill=body)
    draw.rectangle([56, 100, 72, 120], fill=dark)
    draw.rectangle([72, 100, 88, 116], fill=body)
    draw.rectangle([48, 116, 80, 124], fill=dark)
    # 金色高光
    draw.rectangle([44, 32, 52, 36], fill=gold)
    draw.rectangle([76, 32, 84, 36], fill=gold)


def draw_dragon(draw, s):
    """龙 - 各方面都很极致：金红色+龙角+鳞片"""
    body = (200, 50, 30)
    light = (230, 80, 50)
    dark = (150, 30, 15)
    gold = (255, 215, 80)
    gold_d = (220, 180, 50)
    scale = (180, 40, 25)
    eye_gold = (255, 200, 50)
    eye = (30, 10, 5)
    horn = (240, 220, 160)
    horn_d = (200, 180, 120)
    # 龙角（左）
    draw.rectangle([16, 0, 28, 24], fill=horn)
    draw.rectangle([20, 4, 28, 20], fill=horn_d)
    # 龙角（右）
    draw.rectangle([100, 0, 112, 24], fill=horn)
    draw.rectangle([100, 4, 108, 20], fill=horn_d)
    # 头
    draw.rectangle([28, 16, 100, 68], fill=body)
    draw.rectangle([32, 20, 96, 64], fill=light)
    # 龙眼（金色 + 竖瞳）
    draw.rectangle([36, 28, 56, 44], fill=eye_gold)
    draw.rectangle([44, 28, 48, 44], fill=eye)
    draw.rectangle([72, 28, 92, 44], fill=eye_gold)
    draw.rectangle([80, 28, 84, 44], fill=eye)
    # 龙鼻
    draw.rectangle([48, 48, 56, 56], fill=(180, 40, 20))
    draw.rectangle([72, 48, 80, 56], fill=(180, 40, 20))
    # 嘴
    draw.rectangle([40, 56, 88, 68], fill=dark)
    draw.rectangle([44, 58, 84, 64], fill=(255, 100, 50))
    # 龙须/鬃
    draw.rectangle([20, 24, 32, 36], fill=gold)
    draw.rectangle([96, 24, 108, 36], fill=gold)
    draw.rectangle([16, 32, 28, 44], fill=gold_d)
    draw.rectangle([100, 32, 112, 44], fill=gold_d)
    # 身体
    draw.rectangle([28, 64, 100, 108], fill=body)
    draw.rectangle([32, 68, 96, 104], fill=light)
    # 金色腹鳞
    draw.rectangle([44, 72, 84, 76], fill=gold)
    draw.rectangle([44, 80, 84, 84], fill=gold_d)
    draw.rectangle([44, 88, 84, 92], fill=gold)
    draw.rectangle([44, 96, 84, 100], fill=gold_d)
    # 脊背
    draw.rectangle([56, 60, 72, 64], fill=dark)
    # 脚（利爪）
    draw.rectangle([28, 104, 48, 120], fill=dark)
    draw.rectangle([80, 104, 100, 120], fill=dark)
    draw.rectangle([28, 116, 36, 124], fill=gold)
    draw.rectangle([40, 116, 48, 124], fill=gold)
    draw.rectangle([80, 116, 88, 124], fill=gold)
    draw.rectangle([92, 116, 100, 124], fill=gold)


# ═══════════════════════════════════════════
#  渲染器
# ═══════════════════════════════════════════

ANIMAL_DRAW_FNS = {
    "松鼠": draw_squirrel,
    "金丝猴": draw_golden_monkey,
    "雪豹": draw_snow_leopard,
    "蜜蜂": draw_bee,
    "鹰": draw_eagle,
    "狼": draw_wolf,
    "猫头鹰": draw_owl,
    "海豚": draw_dolphin,
    "蚂蚁": draw_ant,
    "变色龙": draw_chameleon,
    "猎豹": draw_cheetah,
    "乌龟": draw_turtle,
    "小龙虾": draw_lobster,
    "龙": draw_dragon,
}


def render_pixel_animal(name: str, pixel_size: int = 16) -> Image.Image:
    """渲染指定动物的像素头像，返回128×128 RGBA图片"""
    draw_fn = ANIMAL_DRAW_FNS.get(name)
    if not draw_fn:
        img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        return img
    return _draw_animal(128, draw_fn)


def generate_all_avatars(output_path: str = "pixel_avatars.png"):
    """生成所有14个像素风动物的预览图"""
    cols = 4
    avatar_display = 192  # 每个头像展示尺寸
    padding = 24
    label_h = 52

    cell_w = avatar_display + padding * 2
    cell_h = avatar_display + padding + label_h

    total_w = cols * cell_w + padding * 2

    regular_rows = 3
    total_h = (regular_rows + 1) * cell_h + padding * 2 + 140

    bg_color = (240, 245, 252)
    img = Image.new("RGB", (total_w, total_h), bg_color)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc", 28)
        label_font = ImageFont.truetype("/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc", 18)
        sub_font = ImageFont.truetype("/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc", 14)
        legend_font = ImageFont.truetype("/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc", 22)
    except:
        title_font = ImageFont.load_default()
        label_font = title_font
        sub_font = title_font
        legend_font = title_font

    # 标题
    title = "像素风灵兽图鉴 · 14 Arcana"
    bb = draw.textbbox((0, 0), title, font=title_font)
    tw = bb[2] - bb[0]
    draw.text(((total_w - tw) // 2, 20), title, font=title_font, fill=(40, 60, 100))

    animals_regular = [
        ("金丝猴", "灵动策略家"), ("雪豹", "冷静执行者"), ("蜜蜂", "极致工匠"), ("鹰", "全局掌控者"),
        ("松鼠", "知识囤积者"), ("狼", "团队领航者"), ("猫头鹰", "深夜思考者"), ("海豚", "创意连接者"),
        ("蚂蚁", "系统构建者"), ("变色龙", "万能适应者"), ("猎豹", "速度之王"), ("乌龟", "稳健守护者"),
    ]

    y_start = 60

    for i, (name, label) in enumerate(animals_regular):
        col = i % cols
        row = i // cols
        cx = padding + col * cell_w + cell_w // 2
        cy = y_start + row * cell_h

        # 卡片
        card_x = cx - avatar_display // 2 - 12
        card_y = cy
        card_w2 = avatar_display + 24
        card_h2 = avatar_display + 20 + label_h
        # 阴影
        draw.rounded_rectangle([card_x + 3, card_y + 3, card_x + card_w2 + 3, card_y + card_h2 + 3],
                               radius=12, fill=(210, 218, 230))
        draw.rounded_rectangle([card_x, card_y, card_x + card_w2, card_y + card_h2],
                               radius=12, fill=(255, 255, 255))

        # 头像
        avatar = render_pixel_animal(name)
        avatar = avatar.resize((avatar_display, avatar_display), Image.NEAREST)
        ax = cx - avatar_display // 2
        ay = cy + 10
        img.paste(avatar, (ax, ay), mask=avatar)

        # 标签
        ly = cy + 10 + avatar_display + 4
        bb = draw.textbbox((0, 0), name, font=label_font)
        nw = bb[2] - bb[0]
        draw.text((cx - nw // 2, ly), name, font=label_font, fill=(40, 60, 100))
        bb2 = draw.textbbox((0, 0), label, font=sub_font)
        sw = bb2[2] - bb2[0]
        draw.text((cx - sw // 2, ly + 22), label, font=sub_font, fill=(100, 120, 160))

    # 金色传说
    legend_y = y_start + regular_rows * cell_h + 20
    line_y = legend_y + 10
    for x in range(padding + 60, total_w - padding - 60):
        t = (x - padding - 60) / (total_w - 2 * padding - 120)
        brightness = 0.5 - abs(t - 0.5)
        r = int(200 + 55 * brightness * 2)
        g = int(160 + 55 * brightness * 2)
        b = int(20 + 30 * brightness * 2)
        draw.line([(x, line_y), (x, line_y + 2)], fill=(r, g, b))

    legend_title = "✨ 金色传说 · 隐藏款 ✨"
    bb = draw.textbbox((0, 0), legend_title, font=legend_font)
    ltw = bb[2] - bb[0]
    draw.text(((total_w - ltw) // 2, legend_y + 20), legend_title, font=legend_font, fill=(180, 140, 20))

    legend_card_y = legend_y + 56
    animals_legend = [("小龙虾", "木有感情的机器"), ("龙", "各方面都很极致")]
    legend_total_w = 2 * cell_w
    legend_start_x = (total_w - legend_total_w) // 2

    for i, (name, label) in enumerate(animals_legend):
        cx = legend_start_x + i * cell_w + cell_w // 2
        card_x = cx - avatar_display // 2 - 12
        card_y = legend_card_y
        card_w2 = avatar_display + 24
        card_h2 = avatar_display + 20 + label_h

        # 金色光晕
        for gs in range(4, 0, -1):
            draw.rounded_rectangle(
                [card_x - gs, card_y - gs, card_x + card_w2 + gs, card_y + card_h2 + gs],
                radius=14, fill=(255, 240, 180) if gs > 2 else (255, 250, 210))
        draw.rounded_rectangle([card_x, card_y, card_x + card_w2, card_y + card_h2],
                               radius=12, fill=(255, 252, 235), outline=(200, 160, 30), width=2)

        avatar = render_pixel_animal(name)
        avatar = avatar.resize((avatar_display, avatar_display), Image.NEAREST)
        ax = cx - avatar_display // 2
        ay = legend_card_y + 10
        img.paste(avatar, (ax, ay), mask=avatar)

        ly = legend_card_y + 10 + avatar_display + 4
        bb = draw.textbbox((0, 0), name, font=label_font)
        nw = bb[2] - bb[0]
        draw.text((cx - nw // 2, ly), name, font=label_font, fill=(160, 120, 10))
        bb2 = draw.textbbox((0, 0), label, font=sub_font)
        sw = bb2[2] - bb2[0]
        draw.text((cx - sw // 2, ly + 22), label, font=sub_font, fill=(180, 140, 40))

    img.save(output_path, "PNG", quality=95)
    print(f"✅ 像素头像预览已保存: {output_path} ({total_w}x{total_h})")
    return output_path


if __name__ == "__main__":
    generate_all_avatars("/data/workspace/personality-card/pixel_avatars_v2.png")
