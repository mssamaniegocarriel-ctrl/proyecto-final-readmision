# Predicción de Readmisión Hospitalaria

**Proyecto Final — Ironhack Data Analytics Bootcamp**  
**Autora:** Melany Salomé Samaniego Carriel

---

## Objetivo del proyecto

Predecir si un paciente diabético será **readmitido en menos de 30 días** tras el alta hospitalaria, utilizando registros clínicos reales de 130 hospitales de EE.UU.

La readmisión temprana es un indicador clave de calidad asistencial y supone un alto coste para el sistema sanitario. Un modelo predictivo permite a los equipos médicos intervenir de forma preventiva en el momento del alta.

---

## Dataset

| Característica | Valor |
|----------------|-------|
| Fuente | UCI ML Repository — Diabetes 130-US Hospitals (1999–2008) |
| Muestras | 101.766 pacientes |
| Features | 49 (numéricas + categóricas) |
| Target | Readmisión en <30 días (binario) |
| Balance | Muy desbalanceado — ~11% positivos |
| Valores nulos | Codificados como `?` → convertidos a NaN |

---

## Proceso de análisis

### Notebook 1 — EDA
- Exploración inicial: shape, tipos de datos, valores únicos
- Creación del target binario: `readmitted_30`
- Análisis de valores faltantes (codificados como `?`)
- Visualización de variables categóricas y numéricas por target
- Matriz de correlación

### Notebook 2 — Limpieza y Feature Engineering
- Eliminación de columnas con >40% de nulos
- Eliminación de columnas ID y diagnóstico (>700 categorías)
- Encoding con `LabelEncoder`
- Train/Test Split 80/20 con `stratify=y`
- Estandarización con `StandardScaler` (fit solo en train)
- Reducción de dimensionalidad con `PCA` (95% varianza retenida)

### Notebook 3 — Modelado y Evaluación
- 4 modelos baseline: Logistic Regression, Decision Tree, Random Forest, Gradient Boosting
- `class_weight='balanced'` para compensar el desbalance
- Evaluación con Accuracy, F1-Score, ROC-AUC y Recall Positivo
- GridSearchCV en Random Forest y Gradient Boosting
- Modelo final seleccionado por ROC-AUC y Recall Positivo

---

## Resultados

| Modelo | Accuracy | F1-Score | ROC-AUC | Recall Positivo |
|--------|----------|----------|---------|-----------------|
| **Logistic Regression** | 0.6797 | 0.7365 | **0.6482** | **0.5038** |
| Gradient Boosting | 0.8899 | 0.8417 | 0.6446 | 0.0175 |
| Random Forest | 0.8898 | 0.8406 | 0.6173 | 0.0122 |
| Decision Tree | 0.8144 | 0.8152 | 0.5308 | 0.1672 |

### Modelo final: Logistic Regression

A pesar de tener menor Accuracy, **Logistic Regression** es el modelo con mejor **ROC-AUC (0.6482)** y **Recall Positivo (0.5038)**, que son las métricas prioritarias en este contexto clínico.

Random Forest y Gradient Boosting obtienen alta Accuracy pero un Recall Positivo casi nulo (~0.01), lo que significa que prácticamente no detectan pacientes readmitidos — el error más costoso en un entorno hospitalario.

---

## Estructura del repositorio

```
ProyectofinalReadmision/
├── notebooks/
│   ├── NB1_readmision_carga_exploracion.ipynb
│   ├── NB2_readmision_feature_engineering.ipynb
│   └── NB3_readmision_modelado.ipynb
├── data/
│   ├── readmision_raw.csv
│   ├── train_processed.csv
│   └── test_processed.csv
├── scripts/
│   ├── scaler.pkl
│   └── pca.pkl
└── README.md
```

---

## Cómo ejecutar el proyecto

### Requisitos
```bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib
```

### Orden de ejecución
```
1. NB1_readmision_carga_exploracion.ipynb
2. NB2_readmision_feature_engineering.ipynb
3. NB3_readmision_modelado.ipynb
```

---

## Tecnologías utilizadas

| Librería | Uso |
|----------|-----|
| `pandas` | Manipulación de datos |
| `numpy` | Operaciones numéricas |
| `scikit-learn` | Modelos ML, preprocesamiento, evaluación |
| `matplotlib` / `seaborn` | Visualización |
| `joblib` | Persistencia del modelo |

---

## Próximos pasos

- Probar técnicas de oversampling (SMOTE) para mejorar la detección de la clase positiva
- Explorar modelos como XGBoost o LightGBM optimizados para datasets desbalanceados
- Incorporar las columnas de diagnóstico (`diag_1`, `diag_2`, `diag_3`) con encoding adecuado
- Desplegar el modelo en una aplicación web con Streamlit
