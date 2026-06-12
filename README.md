# 🦈 Shark Attack Analysis — Diving School Location Strategy

## Objetivo
Identificar los 3 destinos más seguros del mundo para abrir una escuela de buceo,
analizando el histórico global de ataques de tiburón.
La selección se basa en la tasa de fatalidad por país y el volumen de ataques,
con el fin de minimizar el riesgo para los futuros estudiantes.

---

## Dataset

| | |
|---|---|
| **Fuente** | Global Shark Attack File (GSAF) — registro histórico real |
| **Registros originales** | 78.395 filas × 15 columnas |
| **Registros tras limpieza** | ~4.017 filas útiles |
| **Cobertura** | Histórico global hasta 2026 |

### Variables principales

| Variable | Tipo | Descripción |
|---|---|---|
| `country` | Categórica | País donde ocurrió el ataque |
| `state` | Categórica | Estado o región |
| `location` | Categórica | Lugar específico |
| `activity` | Categórica | Actividad de la víctima |
| `age` | Numérica | Edad de la víctima |
| `injury` | Texto | Descripción de la herida |
| `species` | Categórica | Especie de tiburón |
| `fatal` | Booleana | Si el ataque fue mortal (derivada de `injury`) |
| `age_range` | Categórica | Rango de edad (`<18`, `18-25`, `26-35`...) |

---

## Proceso de Análisis

### Día 1 — EDA
- Carga e inspección del dataset (`shape`, `info`, `describe`)
- Eliminación de columnas vacías (columnas 15 en adelante)
- Identificación de columnas clave y clasificación de variables

### Día 2 — Data Cleaning
- **Nulos:** eliminación de filas sin `country` ni `injury`; imputación con `'Unknown'` en columnas no críticas
- **Duplicados:** `drop_duplicates()` + `reset_index()`
- **Strings:** `str.lower()`, `str.strip()`, `str.title()` en todas las columnas de texto
- **Regex:** extracción del primer número válido de `age` con `re.search(r'\d+', valor)`
- **Formato:** `astype(int)` en `age`; rangos de edad con `pd.cut()`
- **Columna `fatal`:** `str.contains('fatal', case=False)` sobre `injury`

### Día 3 — Análisis y Resultados
- Unificación de variantes de país (`USA`, `U.S.A.` → `UNITED STATES`)
- Categorización de actividades (`Diving`, `Surfing`, `Swimming`, `Fishing`, `Boating`, `Other`)
- KPIs calculados por país:
  - `total_attacks` — volumen total de ataques
  - `fatal_attacks` — ataques mortales
  - `fatal_rate` — proporción de ataques fatales
- Filtro de representatividad: mínimo 10 ataques por país
- Visualización con gráfico de barras

---

## Resultados

- El **17%** de los ataques registrados fueron fatales
- El rango de edad más afectado es **18-25 años** (1.078 casos)
- La actividad con más ataques es **Surfing**, pero **Diving** tiene menor tasa de fatalidad
- Los **3 países menos peligrosos** con suficiente volumen de registros se obtienen ordenando por `fatal_rate` ascendente

---

## Próximos Pasos

- Incorporar datos de **estacionalidad** (meses con más ataques) para recomendar temporadas seguras
- Añadir análisis de **especie** por país para identificar el tipo de tiburón predominante
- Cruzar con datos de **turismo de buceo** para validar viabilidad de negocio
- Ampliar con datos de **temperatura del agua** como variable predictiva

---

## Cómo Replicar el Proyecto

1. Clona el repositorio:
```bash
git clone https://github.com/roizherrerapilar-hub/Mini-project---Shark-Attacks
```
2. Instala las dependencias:
```bash
pip install pandas matplotlib
```
3. Abre y ejecuta `Notebook.ipynb` en orden desde el Día 1

