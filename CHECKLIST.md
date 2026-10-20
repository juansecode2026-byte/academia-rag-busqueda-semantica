# Checklist — Academia RAG - Búsqueda semántica

<!--
FUENTE DE VERDAD. Este archivo lo lee Claude; CHECKLIST.html se genera desde aquí
con `python scripts/generar_checklist_html.py` y no se edita a mano.

Formato de cada ítem aceptado (lo propone el agente conectar-academia-proyecto):

## [N] <Repo destino> — <objetivo>   (estado: aceptado | en curso | hecho)
Fuente: documentacion/<archivo> §<sección>
Repositorio: <URL del repo donde se construye>   (aparece como botón en el HTML)
- [ ] <paso tomado de la documentación> — evidencia esperada: <ruta/artefacto en el repo destino>
Última sincronización: <fecha>

### Análisis de resultados — [N]
#### Qué se hizo
#### Herramientas y librerías
#### Lenguaje de programación
#### Por qué importa el resultado
#### Cómo optimizarlo

Etiquetas de cifras: [medido] [calculado] [estimado] [por verificar]
-->

## [1] CRM VENTAS (candyCRM) — RAG por tenant sobre catálogo y FAQ, con citas y medición   (estado: aceptado)
Fuente: documentacion/Guía búsqueda vectorial y rag.html §3, §5, §9 y §10; documentacion/Academia llms ia engineer de datos a agentes v1.1.html §8 y §10
Repositorio: https://github.com/Monkeyotbz/crm-ventas/tree/juanse-candycrm-ventas
Traspaso: traspasos/CRM-VENTAS-RAG.md
Ruta local: C:\Users\juans\Proyectos\LABORATORIO - AGENTES\CRM VENTAS   (la usa el recordatorio de inicio para contar commits nuevos)
- [ ] Decidir modelo de embeddings y dimensión (recomendado: 1536, sin migración) y anotar la decisión — evidencia esperada: entrada en CRM VENTAS/docs/DECISIONES.md
- [ ] Si la dimensión no es 1536, migración nueva que cambie kb_chunks.embedding y su índice (sin editar la migración aplicada) — evidencia esperada: archivo nuevo en CRM VENTAS/supabase/migrations/
- [ ] Convertir cada registro de catálogo y FAQ del tenant en un fragmento legible — evidencia esperada: CRM VENTAS/scripts/rag/ingesta.* con parámetros en su README
- [ ] Generar embeddings y guardarlos en kb_chunks con tenant_id, fuente y metadata, idempotente, solo en demo-pruebas — evidencia esperada: mismo conteo de filas en dos corridas
- [ ] Crear match_kb_chunks (security invoker, sin tenant_id por parámetro, con umbral de similitud) — evidencia esperada: migración nueva en CRM VENTAS/supabase/migrations/
- [ ] Probar que una consulta del tenant A no recupera chunks del tenant B — evidencia esperada: prueba o script con resultado documentado
- [ ] Recuperar top-k con los últimos 3 a 5 mensajes del cliente — evidencia esperada: función de recuperación con prueba
- [ ] Responder solo con lo recuperado, citar fuentes en conversation_insights.citas_rag y decir "no lo sé" si no alcanza — evidencia esperada: código de respuesta y una fila con citas_rag no vacío
- [ ] Armar el set de 30 a 50 preguntas, con vagas y sin respuesta — evidencia esperada: CRM VENTAS/agentes-sdk/validacion-rag/
- [ ] Medir recall@k, MRR, tokens por turno, latencia p50/p95 y fidelidad, cada cifra con su etiqueta — evidencia esperada: informe de la corrida con cifras [medido]
- [ ] Registrar por consulta tokens, ms de recuperación, registros recuperados y similitud máxima — evidencia esperada: migración nueva y filas reales
- [ ] Reindexar el fragmento afectado cuando cambia un dato, con prueba — evidencia esperada: script o trigger y prueba que cambia un dato y verifica el nuevo vector
- [ ] Pruebas automáticas y README del RAG, todo en git — evidencia esperada: carpeta del RAG en CRM VENTAS con pruebas, README y commits
Última sincronización: (sin sincronizar)

### Análisis de resultados — [1]
(vacío hasta cerrar el ítem o un tramo medible)
