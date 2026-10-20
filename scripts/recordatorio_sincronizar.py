#!/usr/bin/env python3
"""Recordatorio de inicio de sesión: ¿hay trabajo nuevo en los repos destino?

Hook SessionStart de Claude Code. Determinístico: no llama a Claude. Lee CHECKLIST.md
y, para cada ítem que no esté 'hecho' y tenga una línea `Ruta local:`, cuenta los
commits del repo destino (solo lectura, `git log`) hechos desde la fecha de
`Última sincronización:`. También avisa si algún HTML quedó desfasado.

No lanza el agente: solo recuerda qué pedirle. Cualquier error se ignora en silencio
para no estorbar el inicio de sesión.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))


def leer_items(texto):
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.DOTALL)
    lista, actual = [], None
    for linea in texto.splitlines():
        if linea.startswith("## "):
            actual = {"titulo": linea[3:].strip(), "lineas": []}
            lista.append(actual)
        elif actual is not None:
            actual["lineas"].append(linea)
    return lista


def campo(lineas, nombre):
    for ln in lineas:
        m = re.match(rf"^\s*{nombre}:\s*(.+)$", ln)
        if m:
            return m.group(1).strip()
    return ""


def commits_desde(ruta, fecha):
    r = subprocess.run(
        ["git", "-C", ruta, "log", f"--since={fecha}", "--format=%h"],
        capture_output=True, text=True, timeout=15,
    )
    return len([x for x in r.stdout.splitlines() if x.strip()]) if r.returncode == 0 else None


def main():
    md = RAIZ / "CHECKLIST.md"
    if not md.exists():
        return
    avisos = []
    for it in leer_items(md.read_text(encoding="utf-8")):
        t = it["titulo"]
        if re.search(r"estado:\s*hecho", t, re.I):
            continue
        nombre = re.sub(r"\s*\(estado:[^)]*\)\s*$", "", t)
        casillas = [ln for ln in it["lineas"] if re.match(r"^\s*-\s+\[[ xX]\]", ln)]
        hechas = sum(1 for ln in casillas if re.match(r"^\s*-\s+\[[xX]\]", ln))
        resumen = f"{nombre} ({hechas}/{len(casillas)} casillas)"
        ruta = campo(it["lineas"], "Ruta local")
        sync = campo(it["lineas"], r"Última sincronización")
        fecha = re.match(r"\d{4}-\d{2}-\d{2}", sync)
        if not ruta:
            avisos.append(f"- {resumen}: falta la línea 'Ruta local:' para poder revisar el repo.")
            continue
        if not fecha:
            avisos.append(f"- {resumen}: nunca sincronizado. Conviene sincronizar.")
            continue
        n = commits_desde(ruta, fecha.group(0))
        if n is None:
            avisos.append(f"- {resumen}: no pude leer el repo en '{ruta}'.")
        elif n > 0:
            avisos.append(f"- {resumen}: {n} commit(s) nuevos en el repo destino desde {fecha.group(0)}.")
        else:
            avisos.append(f"- {resumen}: sin commits nuevos desde {fecha.group(0)}.")
    desfasados = ""
    try:
        r = subprocess.run(
            [sys.executable, str(RAIZ / "scripts" / "generar_checklist_html.py"), "--verificar"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 1:
            desfasados = "\n" + r.stdout.strip()
    except Exception:
        pass
    if not avisos and not desfasados:
        return
    texto = "Recordatorio de la academia (CHECKLIST.md):\n" + "\n".join(avisos)
    if any(("commit(s) nuevos" in a) or ("nunca sincronizado" in a) for a in avisos):
        texto += "\n\nPide: «usa conectar-academia-proyecto en modo sincronizar»."
    texto += desfasados
    print(json.dumps({
        "systemMessage": texto,
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": texto},
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
