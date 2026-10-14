"""Gera dark_mode.svg e light_mode.svg. Uso: pip install pillow && python gen.py avatar.png"""
import sys
from html import escape
from ascii import ascii_art

WIDTH = 58  # largura (em caracteres) da coluna de texto
INFO = [
    ("title", "felipe@fukuoka"),
    ("OS", "macOS, Linux"),
    ("Uptime", "TODO"),
    ("Host", "PX Ativos Judiciais"),
    ("Kernel", "Software Engineer"),
    ("IDE", "VS Code, Claude Code"),
    None,
    ("Languages.Programming", "TypeScript, C#, Python, SQL"),
    ("Languages.Infra", "AWS, Terraform, Docker, Postgres"),
    ("Languages.Real", "Português, English"),
    None,
    ("title", "Contact"),
    ("Email.Work", "TODO"),
    ("LinkedIn", "TODO"),
    ("GitHub", "ffukuokaPX"),
    None,
    ("title", "GitHub Stats"),
    ("Repos", "12 {Contributed: 11}"),
    ("Contributions (12m)", "2,675"),
]
THEMES = {
    "dark": dict(bg="#161b22", text="#c9d1d9", key="#ffa657", value="#a5d6ff", dots="#616e7f"),
    "light": dict(bg="#f6f8fa", text="#24292f", key="#953800", value="#0a3069", dots="#c2cfde"),
}

def info_line(item):
    if item is None:
        return ""
    k, v = item
    if k == "title":
        return f'<tspan class="key">{escape(v)}</tspan> <tspan class="dots">{"-" * (WIDTH - len(v) - 1)}</tspan>'
    dots = "." * (WIDTH - len(k) - len(v) - 4)
    return f'<tspan class="key">{escape(k)}</tspan>: <tspan class="dots">{dots}</tspan> <tspan class="value">{escape(v)}</tspan>'

def svg(art, t):
    lh, top = 17, 30
    art_lh = 14.5
    rows = max(len(art) * art_lh / lh, len(INFO))
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="975" height="{top + rows * lh:.0f}" font-family="Consolas,Menlo,monospace" font-size="14px">',
           f'<style>.key{{fill:{t["key"]}}}.value{{fill:{t["value"]}}}.dots{{fill:{t["dots"]}}}text,tspan{{white-space:pre}}</style>',
           f'<rect width="100%" height="100%" fill="{t["bg"]}" rx="15"/>',
           f'<text x="15" y="{top}" fill="{t["text"]}" font-size="12px">']
    out += [f'<tspan x="15" y="{top + i * art_lh:.1f}">{escape(l)}</tspan>' for i, l in enumerate(art)]
    out += ["</text>", f'<text x="470" y="{top}" fill="{t["text"]}">']
    out += [f'<tspan x="470" y="{top + i * lh}">{info_line(it)}</tspan>' for i, it in enumerate(INFO)]
    out += ["</text>", "</svg>"]
    return "\n".join(out)

if __name__ == "__main__":
    art = ascii_art(sys.argv[1], (112, 50, 365, 345), 60)
    for name, t in THEMES.items():
        open(f"{name}_mode.svg", "w").write(svg(art, t))
