"""Generate docs/assets/stack-{dark,light}.svg for the showcase README.

Icons come from the simple-icons npm package (CC0); download and unpack it anywhere:
    curl -sO https://registry.npmjs.org/simple-icons/-/simple-icons-16.35.0.tgz && tar xzf simple-icons-16.35.0.tgz
    python3 scripts/gen_stack.py package docs/assets

Versions and labels live in PANELS / LLM_CHAIN below.
"""
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ICONS_DIR = Path(sys.argv[1])          # simple-icons package root
OUT_DIR = Path(sys.argv[2])            # showcase docs/assets

brand = {it["slug"] if "slug" in it else re.sub(r"[^a-z0-9]", "", it["title"].lower()): it["hex"]
         for it in json.load(open(ICONS_DIR / "data/simple-icons.json"))}


def icon_path(slug):
    svg = (ICONS_DIR / "icons" / f"{slug}.svg").read_text()
    return re.search(r'<path d="([^"]+)"', svg).group(1)


THEMES = {
    "dark": dict(bg="#1a1828", card="#221f33", panel="#2a2540", chip="#332d4d",
                 border="#3d365a", accent="#a99bd6", text="#f4f0ff", muted="#b8aed0", dim="#8e85a8"),
    "light": dict(bg="#f7f3ec", card="#ffffff", panel="#faf7f2", chip="#ffffff",
                  border="#e6dccf", accent="#b06a2c", text="#2a1d12", muted="#6b5844", dim="#8a7358"),
}

FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

# (slug or None, monogram, color override, name, detail)
PANELS = [
    ("Backend & data", [
        ("python", None, None, "Python", "3.12"),
        ("fastapi", None, None, "FastAPI", "0.143"),
        ("pydantic", None, None, "Pydantic", "v2"),
        ("sqlalchemy", None, None, "SQLAlchemy", "2.1"),
        ("postgresql", None, None, "PostgreSQL", "18"),
        ("keycloak", None, "#4fb3e8", "Keycloak", "26 · OIDC"),
    ]),
    ("AI & agents", [
        ("langgraph", None, None, "LangGraph", "1.2"),
        ("modelcontextprotocol", None, None, "FastMCP", "4.1"),
    ]),
    ("Frontend & quality", [
        ("javascript", None, None, "JavaScript", "ESM"),
        ("css", None, None, "CSS", "3 themes"),
        (None, "P", "#2EAD33", "Playwright", "e2e"),
        ("pytest", None, None, "pytest", "~370 tests"),
        ("eslint", None, None, "ESLint", "+ Stylelint"),
        ("ruff", None, None, "Ruff", "lint"),
    ]),
    ("Infra & delivery", [
        ("docker", None, None, "Docker", "Compose"),
        ("caddy", None, None, "Caddy", "auto-HTTPS"),
        ("hetzner", None, None, "Hetzner", "Cloud VPS"),
        ("githubactions", None, None, "GitHub Actions", "CI"),
        ("letsencrypt", None, "#4c8fd6", "Let's Encrypt", "TLS"),
        ("dependabot", None, "#3a9bd9", "Dependabot", "weekly"),
    ]),
]

LLM_CHAIN = [
    (None, "G", "#F55036", "Groq"),
    ("googlegemini", None, None, "Gemini"),
    ("deepseek", None, None, "DeepSeek"),
    (None, "AI", None, "OpenAI"),
    ("anthropic", None, "#d97757", "Anthropic"),
    ("ollama", None, None, "Ollama"),
]


