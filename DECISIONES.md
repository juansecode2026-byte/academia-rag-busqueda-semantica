# Decisiones — Academia RAG - Búsqueda semántica

<!--
Formato de una entrada:

### [D-N] Nombre
- Estado: ACEPTADO | RECHAZADO | APLAZADO | PROPUESTO (pendiente de veredicto)
- Fecha:
- Qué es:
- Motivo:
- Condición de activación (solo APLAZADO): qué tendría que cambiar
- Procedencia: de dónde salió

Las decisiones sobre un repo destino (aplicar un tramo de la documentación en un
proyecto) llevan además, siempre:
- Viabilidad: sí | condicional | no, y de qué depende
- Por qué es viable: cruce documentación de esta academia × escaneo del repo, con rutas
- Importancia (0-10): número y su justificación. Mide si el proyecto REALMENTE lo necesita: qué fricción resuelve o cuánto hace más efectivo un proceso (0 = nada importante, 10 = extremadamente importante). NO se califica por lo que ya está construido, ni porque "ya existe el esquema, entonces hay que usarlo". Si depende de un disparador futuro, dar el valor de hoy y el valor si se cumple
- Para qué se necesitaría allí: en función de que el proyecto sea óptimo (velocidad, efectividad, costo, escala)
- Qué pasa si no se implementa: el costo para el proyecto en esos mismos ejes (ej. buscar entre miles de conversaciones sin el sistema sería más lento y menos efectivo)
- Qué podría hacer un AI Engineer si se implementara:
- Encaje prospectivo (D-6): lo inferido, con su disparador y etiqueta [estimado]/[por verificar]

Y al final de la entrada, una conclusión en palabras simples para quien empieza en
el campo, que empieza con la línea `#### Conclusión en palabras simples` y trae
ocho subtítulos `#####`: 1 la situación, 2 palabras que necesitas conocer (tabla),
3 el problema (con una analogía), 4 la solución, 5 qué le aportaría al proyecto
(tabla), 6 qué pasa si no se hace, 7 qué haría un AI Engineer aquí, 8 un matiz
importante (límites y qué NO está respaldado).
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

### [D-5] `DECISIONES.md` también tiene su HTML, y ambos pares se mantienen a la par con un hook
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: `scripts/generar_checklist_html.py` genera `CHECKLIST.html` y `DECISIONES.html` (índice, títulos, subtítulos y botón de volver al índice). Un hook `PostToolUse` en `.claude/settings.json` lo corre cada vez que se edita `CHECKLIST.md` o `DECISIONES.md`. `--verificar` comprueba que ningún HTML esté desfasado.
- Motivo: el usuario quiere que cuando se actualice cualquiera de los archivos, el MD y su HTML estén siempre a la par. Esto activa el hook que estaba aplazado.
- Límite conocido: el hook solo dispara con ediciones hechas por Claude Code; si se edita un MD a mano en el IDE hay que correr el script (o `--verificar`).
- Procedencia: pedido del usuario el 2026-10-20 (reemplaza al antiguo D-5 aplazado).

### [D-6] Todo análisis incluye "encaje prospectivo"
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: además del encaje actual (qué hay hoy en el repo), el agente evalúa siempre si el objetivo de la documentación encajaría según lo que el repo va a construir, cómo y en qué etapa, aunque no exista código. Lo inferido va etiquetado y con su disparador.
- Motivo: un repo sin código para el objetivo no significa que no encaje. Ejemplo: en Calificación de llamadas, si habrá miles de llamadas habrá información que vectorizar y un RAG se vuelve necesario.
- Procedencia: pedido del usuario el 2026-10-20.

### [D-13] Al inicializar otra academia, nunca pisar archivos existentes; el usuario decide en el momento
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: cuando el agente arme la estructura (CHECKLIST, DECISIONES, script, hook) en otra academia y ya existan `CLAUDE.md` o `DECISIONES.md`, no los sobrescribe. En `CLAUDE.md` agrega una sección; para `DECISIONES.md` pregunta al usuario si fusionar o separar, y el usuario lo decide en ese momento, en esa academia.
- Motivo: cada academia ya tiene archivos propios (por ejemplo Mapeo Dominio y Scraping tiene `CLAUDE.md` y `DECISIONES.md`; la academia LLMs tiene `CLAUDE.md`) y la mejor opción depende del contenido de cada una.
- Procedencia: pedido del usuario el 2026-10-20.

