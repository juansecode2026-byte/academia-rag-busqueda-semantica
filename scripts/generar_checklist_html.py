#!/usr/bin/env python3
"""Genera CHECKLIST.html a partir de CHECKLIST.md (fuente de verdad).

Determinístico: sin llamadas a Claude, solo biblioteca estándar.
Uso:  python scripts/generar_checklist_html.py
El HTML es solo lectura: las casillas reflejan el MD, no se editan en el navegador.
"""
import html
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "CHECKLIST.md"
SALIDA = RAIZ / "CHECKLIST.html"

TAGS = {"medido": "medido", "calculado": "calculado", "estimado": "estimado", "por verificar": "verificar"}
RE_CASILLA = re.compile(r"^\s*[-*]\s+\[([ xX])\]\s+(.*)$")
RE_ITEM = re.compile(r"^\s*[-*]\s+(.*)$")
RE_TABLA_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


def inline(texto):
    """Escapa HTML y aplica `código`, **negrita** y etiquetas [medido] etc."""
    out = html.escape(texto, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    out = re.sub(
        r"\[(medido|calculado|estimado|por verificar)\]",
        lambda m: f'<span class="tag {TAGS[m.group(1)]}">{m.group(1)}</span>',
        out,
    )
    return out


def celdas(linea):
    return [c.strip() for c in linea.strip().strip("|").split("|")]


def render_bloque(lineas):
    """Convierte las líneas de una sección en HTML. Devuelve (html, hechas, total)."""
    out, i, hechas, total = [], 0, 0, 0
    n = len(lineas)
    while i < n:
        linea = lineas[i]
        if not linea.strip():
            i += 1
            continue
        if linea.strip().startswith("```"):
            i += 1
            codigo = []
            while i < n and not lineas[i].strip().startswith("```"):
                codigo.append(lineas[i])
                i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(codigo)) + "</code></pre>")
            continue
        m = re.match(r"^(#{3,4})\s+(.*)$", linea)
        if m:
            nivel = len(m.group(1))
            out.append(f"<h{nivel}>{inline(m.group(2))}</h{nivel}>")
            i += 1
            continue
        if "|" in linea and i + 1 < n and RE_TABLA_SEP.match(lineas[i + 1]):
            cab = celdas(linea)
            i += 2
            filas = []
            while i < n and "|" in lineas[i] and lineas[i].strip():
                filas.append(celdas(lineas[i]))
                i += 1
            t = "<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in cab) + "</tr>"
            for f in filas:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in f) + "</tr>"
            out.append(t + "</table>")
            continue
        if RE_CASILLA.match(linea):
            items = []
            while i < n and RE_CASILLA.match(lineas[i]):
                marca, txt = RE_CASILLA.match(lineas[i]).groups()
                hecho = marca.lower() == "x"
                total += 1
                hechas += hecho
                paso, _, evid = txt.partition(" — evidencia esperada:")
                cuerpo = f"<b>{inline(paso)}</b>"
                if evid:
                    cuerpo += f"<small>Evidencia esperada: {inline(evid.strip())}</small>"
                estado = " checked" if hecho else ""
                items.append(
                    f'<li><label><input type="checkbox" disabled{estado}>'
                    f'<span class="txt">{cuerpo}</span></label></li>'
                )
                i += 1
            out.append('<ul class="check">' + "".join(items) + "</ul>")
            continue
        if RE_ITEM.match(linea):
            items = []
            while i < n and RE_ITEM.match(lineas[i]) and not RE_CASILLA.match(lineas[i]):
                items.append(f"<li>{inline(RE_ITEM.match(lineas[i]).group(1))}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        parrafo = []
        while (
            i < n
            and lineas[i].strip()
            and not lineas[i].strip().startswith("```")
            and not re.match(r"^#{3,4}\s", lineas[i])
            and not RE_ITEM.match(lineas[i])
        ):
            parrafo.append(lineas[i].strip())
            i += 1
        if parrafo:
            out.append("<p>" + inline(" ".join(parrafo)) + "</p>")
        else:
            i += 1
    return "\n".join(out), hechas, total


def leer_md():
    texto = ENTRADA.read_text(encoding="utf-8")
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.DOTALL)
    titulo, intro, secciones, actual = "Checklist", [], [], None
    for linea in texto.splitlines():
        if linea.startswith("# ") and not linea.startswith("## "):
            titulo = linea[2:].strip()
        elif linea.startswith("## "):
            actual = {"titulo": linea[3:].strip(), "lineas": []}
            secciones.append(actual)
        elif actual is not None:
            actual["lineas"].append(linea)
        else:
            intro.append(linea)
    return titulo, intro, secciones


