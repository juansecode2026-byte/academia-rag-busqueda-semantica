# Academia RAG - Búsqueda semántica

Parte de la familia de academias de IA Engineer del laboratorio. Las reglas
universales están en el `CLAUDE.md` de la raíz del laboratorio y se cargan solas.

## Objetivo

Aprender búsqueda vectorial y RAG y **llevar lo aprendido a proyectos reales**.
La documentación de `documentacion/` es la fuente: de sus checklists de
construcción salen las propuestas de qué aplicar y dónde. El avance se lleva en
`CHECKLIST.md` y termina, por ítem, en un Análisis de resultados.

## Alcance

- Esta academia documenta, propone y registra avance. **No modifica** otros
  proyectos: el código se construye en el repo destino, en una sesión propia.
- El agente `conectar-academia-proyecto` (global, en `~/.claude/agents/`) es quien
  revisa los proyectos que no son academias y propone a cuál aplicar cada
  checklist. Modos: proponer, sincronizar, resultados.

## Excepción de aislamiento (autorizada por el usuario)

El agente puede **leer** los proyectos hermanos que **no son academias**, nunca
modificarlos, y nunca lee otras academias. Registro en `DECISIONES.md`.

## Archivos y quién manda

| Archivo | Para quién | Regla |
|---|---|---|
| `documentacion/*.html` | Usuario | Fuente de conocimiento. No se reescribe. |
| `CHECKLIST.md` | Claude | **Fuente de verdad** del avance y los resultados. |
| `CHECKLIST.html` | Usuario | **Generado** desde el MD. No se edita a mano. |
| `DECISIONES.md` | Ambos | Qué se aceptó, rechazó o aplazó, con su condición. |

Cada vez que cambie `CHECKLIST.md`, regenerar el HTML:

```
python scripts/generar_checklist_html.py
```

## Convenciones

- Las guías HTML pegadas por el usuario van tal cual en `documentacion/`, con nombre
  legible en español y versión.
- Toda cifra en un Análisis de resultados lleva etiqueta: `[medido]`,
  `[calculado]`, `[estimado]` o `[por verificar]`.
- `scripts/` es código determinístico, sin llamadas a Claude.
- Carpetas `.claude/`, `agentes-sdk/` y el resto de la plantilla: no se crean por
  defecto. La `PLANTILLA/` citada en el CLAUDE.md del laboratorio no existe en
  disco; si el usuario la quiere, se pide.