### [D-14] Modo "inicializar" y plantillas globales para replicar la estructura en otras academias
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: un cuarto modo del agente que arma en una academia la estructura estándar (CHECKLIST y DECISIONES con sus HTML, script, hook), con el contexto de la documentación de esa academia. Las plantillas y el script viven en un solo lugar global (`~/.claude/plantillas-academia/`) y se copian a cada academia. El agente sigue sin escribir: entrega el contenido y la sesión principal escribe y muestra qué archivos son nuevos y cuáles ya existían.
- Motivo: esta academia (RAG - Búsqueda semántica) es la piloto, armada para tener una estructura productiva basada en proyectos propios; el usuario aprobó el diseño. Antes figuraba como aplazado hasta completar un ciclo real; el usuario lo aceptó antes.
- Alcance: las academias que ya estaban construidas no se tocan solas; se sincronizan solo cuando el usuario lo decide estando en ellas (ver D-13). Se invoca a mano: no se dispara solo al crear un repositorio.
- Procedencia: pedido del usuario el 2026-10-20.

### [D-15] Se construye en el repo destino; esta academia lo vincula y guarda el análisis
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: la implementación se hace directamente en el repositorio del proyecto (por ejemplo CRM VENTAS), en una sesión propia de ese repo, no aquí. Esta academia decide a qué proyecto aplicar cada checklist (modo proponer) y lleva el seguimiento: cada ítem del `CHECKLIST.md` lleva la línea `Repositorio:` (botón en el HTML) y enlaces a commits o PR como evidencia, y aquí se escribe el Análisis de resultados.
- Motivo: se usa el stack real, se evita portar el trabajo y la academia queda como registro con evidencia verificable. Respeta D-2: desde aquí no se modifican otros repositorios.
- Pendiente: confirmar de quién es el repositorio de CRM VENTAS y si hay permiso de escritura; si no lo hay, se trabaja en una copia (fork) con propuesta de cambios.
- Procedencia: propuesta del usuario el 2026-10-20.

### [D-7] RAG por tenant del Copiloto → CRM VENTAS (candyCRM)
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: checklist de RAG de punta a punta (chunking, embeddings, búsqueda por similitud, respuesta con citas, métricas) sobre catálogo y FAQ de cada tenant.
- Viabilidad: sí, alta. Depende de elegir el modelo de embeddings: la columna es `vector(1536)` y otro tamaño exige una migración nueva.
- Por qué es viable: la base ya está hecha. `kb_chunks` con `embedding vector(1536)`, índice HNSW coseno y RLS por tenant está en `supabase/migrations/20260825115320_setup_multitenant_completo.sql` (L508-520, L785), la columna `conversation_insights.citas_rag` reserva dónde mostrar las fuentes y el Analista ya trae un banco de 30 casos como molde de evaluación (`agentes-sdk/validacion-analista/`). Tu nota del 14-oct (Hoja de vida) ya dice que el RAG es lo primero. Cruza con §8 y §10 del checklist de la academia.
- Importancia (0-10): 7. Fricción que resuelve: el Copiloto no tiene cómo consultar el catálogo y las FAQ de cada empresa con fuentes; sin eso, o se mete todo en el prompt (caro y lento a medida que crece) o se busca por palabra exacta y las preguntas vagas no encuentran nada. Efectividad que gana: respuestas por significado y con citas, y una base de conocimiento que cada tenant nuevo puede traer sin tocar el prompt. No llega a 9-10 porque con catálogos pequeños la fricción todavía es leve.
- Para qué se necesitaría allí: para que el proyecto sea óptimo cuando crezca. Velocidad y costo: recuperar solo los fragmentos relevantes en vez de cargar todo el catálogo y FAQ de un tenant en cada llamada (en el piloto de la academia LLMs, documentado en la guía, el catálogo era el 68 % de la entrada de cada llamada). Efectividad: responder por significado ("algo tranquilo para mi esposo") y con citas verificables. Escala: que cada empresa nueva traiga su base de conocimiento sin tocar el prompt. De paso destraba el Bot de Catálogo y el de Soporte/FAQ, hoy aplazados.
- Qué pasa si no se implementa: a medida que crecen los tenants y el historial, consultar la base de conocimiento (y, a futuro, miles de conversaciones) por palabra exacta o cargándola entera es más lento, más caro en tokens y menos efectivo: las preguntas vagas no encuentran nada y las respuestas se apoyan en contexto irrelevante. `kb_chunks` y `citas_rag` quedan como esquema sin uso y los agentes aplazados siguen bloqueados.
- Qué podría hacer un AI Engineer si se implementara: construir ingesta con chunking y embeddings por tenant, una función de búsqueda aislada por empresa, respuesta que cita fuente y dice "no lo sé"; armar un set de 30+ preguntas y medir recall y fidelidad; y optimizar tokens por turno comparando k, tamaño de fragmento y modelo.
- Encaje prospectivo: se vuelve necesario cuando un tenant cargue un catálogo o FAQ que no quepa en el prompt [estimado].
- Veredicto: aceptado por el usuario el 2026-10-20. Se construye en CRM VENTAS, en la rama `juanse-candycrm-ventas` (ver D-15); el seguimiento está en el ítem [1] de `CHECKLIST.md` y el documento de traspaso en `traspasos/CRM-VENTAS-RAG.md`.
- Procedencia: agente `conectar-academia-proyecto`, modo proponer, 2026-10-20.

