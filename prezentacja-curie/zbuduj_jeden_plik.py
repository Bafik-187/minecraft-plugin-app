#!/usr/bin/env python3
"""Tworzy Prezentacja_Curie.html – jeden plik ze zdjęciami i czcionkami w środku."""
import base64, json, os, re
H = os.path.dirname(os.path.abspath(__file__))
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
html = open(os.path.join(H, "index.html"), encoding="utf-8").read()
css = open(os.path.join(H, "fonts", "fonts.css"), encoding="utf-8").read()
css = re.sub(r"url\(\./([^)]+\.woff2)\)", lambda m: "url(data:font/woff2;base64," + b64(os.path.join(H, "fonts", m.group(1))) + ")", css)
html = html.replace('<link rel="stylesheet" href="fonts/fonts.css">', "<style>\n" + css + "\n</style>")
media = {}
mj = os.path.join(H, "media", "media.js")
if os.path.exists(mj):
    media = json.loads(re.search(r"window\.MEDIA\s*=\s*(\{.*\});?\s*$", open(mj, encoding="utf-8").read(), re.S).group(1))
for k, m in list(media.items()):
    p = os.path.join(H, "media", m["file"])
    if not os.path.exists(p) or p.endswith(".webm"):
        continue
    mime = "image/png" if p.endswith(".png") else "image/jpeg"
    m["data"] = f"data:{mime};base64," + b64(p)
html = html.replace('<script src="media/media.js"></script>', "<script>window.MEDIA = " + json.dumps(media, ensure_ascii=False) + ";</script>")
cj = os.path.join(H, "media", "commons.js")
html = html.replace('<script src="media/commons.js"></script>', "<script>" + open(cj, encoding="utf-8").read() + "</script>")
out = os.path.join(H, "Prezentacja_Curie.html")
open(out, "w", encoding="utf-8").write(html)
print(out, os.path.getsize(out) // 1024, "KB,", sum("data" in m for m in media.values()), "zdjęć w środku")
