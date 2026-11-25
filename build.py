#!/usr/bin/env python3
"""把 App 内的隐私政策文本生成为可托管的静态页。

为什么用生成而不是手写 HTML：隐私政策的**唯一文本来源**是
`rewardsystem_app/assets/docs/privacy_policy_en.txt` / `_zh.txt`（App 内的「隐私政策」页也读它）。
如果另抄一份 HTML，两次改动就会漂移——线上政策和 App 内政策不一致是审核风险，不是排版问题。
所以这里只做排版转换，不做任何文字改写；改文案请改 txt，然后重跑本脚本。

用法：python3 legal-site/build.py
校验：test/legal_site_test.dart 会比对 html 与 txt 是否一致（防「改了 txt 忘了重跑」）。
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(os.path.dirname(HERE), "rewardsystem_app", "assets", "docs")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def linkify(s: str) -> str:
    s = esc(s)
    s = re.sub(r"([\w.+-]+@[\w-]+\.[\w.]+)", r'<a href="mailto:\1">\1</a>', s)
    return s


def to_html(txt: str, lang: str, title: str) -> str:
    lines = [l.rstrip() for l in txt.replace("\r\n", "\n").split("\n")]
    body = []
    head_done = False
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if not head_done:
            body.append(f"<h1>{esc(line)}</h1>")
            head_done = True
            continue
        if re.match(r"^\d+\.\s", line):
            body.append(f"<h2>{esc(line)}</h2>")
        elif line.startswith(("Last updated", "最后更新")):
            body.append(f'<p class="meta">{esc(line)}</p>')
        else:
            body.append(f"<p>{linkify(line)}</p>")
    return (
        "<!DOCTYPE html>\n"
        f'<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f"<title>{title}</title>\n"
        '<link rel="stylesheet" href="style.css">\n</head>\n<body>\n'
        '<main>\n' + "\n".join(body) + "\n</main>\n"
        '<footer><a href="index.html">habitcub legal</a></footer>\n'
        "</body>\n</html>\n"
    )


def main() -> None:
    pairs = [
        ("privacy_policy_en.txt", "privacy.html", "en", "habitcub - Privacy Policy"),
        ("privacy_policy_zh.txt", "privacy-zh.html", "zh-Hans", "小进步 - 隐私政策"),
    ]
    for src, out, lang, title in pairs:
        with io.open(os.path.join(APP, src), encoding="utf-8") as f:
            txt = f.read()
        html = to_html(txt, lang, title)
        with io.open(os.path.join(HERE, out), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"wrote legal-site/{out}  ({len(html)} bytes, from {src})")


if __name__ == "__main__":
    main()