#### Conclusión en palabras simples

##### 1. La situación
CRM VENTAS tiene un **Copiloto**: una IA que ayuda a atender clientes. Para responder bien necesita conocer el **catálogo** y las **preguntas frecuentes (FAQ)** de cada empresa. Esta decisión propone darle una forma inteligente de consultar esa información.

##### 2. Palabras que necesitas conocer
| Palabra | Qué significa, en simple |
|---|---|
| **Tenant** | Cada empresa cliente del CRM, con sus propios productos y respuestas. |
| **Catálogo y FAQ** | La lista de lo que vende la empresa y sus preguntas y respuestas típicas. |
| **Prompt** | El texto que se le envía a la IA en cada llamada: instrucciones más la información que necesita. |
| **Token** | La unidad con la que se mide el texto. Más tokens significa más lento y más caro. |
| **RAG** | Una técnica en tres pasos: buscar lo relevante, dárselo a la IA y que responda con eso. |
| **Búsqueda por significado** | Encuentra textos por lo que quieren decir, no por las palabras exactas. |
| **Embedding** | Convertir un texto en una lista de números que representa su significado, para poder compararlo. |
| **Chunking** | Cortar un documento largo en trozos pequeños, para recuperar solo el que sirve. |
| **Citas** | Mostrar de qué documento salió cada dato, para poder verificarlo. |
| **`kb_chunks`** | La tabla de la base de datos donde se guardarían esos trozos con sus números. |

##### 3. El problema: una biblioteca sin bibliotecario
Imagina a un empleado que debe contestar preguntas de clientes y tiene dos formas malas de hacerlo. La primera es leerse toda la biblioteca antes de cada respuesta, que es lo mismo que meter todo el catálogo en el prompt: lento, caro y peor cada vez que la empresa agrega productos. La segunda es buscar por la palabra exacta: si el cliente pregunta "algo tranquilo para mi esposo" y esa frase no está escrita en el catálogo, no encuentra nada aunque el producto ideal exista.

##### 4. La solución: un bibliotecario inteligente (RAG)
1. **Preparación, una sola vez:** se cortan el catálogo y las FAQ en trozos y cada trozo se convierte en números. Se guardan en `kb_chunks`.
2. **Cada vez que un cliente pregunta:** la pregunta también se convierte en números y se buscan los trozos más parecidos en significado.
3. **Solo esos pocos trozos viajan a la IA,** que responde y cita de dónde sacó cada dato. Si no encuentra nada que sirva, dice "no lo sé" en vez de inventar.

##### 5. Qué le aportaría al proyecto
| Aporte | Qué cambia en concreto |
|---|---|
| **Velocidad y costo** | Se envían unos pocos trozos en vez de todo el catálogo. En un piloto de la academia LLMs, el catálogo completo era el 68 % del texto enviado en cada llamada (cifra de ese piloto, no de CRM VENTAS). |
| **Efectividad** | El Copiloto entiende preguntas vagas y responde con datos reales de esa empresa. |
| **Confianza** | Las citas permiten comprobar de dónde viene cada respuesta. |
| **Escala** | Una empresa nueva trae su catálogo y sus FAQ sin que haya que tocar el prompt. |
| **Desbloqueo** | Habilita dos agentes que hoy están aplazados: el Bot de Catálogo y el de Soporte/FAQ. |

##### 6. Qué pasa si no se hace
Con pocas empresas y catálogos pequeños, casi nada. A medida que el proyecto crece, cada respuesta sale más lenta y más cara, y las preguntas vagas se quedan sin respuesta. Por eso la nota es 7 de 10: la fricción es real, pero todavía leve.

##### 7. Qué haría un AI Engineer aquí
- **Construir la preparación:** cortar los textos, convertirlos en números y guardarlos por empresa.
- **Hacer la búsqueda:** una función que devuelva los trozos más parecidos, sin mezclar datos de una empresa con los de otra.
- **Hacer que la IA cite y diga "no lo sé"** cuando no haya información.
- **Medirlo:** preparar 30 o más preguntas con la respuesta correcta conocida y medir si encuentra el trozo correcto (*recall*) y si la respuesta se apoya en lo encontrado (*fidelidad*).
- **Optimizar:** probar cuántos trozos enviar, qué tamaño deben tener y qué modelo usar, para gastar menos tokens sin perder calidad.

##### 8. Un matiz importante
Todo esto está respaldado para el **catálogo y las FAQ**. Buscar entre **miles de conversaciones** es un uso posible a futuro, pero no es lo que `kb_chunks` está diseñada para guardar hoy.

