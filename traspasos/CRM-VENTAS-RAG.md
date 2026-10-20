# Traspaso: RAG por tenant en CRM VENTAS

**Para:** la sesión de Claude Code abierta dentro de `CRM VENTAS` (rama `juanse-candycrm-ventas`).
**De:** Academia RAG - Búsqueda semántica (decisión D-7, aceptada el 2026-10-20).
**Cómo usarlo:** pega este archivo en la sesión, o cópialo a `notas-locales/` de CRM VENTAS si esa carpeta no se sube a git. Mientras trabajas, el `CLAUDE.md` de CRM VENTAS manda sobre este documento.

> Todo lo que aparece como "ya existe" salió de una lectura de solo lectura que hizo un agente desde la academia. Puede estar desactualizado: **verifícalo en el repo antes de apoyarte en ello.**

## 1. Objetivo
Montar un sistema RAG de punta a punta en CRM VENTAS: que el Copiloto consulte el **catálogo y las FAQ de cada tenant** buscando por significado, responda **solo con lo recuperado**, **cite sus fuentes** y diga "no lo sé" cuando no haya información. Debe medirse (calidad, tokens, latencia) y quedar en git con pruebas y README.

Por qué: sin esto, o se mete todo el catálogo en el prompt (caro y lento al crecer) o se busca por palabra exacta (`ilike`) y las preguntas vagas como "algo tranquilo para mi esposo" no encuentran nada. También destraba los agentes aplazados [6a] Bot de Catálogo y [6c] Soporte/FAQ.

## 2. Reglas de trabajo (verifícalas contra el `CLAUDE.md` del repo)
- Repo de otra cuenta (`Monkeyotbz/crm-ventas`). Trabajar en la rama `juanse-candycrm-ventas`; los cambios llegan a la rama principal por pull request que revisa el dueño.
- **No editar migraciones ya aplicadas.** Todo cambio de base va en una migración nueva.
- Pruebas que escriban datos: **solo en el tenant `demo-pruebas`**; se limpian con `scripts/demo/limpiar-tenant-demo.sql`.
- **Avisar al dueño antes de aplicar migraciones a la base real.**
- La ingesta (llama a una API de embeddings, **no** a Claude) es código determinístico: va en `scripts/`. Un agente que llame a Claude va en `agentes-sdk/`; si tiene que ser un endpoint, va en `supabase/functions/` y el `CLAUDE.md` debe decir por qué.
- `kb_chunks` solo tiene política de lectura por tenant: la ingesta escribe con la clave de servicio, **solo del lado servidor**, nunca en el frontend.
- No subir claves ni `.env`.

## 3. Lo que ya existe (a verificar)
| Pieza | Dónde |
|---|---|
| Tabla `kb_chunks` (`tenant_id`, `contenido`, `embedding vector(1536)`, `fuente` ∈ catalogo/faq/documento, `metadata`) con índice HNSW coseno y RLS por tenant | `supabase/migrations/20260825115320_setup_multitenant_completo.sql` (≈ L508-520 y política ≈ L785) |
| Extensión `vector` movida al schema `extensions` | `supabase/migrations/20260825115441_hardening_search_path_y_extension_schema.sql` |
| Columna de citas `conversation_insights.citas_rag` (máx. 5) | misma migración inicial (≈ L349-355) |
| Búsqueda actual por `ilike` (tope 8) | `agentes-sdk/chatbot-claude/catalogo.py` |
| Catálogo del tenant Turismo Colombia (`tours`, jsonb es/en) | migración `20260904120000` y `scripts/importar-catalogo-turismo.mjs` |
| Molde de evaluación (30 casos, tokens y costo) | `agentes-sdk/validacion-analista/evaluar.py` y tabla `analista_ejecuciones` |
| Tenant de pruebas | `demo-pruebas` + `scripts/demo/` |

Nada de esto usa todavía `kb_chunks`. Faltan: ingesta, embeddings, función de búsqueda, respuesta con citas, set de evaluación.

## 4. Decisión previa (antes de escribir código)
**Modelo de embeddings y dimensión.** La columna es `vector(1536)`.

| Opción | Dimensión | Consecuencia |
|---|---|---|
| OpenAI `text-embedding-3-small` | 1536 | **Recomendada:** no exige migración. Requiere cuenta/clave de OpenAI (de pago). |
| Voyage AI | 1024 por defecto | Exige migración nueva que cambie la columna y el índice. Anthropic no tiene embeddings propios y recomienda a Voyage. |
| `sentence-transformers` local (384) | 384 | Exige migración y no corre en Edge Functions (Deno). Útil solo para una prueba local. |

Cambiar de modelo después obliga a recalcular todos los vectores. Anotar la decisión en `docs/DECISIONES.md` del repo.

