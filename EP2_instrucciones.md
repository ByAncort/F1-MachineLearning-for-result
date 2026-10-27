# Evaluación Parcial 2: Modelos, decisiones e insights (40%)

**Asignatura:** MACHINE LEARNING_001V · Experiencia de Aprendizaje 2
**Entrega:** 29/10/2026 23:59 (UTC-3) · Intentos ilimitados · Puntaje máximo 100 · Rúbrica (se entrega por separado) · SafeAssign habilitado

**Grupo:** Christian Alexis Tapia Miranda · Claudio Andrés Cristóbal Iribarne Wiff · Diego Antonio Cortés Baeza · Mario Nicolás Escobar González

---

## Condiciones generales

| Ítem | Detalle |
|---|---|
| Modalidad | Grupos de 3 (máx. 4). Una nota por grupo |
| Plazo | 2 clases de desarrollo; presentaciones en la tercera |
| Exposición | 10 minutos por grupo |
| Entregables | Presentación (`.pptx`/`.ppt`) + notebook (`.ipynb`) con los datos necesarios para ejecutarlo |
| Ponderación | 40% de la asignatura |

**Cálculo de la nota EP2:**

- 80%: nota grupal de esta evaluación → **32%** de la nota final
- 20%: promedio individual de talleres y desafíos a la fecha → **8%** de la nota final

> Nota: el enunciado original dice que "la evaluación individual aporta un 32%", pero por la aritmética (0,8 × 40%) el 32% corresponde a la nota grupal y el 8% al promedio de talleres/controles.

---

## 1. Desafío

Investigar un dataset mediante **aprendizaje supervisado y no supervisado**. Presentar **tres insights** relevantes, respaldados por resultados reproducibles. En la exposición justificar:

- qué modelos eligieron,
- qué parámetros probaron,
- por qué seleccionaron la configuración final,
- por qué descartaron alternativas.

**Dataset:** preferentemente uno usado por algún integrante en la EP1. Se admite uno nuevo, sin ampliar plazos ni reducir exigencias. Debe permitir definir:

- una variable objetivo **categórica** (clasificación), y
- una variable objetivo **numérica** (regresión),

ambas con sentido en el contexto. **No se aceptan objetivos artificiales** creados solo para cumplir.

---

## 2. Trabajo exigido y evidencia

Mínimos verificables en la presentación y el notebook:

### Problema y datos
- [ ] 2 preguntas predictivas (clasificación y regresión) + 1 pregunta sobre segmentos/anomalías
- [ ] Origen, tamaño, variables, calidad y preparación de datos
- [ ] Explicar separación entrenamiento/prueba y cómo se evita fuga de información

### Clasificación
- [ ] 1 modelo implementado, ≥ 2 configuraciones evaluadas
- [ ] Matriz de confusión + métricas pertinentes (precision, recall, F1 y/o ROC-AUC)
- [ ] 1 algoritmo alternativo considerado y explicación de por qué no se eligió
- [ ] Si hay probabilidades: comparar 2 umbrales cuando tenga sentido

### Regresión
- [ ] 1 modelo implementado, ≥ 2 configuraciones evaluadas
- [ ] MAE, RMSE y/o R², con interpretación
- [ ] 1 algoritmo alternativo considerado y explicación de por qué no se eligió
- [ ] Evaluar regularización Ridge/Lasso cuando corresponda

### DBSCAN (obligatorio)
- [ ] ≥ 3 combinaciones de `eps` y `min_samples`
- [ ] Tabla: parámetros · nº de clústeres (sin ruido) · cantidad o % de ruido
- [ ] Justificar configuración final
- [ ] Caracterizar grupos y observaciones de ruido (si existen)

### K-Means y otros métodos (optativos)
- Si se usa K-Means: justificar `k` mediante codo/inercia y/o silueta
- DBSCAN **no** recibe un `k` fijo

### Insights
- [ ] 3 hallazgos diferentes, cada uno con: **hallazgo + evidencia** (gráfico/tabla/métrica) **+ interpretación + implicancia/recomendación**
- [ ] Incorporar evidencia de enfoques supervisados **y** no supervisados

### Sobre la elección técnica
- Para cada modelo elegido: parámetros probados, comparación y razón de selección.
- Para cada alternativa descartada: indicar si fue **ejecutada** o solo **considerada**. No inventar resultados.
- Si una técnica vista en clases (SVM con kernel, árboles, umbrales o penalización) no es pertinente, explicar brevemente por qué.
- Los árboles convencionales **no** usan el truco del kernel.

> **No cuenta como insight por sí solo:** «92% de accuracy», «DBSCAN encontró 4 grupos» o «Lasso obtuvo menor RMSE». Hay que explicar qué revelan esos resultados sobre el problema.

---

## 3. Presentación oral (10 minutos)

| Lámina | Contenido obligatorio |
|---|---|
| 1 | Dataset, problema y preguntas |
| 2 | Datos, preparación y estrategia de evaluación |
| 3 | Clasificación: alternativas, parámetros comparados, métricas y decisión |
| 4 | Regresión: alternativas, parámetros comparados, métricas y decisión |
| 5 | DBSCAN: tres pruebas, grupos, ruido y su interpretación |
| 6 | Tres insights con evidencia e implicancias |
| 7 | Conclusiones, limitaciones y recomendaciones |

Se evalúa la explicación de decisiones y hallazgos, **no una lectura del código**. La nota es grupal.

---

## 4. Notebook obligatorio

Orden de secciones:

1. Problema y preguntas
2. Carga / preparación de datos
3. Experimentos de clasificación
4. Experimentos de regresión
5. DBSCAN
6. Tres insights
7. Conclusiones

Para cada experimento, celdas **Markdown** con: modelo, parámetros, resultados, comparación y justificación.

**Verificación:**
- [ ] Se ejecuta de principio a fin
- [ ] Incluye los resultados y gráficos de la presentación
- [ ] Usa rutas relativas
- [ ] Adjunta el dataset si no puede descargarse automáticamente
- [ ] Indica dependencias

El notebook respalda las afirmaciones de la exposición; no reemplaza la presentación.

---

## 5. Calendario

| Clase | Trabajo |
|---|---|
| Jueves 22 oct 2026 | Dataset, preguntas, preparación, primeros modelos supervisados |
| Martes 27 oct 2026 | Comparaciones, DBSCAN, insights y preparación de la exposición |
| Jueves 29 oct 2026 | Presentaciones orales y entrega del notebook |

---

## Regla central

> Resultados sin evidencia o elecciones sin justificación técnica **no acreditan plenamente** el cumplimiento.