### [D-16] Recordatorio automático de sincronización al abrir la sesión
- Estado: ACEPTADO
- Fecha: 2026-10-20
- Qué es: un hook `SessionStart` corre `scripts/recordatorio_sincronizar.py`, que lee `CHECKLIST.md`, cuenta los commits nuevos del repo destino desde la última sincronización (solo lectura, `git log`) y muestra un aviso con la frase para pedir la sincronización. También avisa si algún HTML está desfasado.
- Motivo: que no se olvide sincronizar después de trabajar en el repo destino.
- Límite conocido: el hook no lanza el agente por sí solo, porque necesita a Claude; solo recuerda qué pedirle. Requiere la línea `Ruta local:` en cada ítem del checklist.
- Procedencia: pedido del usuario el 2026-10-20.

## Propuestas pendientes de veredicto

Propuestas del agente `conectar-academia-proyecto` (2026-10-20). Ninguna está aceptada: el veredicto es del usuario. Cada una resume el cruce entre `documentacion/Academia llms ia engineer de datos a agentes v1.1.html` (y la Guía de búsqueda vectorial y RAG) y lo escaneado en el repo destino. Está sintetizado del informe del agente y no se verificó de nuevo contra los repos. Las cifras marcadas [estimado] son supuestos, no mediciones.

### [D-8] Banco de evaluación de 30-50 llamadas → Calificación de llamadas
- Estado: PROPUESTO (pendiente de veredicto)
- Fecha: 2026-10-20
- Qué es: set de llamadas etiquetadas por humanos, comparación IA contra humano por pregunta, y registro de costo por evaluación (§7 y §10 del checklist).
- Viabilidad: sí, media. El código es poco; el costo real es humano: calificar y anonimizar 30-50 llamadas.
- Por qué es viable: el evaluador ya existe con salida JSON (`backend/agent/output_schema.json`, `parser.ts`), hay columnas de corrección humana (`db/migrations/017_columnas_correccion_humana.sql`) y un caso real calificado a mano (`docs/caso-de-referencia-criterios.md`).
- Importancia (0-10): 8. Fricción que resuelve: hoy nadie puede decir qué tan bien califica el evaluador, y una calificación errónea cambia la comisión de un asesor; cada cambio de prompt o de modelo es una apuesta. Efectividad que gana: poder mejorar el evaluador con evidencia y comprobar si un modelo más barato aguanta. El freno es el trabajo humano de etiquetar llamadas, no la utilidad.
- Para qué se necesitaría allí: para que el evaluador sea óptimo y se pueda mejorar con datos. Efectividad: saber qué tan acertado es antes de tocar el prompt o el modelo (una llamada mal calificada afecta la comisión de un asesor). Costo: comprobar si un modelo más barato mantiene el acierto antes de cambiarlo.
- Qué pasa si no se implementa: cada cambio de prompt o de modelo se valida a ojo, no se puede demostrar que mejora ni que no empeora, y no se detecta si se está pagando de más por un modelo que no hace falta.
- Qué podría hacer un AI Engineer si se implementara: montar el banco, el script de acuerdo IA-humano con % de acierto por pregunta, y medir costo por llamada para decidir con datos si baja de Sonnet a un modelo más barato.
- Encaje prospectivo: es imprescindible cuando se cambie de modelo o de prompt, y la fase de revisión humana ya produce las etiquetas [estimado].
- Procedencia: agente `conectar-academia-proyecto`, 2026-10-20.

#### Conclusión en palabras simples

##### 1. La situación
En el call center, una IA lee cada llamada y la califica con preguntas de sí o no. Esa calificación influye en la comisión del asesor. Esta decisión propone medir qué tan bien califica la IA, comparándola con personas.

##### 2. Palabras que necesitas conocer
| Palabra | Qué significa, en simple |
|---|---|
| **Evaluador** | La IA que califica cada llamada. |
| **Banco de evaluación** | Un grupo de llamadas ya calificadas por personas, que sirve como "respuesta correcta" para comparar. |
| **Etiquetar** | Que una persona califique una llamada a mano. |
| **Acuerdo IA-humano** | El porcentaje de veces que la IA califica igual que la persona. |
| **Anonimizar** | Quitar nombres y datos personales de la llamada antes de usarla como ejemplo. |
| **Prompt y modelo** | Las instrucciones que recibe la IA y la IA misma. Cambiar cualquiera de los dos puede cambiar las calificaciones. |

##### 3. El problema: un juez al que nadie ha revisado
Hoy nadie puede decir qué tan acertado es el evaluador. Cada vez que se cambia el prompt o el modelo es una apuesta, y un error no es un detalle: afecta lo que cobra una persona.

##### 4. La solución: ponerle un examen
1. Se reúnen 30 a 50 llamadas y varias personas las califican a mano.
2. La IA califica esas mismas llamadas.
3. Se compara pregunta por pregunta y se calcula el porcentaje de coincidencia.
4. Se registra cuánto cuesta calificar cada llamada.