## 5. Pasos (el mismo checklist que se sigue en la academia)
1. Decidir modelo y dimensión; anotarlo — *evidencia:* entrada en `docs/DECISIONES.md`.
2. Si la dimensión no es 1536: migración nueva que cambie `kb_chunks.embedding` y el índice — *evidencia:* archivo nuevo en `supabase/migrations/`.
3. Convertir cada registro de catálogo/FAQ del tenant en un fragmento de texto legible (frase en lenguaje natural, no JSON) — *evidencia:* `scripts/rag/ingesta.*` con la función de armado y los parámetros en un README.
4. Generar embeddings y guardarlos en `kb_chunks` con `tenant_id`, `fuente` y `metadata`, de forma idempotente (correrlo dos veces no duplica) y solo en `demo-pruebas` — *evidencia:* conteo de filas igual en dos corridas.
5. Crear `match_kb_chunks` (ver §6), sin recibir `tenant_id` por parámetro, con umbral mínimo de similitud — *evidencia:* migración nueva.
6. Probar que una consulta del tenant A no recupera chunks del tenant B — *evidencia:* prueba o script con resultado documentado.
7. Recuperar top-k usando los últimos 3 a 5 mensajes del cliente (no solo el último) — *evidencia:* función de recuperación con prueba.
8. Responder solo con lo recuperado, citar las fuentes en `conversation_insights.citas_rag` y decir "no lo sé" si no alcanza — *evidencia:* código de respuesta y una fila con `citas_rag` no vacío.
9. Armar el set de evaluación de 30 a 50 preguntas con el registro esperado, incluyendo preguntas vagas y preguntas **sin respuesta** en la base — *evidencia:* `agentes-sdk/validacion-rag/` (mismo patrón que `validacion-analista`).
10. Medir recall@k, MRR, tokens de contexto por turno, latencia de recuperación (p50 y p95) y fidelidad (cero inventos) — *evidencia:* informe de la corrida con cifras `[medido]`.
11. Registrar por consulta tokens, ms de recuperación, registros recuperados y similitud máxima — *evidencia:* migración nueva y filas reales.
12. Definir qué pasa cuando cambia un dato (reindexar el fragmento afectado) y probarlo — *evidencia:* script o trigger y una prueba.
13. Pruebas automáticas y README del RAG, todo en git — *evidencia:* carpeta del RAG con pruebas, README y commits.

## 6. Referencia técnica (de la guía de la academia; adaptar al stack)
Función de búsqueda en Postgres. El aislamiento entre empresas lo debe hacer la política RLS (`security invoker`), no un `tenant_id` que llegue desde el cliente. Confirmar que `kb_chunks` tenga su política antes de exponerla.

```sql
create or replace function match_kb_chunks(
  query_embedding extensions.vector(1536),
  match_count int default 6,
  min_similitud float default 0.3
)
returns table (id bigint, contenido text, fuente text, metadata jsonb, similitud float)
language sql stable security invoker
set search_path = public, extensions
as $$
  select id, contenido, fuente, metadata, 1 - (embedding <=> query_embedding) as similitud
  from kb_chunks
  where 1 - (embedding <=> query_embedding) >= min_similitud   -- RLS filtra por tenant
  order by embedding <=> query_embedding
  limit match_count;
$$;
```

Ideas que se mantienen aunque cambie el código:
- Un fragmento = un registro legible (nombre, tipo, ciudad, resumen, precio…), en lenguaje natural.
- La consulta usa los últimos 3 a 5 mensajes del cliente ("¿cuánto sale 5 noches ahí?" no dice dónde es "ahí").
- Búsqueda híbrida cuando convenga: filtro exacto (ciudad, precio) + orden por similitud.

## 7. Métricas (metas iniciales de la guía; son metas, no mediciones)
| Métrica | Qué responde | Meta inicial |
|---|---|---|
| Recall@k | ¿Llegó el registro correcto? | ≥ 95 % |
| MRR | ¿Llegó arriba? | ≥ 0,8 |
| Tokens de catálogo por turno | ¿Cuánto contexto envío? | < 1.200 |
| Latencia de recuperación | ¿La búsqueda frena la respuesta? | p95 < 300 ms |
| Fidelidad | ¿Respondió solo con lo recuperado? | 0 inventos |

Etiqueta toda cifra: `[medido]`, `[calculado]`, `[estimado]` o `[por verificar]`.

## 8. Preguntas abiertas
1. ¿Embeddings por API (OpenAI) o el modelo integrado del runtime de Supabase? Define la dimensión.
2. ¿Primero una consola (como `chatbot-claude`) o directo una Edge Function? Una nota previa recomendaba consola primero.
3. ¿Qué corpus primero: el catálogo de Turismo Colombia en `demo-pruebas` o una FAQ nueva?
4. ¿El dueño acepta que se aplique la migración nueva a la base real, y cuándo?

## 9. Qué devolver a la academia al terminar cada tramo
Para que el seguimiento y el análisis de resultados se escriban en la academia, anota y entrega:
- El enlace al commit o PR de cada paso hecho.
- Las cifras medidas, cada una con su etiqueta.
- Qué falló o qué se decidió distinto a lo planeado, y por qué.
- Cuántos tokens y cuánto costó cada corrida de evaluación.
