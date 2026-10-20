# Decisiones — Academia RAG - Búsqueda semántica

<!--
Formato de una entrada:

### [D-N] Nombre
- Estado: ACEPTADO | RECHAZADO | APLAZADO
- Fecha:
- Qué es:
- Motivo:
- Condición de activación (solo APLAZADO): qué tendría que cambiar
- Procedencia: de dónde salió
-->

## Aceptados

### [D-1] Agente `conectar-academia-proyecto` como subagente markdown global
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: un solo agente de solo lectura (`Read, Grep, Glob`) en `~/.claude/agents/`, con tres modos: proponer, sincronizar y resultados.
- Motivo: lo dispara el usuario en sesión (subagente markdown, no SDK), no hay volumen que justifique orquestador, y al ser global sirve a todas las academias sin copias que sincronizar.
- Procedencia: pedido del usuario; forma elegida con el usuario el 2026-10-20.

### [D-2] Excepción de aislamiento: lectura de proyectos no-academia
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: el agente puede leer los proyectos hermanos que no son academias. Nunca los modifica y nunca lee otras academias.
- Motivo: el CLAUDE.md del laboratorio exige pedido explícito del usuario para cruzar proyectos; el usuario lo pidió para este fin.
- Procedencia: pedido del usuario el 2026-10-20.

### [D-3] `CHECKLIST.md` como fuente de verdad y `CHECKLIST.html` generado
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: el MD es el contexto para Claude; el HTML es la vista para el usuario y lo produce `scripts/generar_checklist_html.py` (determinístico, sin Claude). Sincronía de un solo sentido: MD → HTML.
- Motivo: evitar dos fuentes que se desalineen; el HTML nunca se edita a mano.
- Procedencia: pedido del usuario el 2026-10-20.

### [D-4] Cada ítem del checklist cierra con "Análisis de resultados"
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: cinco subtítulos fijos — qué se hizo, herramientas y librerías, lenguaje y por qué, por qué importa, cómo optimizar (tokens y efectividad).
- Motivo: que el aprendizaje quede explicado en palabras simples y con cifras etiquetadas.
- Procedencia: pedido del usuario el 2026-10-20.

## Aplazados

### [D-5] Hook que regenere `CHECKLIST.html` al editar `CHECKLIST.md`
- Estado: APLAZADO
- Fecha: 2026-10-20
- Qué es: hook en `.claude/settings.json` que corra el script de generación.
- Motivo: por ahora se corre a mano; automatizar antes de que duela vuelve rígido el flujo.
- Condición de activación: se olvidó regenerar el HTML al menos una vez, o se hizo a mano tres veces.
- Procedencia: plan del 2026-10-20.

## Rechazados

(ninguno todavía)