CSS = """
:root{--bg:#f5f7fb;--card:#fff;--text:#1c2230;--muted:#5a6477;--line:#e2e6ef;--primary:#2f5bea;--primary-soft:#e8eeff;--ok:#0e9f6e;--ok-soft:#e3f6ee;--warn:#c2410c;--warn-soft:#fff1e6;--code-bg:#0f172a;--code-text:#e2e8f0}
@media (prefers-color-scheme:dark){:root{--bg:#0e1117;--card:#161b26;--text:#e6e9f0;--muted:#9aa3b5;--line:#262d3d;--primary:#7c9bff;--primary-soft:#1b2540;--ok:#34d399;--ok-soft:#10261d;--warn:#fb923c;--warn-soft:#2a1a0e;--code-bg:#0a0d14}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.65}
header.hero{background:linear-gradient(135deg,#1d3fb8,#2f5bea 55%,#6a8cff);color:#fff;padding:50px 20px 72px;text-align:center}
header.hero .kicker{font-size:13px;letter-spacing:.12em;text-transform:uppercase;opacity:.85;font-weight:700}
header.hero h1{margin:8px 0;font-size:clamp(28px,6vw,42px)}
header.hero .meta{display:inline-block;margin-top:14px;background:rgba(255,255,255,.18);padding:6px 14px;border-radius:999px;font-size:14px;font-weight:600}
main{max-width:920px;margin:0 auto;padding:0 16px 100px}
nav#indice,section{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:26px 24px;margin:22px 0;scroll-margin-top:14px}
nav#indice{margin-top:-42px;box-shadow:0 8px 24px rgba(0,0,0,.1)}
h2{margin:0 0 6px;font-size:24px;color:var(--primary)}
h3{margin:26px 0 8px;font-size:19px;padding-top:14px;border-top:2px solid var(--line)}
h4{margin:18px 0 6px;font-size:16px;color:var(--primary)}
p{margin:8px 0}.lead{color:var(--muted)}
code{background:var(--primary-soft);padding:1px 6px;border-radius:5px;font-size:.9em}
pre{background:var(--code-bg);color:var(--code-text);padding:14px 16px;border-radius:12px;overflow-x:auto;font-size:13.5px;line-height:1.55;margin:10px 0}
pre code{background:none;padding:0;color:inherit}
table{width:100%;border-collapse:collapse;margin:12px 0;font-size:14.5px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}th{background:var(--primary-soft)}
ul,ol{padding-left:22px}
.bar{height:12px;background:var(--line);border-radius:999px;overflow:hidden}
.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--primary),var(--ok))}
.progress small{color:var(--muted)}
nav#indice ol{list-style:none;padding:0;margin:14px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:9px}
nav#indice a{display:flex;gap:10px;align-items:center;text-decoration:none;color:var(--text);background:var(--bg);border:1px solid var(--line);padding:10px 13px;border-radius:10px}
nav#indice a:hover{border-color:var(--primary);background:var(--primary-soft)}
nav#indice a b{background:var(--primary);color:#fff;border-radius:7px;min-width:28px;height:28px;display:inline-flex;align-items:center;justify-content:center;font-size:14px;flex:none}
.check{list-style:none;padding:0;margin:10px 0}.check li{margin:8px 0}
.check label{display:flex;gap:12px;align-items:flex-start;background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:11px 14px}
.check input{appearance:none;-webkit-appearance:none;flex:none;width:22px;height:22px;margin-top:2px;border:2px solid var(--primary);border-radius:6px;background:var(--card);position:relative}
.check input:checked{background:var(--ok);border-color:var(--ok)}
.check input:checked::after{content:"\\2713";position:absolute;inset:0;color:#fff;font-size:15px;font-weight:700;display:flex;align-items:center;justify-content:center}
.check input:checked ~ .txt{opacity:.65}
.txt b{display:block}.txt small{display:block;color:var(--muted);font-size:14px}
.sec-progress{font-size:13px;color:var(--muted);font-weight:600;margin-bottom:4px}
.tag{display:inline-block;font-size:12px;font-weight:700;padding:1px 8px;border-radius:999px;white-space:nowrap}
.medido{background:var(--ok-soft);color:var(--ok)}.calculado{background:var(--primary-soft);color:var(--primary)}
.estimado{background:var(--warn-soft);color:var(--warn)}.verificar{background:var(--line);color:var(--muted)}
.estado{display:inline-block;font-size:12px;font-weight:700;padding:2px 10px;border-radius:999px;background:var(--primary-soft);color:var(--primary);vertical-align:middle}
.back{display:inline-block;margin-top:16px;text-decoration:none;font-weight:600;font-size:14px;color:var(--primary);border:1px solid var(--primary);padding:7px 14px;border-radius:999px}
.back:hover{background:var(--primary);color:#fff}
.fab{position:fixed;right:16px;bottom:16px;z-index:50;background:var(--primary);color:#fff;text-decoration:none;font-weight:700;padding:12px 18px;border-radius:999px;box-shadow:0 6px 18px rgba(0,0,0,.3);font-size:15px}
footer{text-align:center;color:var(--muted);padding:10px 0 30px;font-size:14px}
"""