def lum(hex_):
    r, g, b = (int(hex_.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mix(hex_, target, k):
    a = [int(hex_.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(target.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * k):02x}" for x, y in zip(a, b))


def icon_color(slug, override, t, bg):
    """Brand color, tinted toward white (dark theme) or black (light) until it reads on the chip."""
    col = override or ("#" + brand[slug] if slug else t["accent"])
    target = "#ffffff" if lum(bg) < 0.5 else "#000000"
    k = 0.0
    while contrast(mix(col, target, k), bg) < 4.0 and k < 1:
        k += 0.05
    return mix(col, target, k)


def tile(x, y, size, slug, mono, override, t, bg):
    col = icon_color(slug, override, t, bg)
    out = [f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.28:.1f}" '
           f'fill="{col}" fill-opacity="0.14"/>']
    pad = size * 0.2
    s = (size - 2 * pad) / 24
    if slug:
        out.append(f'<path transform="translate({x + pad:.1f} {y + pad:.1f}) scale({s:.4f})" '
                   f'fill="{col}" d="{icon_path(slug)}"/>')
    else:
        fs = size * (0.5 if len(mono) == 1 else 0.38)
        out.append(f'<text x="{x + size / 2:.1f}" y="{y + size / 2 + fs * 0.36:.1f}" text-anchor="middle" '
                   f'font-size="{fs:.1f}" font-weight="800" fill="{col}">{mono}</text>')
    return out


def build(theme):
    t = THEMES[theme]
    W, PAD, GAP = 960, 24, 16
    PW = (W - 2 * PAD - GAP) / 2
    PP, CG, CH = 18, 10, 40
    CW = (PW - 2 * PP - CG) / 2
    HEAD = 64
    PANEL_TITLE = 38
    PH = PP + PANEL_TITLE + 3 * CH + 2 * CG + PP
    H = HEAD + 2 * PH + GAP + PAD

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}" '
         f'font-family="{FONT}" role="img" aria-label="Rockfile tech stack">',
         '<title>Rockfile tech stack</title>',
         f'<rect width="{W}" height="{H:.0f}" rx="22" fill="{t["card"]}" stroke="{t["border"]}"/>',
         f'<text x="{PAD + 4}" y="40" font-size="13" font-weight="700" letter-spacing="2.2" fill="{t["accent"]}">TECH STACK</text>',
         f'<text x="{W - PAD - 4}" y="40" text-anchor="end" font-size="13" fill="{t["dim"]}">'
         f'one FastAPI monolith · vanilla JS · one Compose stack</text>']

    for i, (title, items) in enumerate(PANELS):
        px = PAD + (i % 2) * (PW + GAP)
        py = HEAD + (i // 2) * (PH + GAP)
        o.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{PW:.1f}" height="{PH:.1f}" rx="16" '
                 f'fill="{t["panel"]}" stroke="{t["border"]}"/>')
        o.append(f'<text x="{px + PP:.1f}" y="{py + PP + 14:.1f}" font-size="12" font-weight="700" '
                 f'letter-spacing="1.4" fill="{t["muted"]}">{escape(title.upper())}</text>')
        top = py + PP + PANEL_TITLE
        for j, (slug, mono, ov, name, detail) in enumerate(items):
            cx = px + PP + (j % 2) * (CW + CG)
            cy = top + (j // 2) * (CH + CG)
            o.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{CW:.1f}" height="{CH}" rx="11" '
                     f'fill="{t["chip"]}" stroke="{t["border"]}"/>')
            o += tile(cx + 7, cy + 7, 26, slug, mono, ov, t, t["chip"])
            o.append(f'<text x="{cx + 42:.1f}" y="{cy + 25:.1f}" font-size="14" font-weight="600" '
                     f'fill="{t["text"]}">{escape(name)}</text>')
            o.append(f'<text x="{cx + CW - 12:.1f}" y="{cy + 25:.1f}" text-anchor="end" font-size="12" '
                     f'fill="{t["dim"]}">{escape(detail)}</text>')
        if title.startswith("AI"):
            # LLM fallback chain fills the remaining two chip rows
            by = top + CH + CG
            bw, bh = PW - 2 * PP, 2 * CH + CG
            bx = px + PP
            o.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh}" rx="11" '
                     f'fill="{t["chip"]}" stroke="{t["border"]}"/>')
            o.append(f'<text x="{bx + 14:.1f}" y="{by + 22:.1f}" font-size="12" font-weight="600" '
                     f'fill="{t["muted"]}">LLM fallback chain</text>')
            o.append(f'<text x="{bx + bw - 14:.1f}" y="{by + 22:.1f}" text-anchor="end" font-size="12" '
                     f'fill="{t["dim"]}">LangChain with_fallbacks()</text>')
            step = (bw - 28) / len(LLM_CHAIN)
            for k, (slug, mono, ov, name) in enumerate(LLM_CHAIN):
                cxk = bx + 14 + step * k + step / 2
                o += tile(cxk - 14, by + 34, 28, slug, mono, ov, t, t["chip"])
                o.append(f'<text x="{cxk:.1f}" y="{by + 78:.1f}" text-anchor="middle" font-size="11.5" '
                         f'fill="{t["text"]}">{name}</text>')
                if k < len(LLM_CHAIN) - 1:
                    o.append(f'<text x="{cxk + step / 2:.1f}" y="{by + 53:.1f}" text-anchor="middle" '
                             f'font-size="14" fill="{t["dim"]}">→</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT_DIR.mkdir(parents=True, exist_ok=True)
for theme in THEMES:
    (OUT_DIR / f"stack-{theme}.svg").write_text(build(theme))
    print("written", OUT_DIR / f"stack-{theme}.svg")