##### 5. Qué le aportaría al proyecto
| Aporte | Qué cambia en concreto |
|---|---|
| **Confianza** | Se puede decir con un número qué tan acertado es el evaluador. |
| **Mejora con evidencia** | Cada cambio de prompt se prueba contra el banco antes de usarlo. |
| **Costo** | Se puede comprobar si un modelo más barato aguanta la misma calidad. |
| **Justicia** | Menos riesgo de que una calificación errónea afecte la comisión de un asesor. |

##### 6. Qué pasa si no se hace
Los cambios se validan a ojo, no se puede demostrar que algo mejoró ni que no empeoró, y se podría estar pagando un modelo más caro de lo necesario sin saberlo. Por eso la nota es 8 de 10.

##### 7. Qué haría un AI Engineer aquí
- **Armar el banco** de llamadas etiquetadas y anonimizadas.
- **Escribir el script** que compara IA contra humano y da el porcentaje de acierto por pregunta.
- **Medir el costo** por llamada.
- **Decidir con datos** si conviene cambiar de modelo o de prompt.

##### 8. Un matiz importante
Lo difícil no es el código, es el trabajo humano de etiquetar y anonimizar las llamadas. Hoy hay un solo caso real calificado a mano, así que habría que conseguir el resto con el equipo de calidad.

### [D-9] RAG sobre transcripciones → Calificación de llamadas (prospectivo)
- Estado: PROPUESTO (pendiente de veredicto); el agente sugiere aplazar
- Fecha: 2026-10-20
- Qué es: búsqueda semántica sobre transcripciones, y recuperar correcciones humanas parecidas como ejemplos para el evaluador (§8).
- Viabilidad: condicional. Hoy no hay nada vectorial ni volumen; depende de D-8, porque sin banco no se puede medir si el RAG mejora al evaluador.
- Por qué es viable: `transcripciones.texto` ya guarda cada llamada en texto (`db/migrations/003_transcripciones.sql`) y el proyecto declara un Supabase por empresa. Con miles de llamadas por empresa habrá información que vectorizar.
- Importancia (0-10): 3 hoy, y sube a 8 si se cumple el disparador. Fricción hoy: casi ninguna, porque con pocas llamadas por empresa nadie necesita buscar entre ellas y no hay un pedido de búsqueda. Fricción si hay miles de llamadas: revisar a mano o por palabra literal sería lento y se perderían casos con el mismo significado; ahí la efectividad de calidad y coaching dependería de este sistema.
- Para qué se necesitaría allí: para que el proyecto siga siendo óptimo cuando haya miles de llamadas. Velocidad: encontrar en segundos las llamadas parecidas a una queja o a una objeción, sin revisarlas una por una. Efectividad: que la búsqueda entienda el significado aunque se diga con otras palabras, y que el evaluador reciba ejemplos ya corregidos por humanos.
- Qué pasa si no se implementa: hoy nada. Con miles de llamadas, encontrar casos parecidos sería lento y manual, la búsqueda por palabra literal pasaría por alto llamadas con el mismo significado y el evaluador no aprendería de las correcciones humanas, así que la calidad dependería de que alguien revise a mano.
- Qué podría hacer un AI Engineer si se implementara: fragmentar por turnos de conversación, habilitar pgvector en cada proyecto de empresa, recuperar correcciones como ejemplos y medir si mejora el acierto del evaluador.
- Encaje prospectivo: se vuelve necesario cuando una empresa supere unas 500 transcripciones [estimado] o haya al menos 30 correcciones humanas [estimado].
- Procedencia: agente `conectar-academia-proyecto`, 2026-10-20; ejemplo propuesto por el usuario.

#### Conclusión en palabras simples

##### 1. La situación
Cada llamada del call center se guarda como texto (una transcripción). Hoy son pocas, pero si llegan a ser miles, encontrar una llamada concreta o ver cómo se resolvió un caso parecido sería muy difícil.

##### 2. Palabras que necesitas conocer
| Palabra | Qué significa, en simple |
|---|---|
| **Transcripción** | La llamada escrita en texto. |
| **Búsqueda por significado** | Encuentra llamadas que dicen lo mismo aunque usen otras palabras. |
| **Ejemplo recuperado** | Una llamada ya corregida por una persona que se le muestra a la IA como guía antes de calificar una nueva. |
| **Disparador** | La señal que indica que ya es momento de construirlo, por ejemplo cuando el volumen crece. |

##### 3. El problema: encontrar una aguja en un pajar
Con pocas llamadas nadie necesita buscar. Con miles, revisar a mano es lento y la búsqueda por palabra exacta pasa por alto llamadas que dicen lo mismo con otras palabras.