def pct(a, b):
    return round(a / b * 100) if b else 0


def main():
    if not ENTRADA.exists():
        sys.exit(f"No existe {ENTRADA}")
    titulo, intro, secciones = leer_md()
    intro_html, _, _ = render_bloque(intro)

    cuerpo, indice, th, tt = [], [], 0, 0
    for n, sec in enumerate(secciones, 1):
        ident = f"item{n}"
        contenido, h, t = render_bloque(sec["lineas"])
        th, tt = th + h, tt + t
        nombre = sec["titulo"]
        estado = ""
        m = re.search(r"\(estado:\s*([^)]+)\)\s*$", nombre)
        if m:
            estado = f' <span class="estado">{html.escape(m.group(1).strip())}</span>'
            nombre = nombre[: m.start()].strip()
        indice.append(f'<li><a href="#{ident}"><b>{n}</b> {inline(nombre)} ({h}/{t})</a></li>')
        cuerpo.append(
            f'<section id="{ident}"><h2>{inline(nombre)}{estado}</h2>'
            f'<div class="sec-progress">Avance de este ítem: {h} de {t}</div>'
            f"{contenido}"
            f'<a class="back" href="#indice">↑ Volver al índice</a></section>'
        )

    if not secciones:
        cuerpo.append(f'<section><div class="lead">{intro_html or "Todavía no hay ítems aceptados."}</div></section>')
        lista_indice = '<p class="lead">Sin ítems todavía.</p>'
    else:
        lista_indice = "<ol>" + "".join(indice) + "</ol>"

    hoy = date.today().strftime("%d/%m/%Y")
    salida = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo)}</title>
<style>{CSS}</style>
</head>
<body>
<header class="hero">
  <div class="kicker">Academia LLMs · IA Engineer</div>
  <h1>{html.escape(titulo)}</h1>
  <span class="meta">Generado desde CHECKLIST.md · {hoy}</span>
</header>
<main>
<nav id="indice">
  <h2>📚 Índice</h2>
  <p class="lead">Vista de solo lectura: se genera desde <code>CHECKLIST.md</code>. Para cambiar algo, se edita el MD y se regenera.</p>
  <div class="progress"><div class="bar"><i style="width:{pct(th, tt)}%"></i></div>
  <small>{th} de {tt} casillas completadas ({pct(th, tt)}%)</small></div>
  {lista_indice}
</nav>
{"".join(cuerpo)}
<footer>{html.escape(titulo)} · generado el {hoy}</footer>
</main>
<a class="fab" href="#indice" aria-label="Volver al índice">☰ Índice</a>
</body>
</html>
"""
    SALIDA.write_text(salida, encoding="utf-8")
    print(f"OK: {SALIDA.name} ({len(secciones)} ítems, {th}/{tt} casillas)")


if __name__ == "__main__":
    main()
