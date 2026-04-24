"""
mirror.skill — 图片上传模块
自动上传映照图到免费图床，返回可直接访问的图片链接

支持图床（按优先级）：
1. imgloc.com    — 免费、无需注册、直链域名 i.imgs.ovh（微信可打开 ✅）
2. imgbb.com     — 免费、匿名上传、直链域名 i.ibb.co
3. freeimage.host — 免费、无需注册、直链域名 iili.io（⚠️ 微信已封禁）

用法：
    from image_uploader import upload_image
    url = upload_image("/path/to/share_card.png")
    if url:
        print(f"图片链接: {url}")
"""

import base64
import re
import requests
from pathlib import Path

# 超时设置
UPLOAD_TIMEOUT = 60  # 秒


def _upload_imgloc(image_path: str) -> str:
    """
    上传到 imgloc.com（Chevereto 架构）
    图片域名: i.imgs.ovh — 微信可正常打开 ✅
    无需注册，返回永久直链
    """
    sess = requests.Session()
    sess.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })

    # 获取 auth_token
    page = sess.get('https://imgloc.com', timeout=UPLOAD_TIMEOUT)
    m = re.search(r'PF\.obj\.config\.auth_token\s*=\s*"([^"]+)"', page.text)
    if not m:
        return ""

    auth_token = m.group(1)

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    resp = sess.post('https://imgloc.com/json',
        files={'source': ('mirror.png', img_bytes, 'image/png')},
        data={'type': 'file', 'action': 'upload', 'auth_token': auth_token},
        timeout=UPLOAD_TIMEOUT
    )

    if resp.status_code == 200:
        j = resp.json()
        url = j.get('image', {}).get('url', '')
        if url:
            return url
    return ""


def _upload_imgbb(image_path: str) -> str:
    """
    上传到 imgbb.com（匿名上传，无需 API Key）
    图片域名: i.ibb.co
    """
    sess = requests.Session()
    sess.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })

    # 获取 auth_token
    page = sess.get('https://imgbb.com', timeout=UPLOAD_TIMEOUT)
    m = re.search(r'PF\.obj\.config\.auth_token\s*=\s*"([^"]+)"', page.text)
    if not m:
        return ""

    auth_token = m.group(1)

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    resp = sess.post('https://imgbb.com/json',
        files={'source': ('mirror.png', img_bytes, 'image/png')},
        data={'type': 'file', 'action': 'upload', 'auth_token': auth_token},
        timeout=UPLOAD_TIMEOUT
    )

    if resp.status_code == 200:
        j = resp.json()
        url = j.get('image', {}).get('url', '')
        if url:
            return url
    return ""


def _upload_freeimage(image_path: str) -> str:
    """
    上传到 freeimage.host
    ⚠️ 图片域名 iili.io 已被微信/企微封禁，仅作兜底
    """
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    resp = requests.post("https://freeimage.host/api/1/upload", data={
        "key": "6d207e02198a847aa98d0a2a901485a5",
        "source": img_b64,
        "format": "json",
    }, timeout=UPLOAD_TIMEOUT)

    if resp.status_code == 200:
        j = resp.json()
        if j.get("status_code") == 200 and "image" in j:
            return j["image"]["url"]
    return ""


# 图床列表，按优先级排列
UPLOADERS = [
    ("imgloc.com (i.imgs.ovh)", _upload_imgloc),
    ("imgbb.com (i.ibb.co)", _upload_imgbb),
    ("freeimage.host (iili.io)", _upload_freeimage),
]


def upload_image(image_path: str) -> str:
    """
    自动上传图片到可用的免费图床

    Args:
        image_path: 本地图片文件路径

    Returns:
        成功返回图片直链 URL，全部失败返回空字符串
    """
    path = Path(image_path)
    if not path.exists():
        print(f"  ❌ 图片文件不存在: {image_path}")
        return ""

    file_size = path.stat().st_size
    if file_size > 30 * 1024 * 1024:  # 30MB
        print(f"  ❌ 图片太大 ({file_size / 1024 / 1024:.1f}MB)，超过图床限制")
        return ""

    for name, uploader in UPLOADERS:
        try:
            url = uploader(image_path)
            if url:
                print(f"  ✅ 已上传到 {name}")
                return url
        except requests.exceptions.Timeout:
            print(f"  ⚠️ {name} 上传超时，尝试下一个...")
        except requests.exceptions.ConnectionError:
            print(f"  ⚠️ {name} 连接失败，尝试下一个...")
        except Exception as e:
            print(f"  ⚠️ {name} 上传失败: {e}")

    print("  ❌ 所有图床均上传失败")
    return ""


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "/data/workspace/personality-card/share_card.png"
    url = upload_image(path)
    if url:
        print(f"\n🔗 图片链接: {url}")
    else:
        print("\n❌ 上传失败")