##### 4. La solución: buscar por significado
Se convierten las transcripciones en números, como en D-7, y se buscan las más parecidas a lo que alguien pregunta. También se pueden mostrar al evaluador ejemplos parecidos que ya corrigió una persona.

##### 5. Qué le aportaría al proyecto
| Aporte | Qué cambia en concreto |
|---|---|
| **Velocidad** | Encontrar en segundos las llamadas parecidas a una queja u objeción. |
| **Efectividad** | No se pierden casos que usan otras palabras para decir lo mismo. |
| **Mejor calidad** | El evaluador aprende de las correcciones humanas. |

##### 6. Qué pasa si no se hace
Hoy casi nada, y por eso la nota es 3 de 10. Si el volumen llega a miles, la calidad y el coaching dependerían de que alguien revise llamadas a mano, y la nota subiría a 8.

##### 7. Qué haría un AI Engineer aquí
- **Cortar las llamadas por turnos** de conversación y guardarlas con sus números.
- **Activar la búsqueda vectorial** en el proyecto de cada empresa.
- **Medir** si mostrar ejemplos corregidos mejora el acierto del evaluador.

##### 8. Un matiz importante
No conviene construirlo todavía. Depende del volumen (el agente estima unas 500 llamadas por empresa, un supuesto, no una medición) y de que primero exista el banco de D-8, porque sin él no se puede medir si el sistema ayuda.

### [D-10] Extracción y chatbot sobre contratos → CRM mobiliaria
- Estado: PROPUESTO (pendiente de veredicto); discutible
- Fecha: 2026-10-20
- Qué es: pasar PDFs a JSON y consultar cláusulas con citas (§7 y el ejercicio "chatbot sobre contratos" de §8).
- Viabilidad: condicional. No hay contratos reales cargados ni CLAUDE.md o DECISIONES.md en el repo, y se solapa con el ERP.
- Por qué es viable: la tabla `documents` (`sale_contract`, `property_title`, PDFs en Storage) y `014_rental_contracts.sql` indican que el corpus existirá; hoy solo hay búsqueda `pg_trgm` por título.
- Importancia (0-10): 3 [por verificar]. No hay una fricción demostrada: no sé si alguien hoy pierde tiempo buscando cláusulas, porque no hay contratos reales cargados ni documentación de alcance legible. Si los contratos se consultan seguido, la efectividad ganada sería alta y subiría a 6-7; mientras no se confirme esa fricción, la necesidad es baja.
- Para qué se necesitaría allí: para que consultar contratos sea rápido y confiable. Velocidad: preguntar por cláusulas, plazos y penalidades sin abrir cada PDF. Efectividad: encontrar obligaciones por significado, no solo por palabra, y con cita del documento.
- Qué pasa si no se implementa: con muchos contratos, revisar una cláusula depende de abrir PDFs a mano o de la búsqueda por palabra, que es lenta y se salta lo dicho con otros términos; se pueden pasar por alto plazos o penalidades.
- Qué podría hacer un AI Engineer si se implementara: extraer cada contrato a JSON validado, indexar por cláusula y responder con cita de documento y página.
- Encaje prospectivo: se vuelve necesario cuando haya contratos reales cargados y alguien pregunte por cláusulas [estimado].
- Procedencia: agente `conectar-academia-proyecto`, 2026-10-20.

#### Conclusión en palabras simples

##### 1. La situación
Una inmobiliaria guarda contratos de venta, de arriendo y títulos de propiedad como archivos PDF. Para saber qué dice una cláusula, hoy alguien tiene que abrir el archivo y leerlo.

##### 2. Palabras que necesitas conocer
| Palabra | Qué significa, en simple |
|---|---|
| **Extracción** | Que la IA lea un PDF y saque los datos importantes en un formato ordenado (fechas, montos, partes). |
| **Cláusula** | Un punto concreto de un contrato, como un plazo o una penalidad. |
| **Chatbot sobre documentos** | Un asistente al que le preguntas y que responde con lo que dicen los contratos. |
| **Cita** | Indicar de qué documento y página salió la respuesta. |

##### 3. El problema: contratos que nadie puede preguntar
Los contratos son archivos, y buscar en ellos por palabra exacta encuentra términos, no obligaciones. Alguien que quiere saber "¿qué pasa si el inquilino se atrasa?" tiene que abrir PDF por PDF.

##### 4. La solución: preguntarle a los contratos
La IA extrae los datos de cada contrato a un formato ordenado, los textos se guardan por trozos con sus números (como en D-7) y se puede preguntar en lenguaje normal, con respuestas que citan el contrato.

##### 5. Qué le aportaría al proyecto
| Aporte | Qué cambia en concreto |
|---|---|
| **Velocidad** | Consultar una cláusula sin abrir cada PDF. |
| **Efectividad** | Encontrar obligaciones por significado, no solo por palabra. |
| **Confianza** | Cada respuesta cita el documento, así que se puede verificar. |

