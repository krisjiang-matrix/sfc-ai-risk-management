#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 GitHub 仓库社交预览图（Social Preview）。

GitHub 不会自动为纯文档仓库生成预览图，需在仓库中放置一张图片，
并在 Settings → General → Social preview 中选择。

用法:
    python scripts/make_social_preview.py
    python scripts/make_social_preview.py --out .github/assets/images/social-preview.png

可选依赖: requirements-preview.lock（Pillow；不影响文档构建）
字体: 自动选择本机中文字体，或用 --font 指定；不下载或分发字体
"""

import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit('需要可选依赖 Pillow：python -m pip install Pillow')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

W, H = 1280, 640
BG_TOP = (26, 26, 46)
BG_BOTTOM = (12, 12, 24)
ACCENT = (124, 148, 255)
TEXT = (255, 255, 255)
MUTED = (168, 176, 205)

# 常见中文字体，按优先级尝试
CJK_CANDIDATES = [
    r'C:\Windows\Fonts\msyhbd.ttc',   # Microsoft YaHei Bold
    r'C:\Windows\Fonts\msyh.ttc',      # Microsoft YaHei
    r'C:\Windows\Fonts\simhei.ttf',    # SimHei
    r'C:\Windows\Fonts\simsun.ttc',    # SimSun
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
]

# 仓库实际数量，改动内容结构后请同步更新
STATS = '概念与机制  ·  实现与演算  ·  现有工具  ·  结果与局限'


def load_font(size, font_path=None):
    """Use a local font with Chinese glyphs; never silently render missing glyphs."""
    candidates = [font_path] if font_path else CJK_CANDIDATES
    sample = 'SFC AI 风险管理知识库理解概念方法工具以香港要求为背景开放实现演算现有结果局限' + STATS
    for path in candidates:
        if not os.path.isfile(path):
            continue
        try:
            font = ImageFont.truetype(path, size)
            missing = font.getmask('\U0010ffff')
            missing_signature = (missing.size, bytes(missing))
            for char in set(sample) - {' '}:
                glyph = font.getmask(char)
                if (glyph.size, bytes(glyph)) == missing_signature or not glyph.getbbox():
                    break
            else:
                return font
        except (OSError, ValueError):
            continue
    raise ValueError('找不到可用的中文字体；请用 --font 指定本机中文 TTF/TTC/OTF 文件。')


def vertical_gradient(size, top, bottom):
    w, h = size
    img = Image.new('RGB', (1, h))
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return img.resize((w, h), Image.BILINEAR)


def main():
    parser = argparse.ArgumentParser(description='生成 GitHub 社交预览图')
    parser.add_argument('--out', default=os.path.join(ROOT, '.github', 'assets', 'images',
                                                     'social-preview.png'))
    parser.add_argument('--font', help='本机中文字体文件（TTF/TTC/OTF）；不会下载字体')
    args = parser.parse_args()

    try:
        f_title = load_font(62, args.font)
        f_sub = load_font(30, args.font)
        f_small = load_font(20, args.font)
        f_stat = load_font(22, args.font)
    except ValueError as exc:
        parser.error(str(exc))

    base = Image.new('RGB', (W, H), BG_TOP)
    grad = vertical_gradient((W, H), BG_TOP, BG_BOTTOM)
    base.paste(grad, (0, 0))
    d = ImageDraw.Draw(base)

    # 顶部强调条
    d.rectangle([0, 0, W, 8], fill=ACCENT)

    x = 72
    y = 150

    # 眉标
    d.text((x, y - 78), 'HONG KONG SFC  ·  AI RISK MANAGEMENT', font=f_small, fill=ACCENT)

    # 主标题
    d.text((x, y), 'SFC AI 风险管理知识库', font=f_title, fill=TEXT)

    # 副标题
    y += 92
    d.text((x, y), '理解 AI 风险的概念、方法与工具', font=f_sub, fill=MUTED)
    y += 44
    d.text((x, y), '以香港 SFC 要求为背景的开放知识库', font=f_sub, fill=MUTED)

    # 分隔线
    y += 78
    d.rectangle([x, y, x + 96, y + 3], fill=ACCENT)

    # 统计行
    y += 34
    d.text((x, y), STATS, font=f_stat, fill=TEXT)

    # 角标：内容授权
    d.text((W - 300, H - 74), 'CC BY 4.0  ·  MIT', font=f_small, fill=MUTED)

    out = args.out
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    base.save(out, 'PNG', optimize=True)

    size_kb = os.path.getsize(out) / 1024
    print('已生成社交预览图: %s (%.0f KB, %dx%d)' % (out, size_kb, W, H))
    print('请在 GitHub 仓库 Settings → General → Social preview 中选择该文件。')


if __name__ == '__main__':
    main()