##### 6. Qué pasa si no se hace
Con pocos contratos, casi nada. Con muchos, revisar una cláusula depende de abrir archivos a mano y se pueden pasar por alto plazos o penalidades. La nota es 3 de 10 porque no se ha demostrado que alguien pierda tiempo con esto hoy.

##### 7. Qué haría un AI Engineer aquí
- **Convertir cada contrato** a datos ordenados y comprobar que sean correctos.
- **Indexar por cláusula** para poder buscar por significado.
- **Responder con cita** de documento y página.

##### 8. Un matiz importante
No hay contratos reales cargados todavía ni documentación clara de alcance, y se solapa con el proyecto del ERP, que prevé algo parecido. Antes de construirlo hay que confirmar si de verdad se consultan seguido.

### [D-11] Segmentación y deduplicación de leads → Scraping de leads
- Estado: PROPUESTO (pendiente de veredicto); discutible
- Fecha: 2026-10-20
- Qué es: K-Means para priorizar a quién llamar (§5) y embeddings para detectar duplicados difusos (§4).
- Viabilidad: condicional. No es RAG; sin volumen los grupos no significan nada.
- Por qué es viable: hay datos estructurados limpios (`leads_constructoras`, deduplicación por `place_id` y dominio) y un techo de 14.000 leads al mes; la Fase 7 conecta con calificación de leads.
- Importancia (0-10): 4. Fricción que resuelve: con miles de leads, el equipo no sabe a quién contactar primero y puede gastar llamadas y calificaciones en la misma empresa duplicada con otro nombre. Efectividad que gana: contactar primero a los más prometedores. Queda en 4 porque esa fricción depende del volumen real de leads, que no está medido; subiría a 6-7 con más de unos 1.000 leads [estimado].
- Para qué se necesitaría allí: para que el proyecto rinda con miles de leads. Efectividad: priorizar a quién contactar primero y unir "Constructora XYZ S.A.S." con "XYZ Constructora" cuando no hay sitio web. Costo: no gastar llamadas ni calificaciones en duplicados.
- Qué pasa si no se implementa: la Fase 7 arranca sin priorizar, el equipo trabaja la lista en orden arbitrario (menos efectivo) y los duplicados difusos se acumulan, con gasto de tiempo y de calificación repetido.
- Qué podría hacer un AI Engineer si se implementara: segmentar con scikit-learn, explicar cada grupo en lenguaje simple y medir cuántos duplicados nuevos detectan los embeddings frente a la regla actual.
- Encaje prospectivo: se vuelve necesario con más de unos 1.000 leads [estimado].
- Procedencia: agente `conectar-academia-proyecto`, 2026-10-20.

#### Conclusión en palabras simples

##### 1. La situación
El proyecto de scraping reúne empresas constructoras que podrían ser clientes (hasta 14.000 por mes) para que luego alguien las contacte. Esta decisión propone ordenarlas mejor y evitar contactar a la misma empresa dos veces.

##### 2. Palabras que necesitas conocer
| Palabra | Qué significa, en simple |
|---|---|
| **Lead** | Una empresa o persona que podría comprar. |
| **Duplicado difuso** | La misma empresa escrita de dos formas, como "Constructora XYZ S.A.S." y "XYZ Constructora". |
| **Segmentación (K-Means)** | Una técnica que agrupa cosas parecidas sin que nadie le diga cuáles son los grupos. |
| **Embedding** | Convertir un texto en números que representan su significado, para poder compararlo. |
| **Priorizar** | Decidir a quién contactar primero. |

##### 3. El problema: una lista larga sin orden
Con miles de leads, el equipo no sabe por dónde empezar y puede gastar llamadas y calificaciones en la misma empresa que aparece dos veces con nombres distintos.

##### 4. La solución: agrupar y comparar significados
Se agrupan los leads parecidos y se explica en palabras qué tiene en común cada grupo, para decidir a cuáles contactar primero. Además, se comparan los nombres y direcciones por significado para detectar duplicados que una regla simple no ve.

##### 5. Qué le aportaría al proyecto
| Aporte | Qué cambia en concreto |
|---|---|
| **Efectividad** | El equipo empieza por los leads más prometedores. |
| **Ahorro** | Menos llamadas y calificaciones gastadas en duplicados. |
| **Orden** | Grupos con una explicación clara de qué los une. |

##### 6. Qué pasa si no se hace
La calificación de leads arranca sin un orden de prioridad y los duplicados se van acumulando. La nota es 4 de 10 porque depende de cuántos leads haya de verdad.

##### 7. Qué haría un AI Engineer aquí
- **Limpiar y preparar** los datos de los leads.
- **Agrupar** con una herramienta de aprendizaje automático (scikit-learn) y explicar cada grupo.
- **Medir** cuántos duplicados nuevos detecta frente a la regla actual por dominio.

##### 8. Un matiz importante
Esto no es un sistema RAG: es aprendizaje automático clásico. Con pocos leads los grupos no significan nada, así que solo vale la pena cuando el volumen sea grande (el agente estima más de unos 1.000, un supuesto).

### [D-12] Banco de evaluaciones de agentes → CRM Productividad Hello-Minus
- Estado: PROPUESTO (pendiente de veredicto)
- Fecha: 2026-10-20
- Qué es: casos conocidos, juez separado y corrida antes de cada cambio de prompt (§10).
- Viabilidad: condicional. Su propia decisión [7] está aplazada hasta que un prompt de producción se modifique por segunda vez; este par solo se activa si esa condición se cumple.
- Por qué es viable: ya existe la tabla `eval_cases`, `trazas_agente` con tokens de entrada y salida, y tres agentes con LLM (Clasificador, Sugeridor, Verificador).
- Importancia (0-10): 5. Fricción que resuelve: no se puede saber si un cambio de prompt mejora o empeora un agente, ni cuánto cuesta y tarda cada uno de los tres. Efectividad que gana: cambiar prompts con evidencia y controlar el gasto en tokens. Es una fricción real pero moderada: crece cuando los prompts se modifiquen con frecuencia.
- Para qué se necesitaría allí: para que los agentes sean óptimos y confiables. Efectividad: probar cada cambio de prompt contra casos conocidos. Costo y velocidad: medir tokens y latencia de los tres agentes, no solo de uno.
- Qué pasa si no se implementa: los cambios de prompt se validan a ojo, no se sabe si un agente empeoró y sigue sin medirse el costo ni la velocidad de dos de los tres agentes.
- Qué podría hacer un AI Engineer si se implementara: cargar casos reales, instrumentar latencia y tokens en los otros dos agentes y correr la evaluación antes de cada cambio.
- Encaje prospectivo: la condición de su [7] puede estar cerca si el Clasificador ya cambió de prompt [por verificar].
- Procedencia: agente `conectar-academia-proyecto`, 2026-10-20.

#### Conclusión en palabras simples

##### 1. La situación
CRM Productividad tiene tres agentes de IA que ayudan a organizar el trabajo de desarrollo: uno clasifica los cambios de código (commits), otro sugiere en qué etapa va un trabajo y otro verifica una lista de pendientes. Esta decisión propone comprobar que funcionan bien y medir cuánto cuestan.

##### 2. Palabras que necesitas conocer
| Palabra | Qué significa, en simple |
|---|---|
| **Agente** | Una IA con una tarea concreta. |
| **Caso de prueba** | Un ejemplo con la respuesta correcta ya conocida. |
| **Juez** | Lo que compara la respuesta del agente con la correcta (puede ser otra IA o una regla). |
| **Telemetría** | El registro automático de cuánto texto y cuánto tiempo gasta cada agente. |
| **Latencia** | Cuánto se demora en responder. |
| **Regresión** | Que un cambio arregle una cosa y rompa otra que funcionaba. |

##### 3. El problema: cambiar sin saber si mejoró
Cuando se modifica el prompt de un agente, hoy se revisa a ojo. No hay forma de saber si empeoró, y dos de los tres agentes no tienen medido cuánto cuestan ni cuánto tardan.

##### 4. La solución: una prueba antes de cada cambio
Se reúnen casos con la respuesta correcta conocida, se corren antes de publicar cada cambio de prompt y se registran tokens y tiempo en los tres agentes, no solo en uno.

##### 5. Qué le aportaría al proyecto
| Aporte | Qué cambia en concreto |
|---|---|
| **Seguridad al cambiar** | Se detecta si un cambio empeoró algo antes de que llegue a producción. |
| **Control del gasto** | Se sabe cuánto cuesta y cuánto tarda cada agente. |
| **Decisiones con datos** | Se puede comparar dos versiones de un prompt con números. |

##### 6. Qué pasa si no se hace
Los cambios de prompt se siguen validando a ojo y no se sabe si un agente empeoró ni cuánto gasta. La nota es 5 de 10: la fricción es real pero moderada, y crece cuando los prompts cambien con frecuencia.

##### 7. Qué haría un AI Engineer aquí
- **Cargar casos reales** con su respuesta correcta.
- **Medir tokens y tiempo** en los otros dos agentes.
- **Correr la evaluación** antes de cada cambio de prompt.

##### 8. Un matiz importante
Esto no es un sistema RAG: es evaluación y medición de agentes. El proyecto ya tiene su propia medición en uno de los agentes y su propia decisión aplazada con una condición, así que no conviene instalar herramientas externas que dupliquen lo que ya mide.

## Aplazados

(ninguno todavía)

## Rechazados

(ninguno todavía)
