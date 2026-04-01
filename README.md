# RiskLab · USTA
**Proyecto Integrador — Teoría del Riesgo**  
Universidad Santo Tomás · Facultad de Estadística  
Docente: Javier Mauricio Sierra  

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Decisiones de Diseño](#decisiones-de-diseño)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Portafolio de Activos](#portafolio-de-activos)
5. [APIs y Datos](#apis-y-datos)
6. [Estructura del Proyecto](#estructura-del-proyecto)
7. [Instalación y Ejecución](#instalación-y-ejecución)
8. [Arquitectura del Código](#arquitectura-del-código)
9. [Módulo 1 · Análisis Técnico](#módulo-1--análisis-técnico)
10. [Módulo 2 · Rendimientos](#módulo-2--rendimientos)
11. [Módulo 3 · ARCH / GARCH](#módulo-3--arch--garch)
12. [Módulo 4 · CAPM y Beta](#módulo-4--capm-y-beta)
13. [Módulos Pendientes](#módulos-pendientes)
14. [Despliegue en la Nube](#despliegue-en-la-nube)
15. [Uso de IA](#uso-de-ia)
16. [Bibliografía](#bibliografía)

---

## Descripción General

**RiskLab** es un tablero interactivo de análisis de riesgo financiero desarrollado como Proyecto Integrador para la asignatura Teoría del Riesgo de la Universidad Santo Tomás. El objetivo es construir una herramienta profesional que permita analizar un portafolio de acciones del S&P 500 a través de ocho módulos que cubren desde el análisis técnico básico hasta la optimización de portafolio y el modelado de volatilidad condicional.

El tablero consume datos **en tiempo real** desde Yahoo Finance, sin necesidad de datasets estáticos ni archivos CSV. Cada vez que el usuario selecciona un activo o ajusta un parámetro, los datos se descargan directamente desde la API y los cálculos se ejecutan sobre los datos más recientes disponibles.

---

## Decisiones de Diseño

### ¿Por qué Dash y no Streamlit, Shiny, Power BI o Looker Studio?

Se evaluaron todas las opciones disponibles antes de tomar la decisión:

| Herramienta | Calidad visual | APIs financieras | GARCH/VaR | Despliegue gratis |
|-------------|---------------|-----------------|-----------|------------------|
| **Dash** | ⭐⭐⭐⭐⭐ | ✅ | ✅ | ✅ Render |
| Streamlit | ⭐⭐⭐ | ✅ | ✅ | ✅ Streamlit Cloud |
| Shiny (R) | ⭐⭐⭐⭐ | ✅ | ✅ rugarch | ✅ shinyapps.io |
| Bokeh | ⭐⭐⭐⭐ | ✅ | ✅ | ⚠️ Complejo |
| Power BI | ⭐⭐⭐ | ❌ | ❌ | ❌ De pago |
| Looker Studio | ⭐⭐ | ❌ | ❌ | ✅ |

**Power BI y Looker Studio fueron descartados** porque no permiten implementar modelos estadísticos como GARCH, VaR por Montecarlo o la optimización de Markowitz. Son herramientas de visualización no-code que no pueden ejecutar código Python o R arbitrario.

**Dash fue elegido** porque ofrece la mayor calidad visual gracias al control total sobre CSS y los componentes de Plotly, usa las mismas librerías Python que se necesitan para los cálculos financieros (`arch`, `scipy`, `pypfopt`), y puede desplegarse gratuitamente en Render, lo que aplica para la bonificación del proyecto.

### ¿Por qué Python y no R?

Aunque el profesor usa R Markdown en clase, Python fue seleccionado porque la librería `arch` para modelos GARCH es más madura en cuanto a integración con aplicaciones web, `yfinance` es la forma más directa de consumir datos de Yahoo Finance sin API key, `pypfopt` ofrece optimización de portafolio de Markowitz lista para usar, y Dash es nativo de Python, eliminando la fricción de integrar R con una aplicación web.

### ¿Por qué solo Yahoo Finance?

El proyecto recomienda varias APIs (Alpha Vantage, Finnhub, FRED, Banco de la República, Polygon.io). Se decidió usar **únicamente Yahoo Finance** porque es gratuita y sin API key, elimina el riesgo de que la key expire o se agoten los límites durante la sustentación, cubre todo el proyecto incluyendo el ticker `^IRX` para la tasa libre de riesgo, y el sistema incluye fallback automático si cualquier descarga falla.

---

## Stack Tecnológico

| Componente | Librería / Versión | Uso |
|-----------|-------------------|-----|
| Framework web | `dash 2.17.1` | Estructura de la aplicación y callbacks |
| Componentes UI | `dash-bootstrap-components 1.6.0` | Tema oscuro base |
| Gráficos | `plotly 5.22.0` | Todos los gráficos interactivos |
| Datos | `pandas 2.2.2` | Manipulación de series temporales |
| Álgebra | `numpy 1.26.4` | Cálculos matriciales y estadísticos |
| API de mercado | `yfinance 0.2.40` | Precios y tasa libre de riesgo |
| Modelos GARCH | `arch 7.0.0` | ARCH(1), GARCH(1,1), GJR-GARCH |
| Estadística | `scipy 1.13.1` | Pruebas de normalidad, regresión lineal |
| Diagnóstico | `statsmodels 0.14.2` | Prueba ARCH-LM (het_arch) |
| Optimización | `pypfopt 1.5.5` | Frontera eficiente de Markowitz |
| Tipografía | Google Fonts | Syne (títulos) + DM Mono (datos numéricos) |
| Iconos | Font Awesome 6.5 | Iconos del sidebar de navegación |

---

## Portafolio de Activos

Se seleccionaron **cinco acciones del S&P 500** de sectores distintos, cumpliendo el requisito de "distintos sectores o geografías":

| Ticker | Empresa | Sector | Justificación de la selección |
|--------|---------|--------|-------------------------------|
| `AAPL` | Apple Inc. | Tecnología | Mayor empresa por capitalización bursátil. Alta liquidez, datos perfectos, beta históricamente alto |
| `JPM` | JPMorgan Chase | Financiero | Banco más grande de EE.UU. Muy sensible a tasas de interés y ciclos económicos |
| `XOM` | ExxonMobil | Energía | Mayor empresa de petróleo del mundo. Alta correlación con el precio del crudo, sector muy diferente a tecnología |
| `JNJ` | Johnson & Johnson | Salud | Sector defensivo. Beta históricamente bajo. Buen contraste con activos agresivos para Markowitz |
| `AMZN` | Amazon.com | Consumo discrecional | Empresa de alto crecimiento con volatilidad mayor, útil para ilustrar modelos GARCH y efectos de apalancamiento |
| `^GSPC` | S&P 500 | Benchmark | Índice de referencia para CAPM (Módulo 4) y comparación de rendimiento (Módulo 8). No forma parte del portafolio |

**Horizonte histórico:** 3 años de datos diarios, lo que supera el mínimo requerido de 2 años. Se eligieron 3 años para incluir el ciclo post-COVID, la crisis de tasas de 2022 y la recuperación de 2023–2024, enriqueciendo el análisis de volatilidad condicional y el cálculo de VaR.

---

## APIs y Datos

### Yahoo Finance — Precios históricos

La librería `yfinance` descarga datos directamente desde Yahoo Finance sin requerir API key ni registro. Se usa para descargar precios de cierre ajustados (OHLCV) de los 5 activos y el benchmark, y el ticker `^IRX` para la tasa libre de riesgo (T-Bill 3 meses en % anualizado).

### Tasa Libre de Riesgo — ^IRX

El ticker `^IRX` representa el rendimiento del T-Bill del Tesoro de EE.UU. a 3 meses, expresado como tasa anualizada en porcentaje. Es el proxy estándar de la tasa libre de riesgo en modelos CAPM para activos en USD.

El proceso de obtención es: descargar `^IRX` con `yfinance`, tomar el último valor disponible, dividir entre 100 para convertir a decimal, dividir entre 252 para obtener la tasa diaria, y si falla, usar automáticamente **5.25%** como referencia.

### Sistema de Caché en Memoria

Para respetar los rate limits de Yahoo Finance y mejorar el rendimiento, se implementó un caché en memoria en `data/loader.py`. Los datos se almacenan en un diccionario `_cache` con timestamp, cada entrada expira después de **30 minutos**, y antes de cada descarga se verifica si los datos en caché siguen vigentes.

### Reintentos con Backoff Exponencial

Cuando una descarga falla, el sistema reintenta hasta **3 veces**:
```
Intento 1 → falla → espera 2 segundos
Intento 2 → falla → espera 4 segundos  
Intento 3 → falla → espera 8 segundos → lanza ConnectionError
```

---

## Estructura del Proyecto

```
risklab/
│
├── app.py                  # Punto de entrada: inicializa Dash, CSS global,
│                           # sidebar de navegación y routing entre páginas
│
├── requirements.txt        # Dependencias con versiones fijas
├── README.md               # Este archivo
│
├── data/
│   ├── __init__.py         # Exporta funciones públicas del módulo de datos
│   └── loader.py           # Módulo central de datos:
│                           #   get_prices()         → precios históricos
│                           #   get_returns()        → log o simple
│                           #   get_risk_free_rate() → ^IRX con fallback
│                           #   caché 30 min + reintentos automáticos
│
└── pages/
    ├── __init__.py
    ├── m1_technical.py     # Módulo 1: Análisis Técnico
    ├── m2_returns.py       # Módulo 2: Rendimientos y propiedades empíricas
    ├── m3_garch.py         # Módulo 3: Modelos ARCH/GARCH
    └── m4_capm.py          # Módulo 4: CAPM y Beta
```

---

## Instalación y Ejecución

### Requisitos previos
- Python 3.10 o superior
- Conexión a internet (para descarga de datos en tiempo real)

### Paso 1 — Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/risklab-usta.git
cd risklab-usta
```

### Paso 2 — Crear entorno virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac / Linux
python -m venv .venv
source .venv/bin/activate
```

### Paso 3 — Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4 — Ejecutar el tablero
```bash
python app.py
```

Abrir el navegador en **http://localhost:8050**

> **No se requiere ninguna API key ni archivo .env.** Todos los datos se obtienen automáticamente desde Yahoo Finance.

### Navegación

| URL | Módulo |
|-----|--------|
| `localhost:8050/m1` | Análisis Técnico |
| `localhost:8050/m2` | Rendimientos |
| `localhost:8050/m3` | ARCH / GARCH |
| `localhost:8050/m4` | CAPM & Beta |

---

## Arquitectura del Código

### app.py — Routing y Sidebar

`app.py` inicializa Dash con el tema oscuro de Bootstrap y las fuentes de Google, define el CSS global como string de Python que se inyecta en el HTML (estilos del sidebar, cards, chips, scrollbar y clases de utilidad), y maneja el routing: el callback `route()` escucha cambios en la URL y carga el `layout` del módulo correspondiente desde su archivo en `pages/`.

El sidebar se construye dinámicamente desde una lista `NAV` que define cada elemento con su ícono de Font Awesome, etiqueta, ruta y badge (porcentaje de nota o "NEW" para módulos nuevos).

### data/loader.py — Módulo de Datos

Todos los módulos importan sus datos desde `data/loader.py`, nunca llaman directamente a `yfinance`. Esto centraliza la lógica de descarga, caché y manejo de errores en un solo lugar. Las tres funciones principales son `get_prices()`, `get_returns()` y `get_risk_free_rate()`.

### Patrón de cada módulo en pages/

Cada archivo sigue el mismo patrón: constantes de color, configuración base de Plotly (`PLOT_BASE`), funciones de datos, funciones de gráficos (cada una retorna un `go.Figure`), componentes UI helper (`card()`, `chip()`, etc.), la variable `layout` con la estructura visual completa, y los callbacks decorados con `@callback`.

---

## Módulo 1 · Análisis Técnico

**Ruta:** `/m1` | **Peso en nota:** 12%

### Objetivo

Permitir explorar el comportamiento histórico de cada activo con indicadores técnicos interactivos y parámetros ajustables en tiempo real, con datos descargados dinámicamente desde Yahoo Finance.

### Controles disponibles

El módulo tiene un panel de controles con selector de activo (dropdown con los 5 tickers), toggle entre gráfico de línea y velas japonesas, selector de rango de fechas, y cuatro sliders para ajustar los períodos de SMA 1 (5–200 días), SMA 2 (5–200 días), EMA (5–100 días) y RSI (7–30 días). Los labels de los sliders se actualizan en tiempo real mostrando el valor seleccionado.

### Indicadores implementados

**SMA — Media Móvil Simple**

Promedia los precios de cierre de los últimos N períodos con igual peso. Es el indicador de tendencia más básico.

```
SMA(N)ₜ = (Pₜ + Pₜ₋₁ + ... + Pₜ₋ₙ₊₁) / N
```

Un cruce de la SMA corta sobre la SMA larga se denomina **Golden Cross** y es señal alcista. El cruce inverso se llama **Death Cross** y anticipa caídas.

**EMA — Media Móvil Exponencial**

Pondera más los datos recientes mediante un factor de suavizamiento `α = 2/(N+1)`. Reacciona más rápido a los cambios de precio que la SMA.

```
EMA(N)ₜ = Pₜ × α + EMA(N)ₜ₋₁ × (1 - α),   α = 2/(N+1)
```

**Bandas de Bollinger**

Construidas alrededor de la SMA(20) usando la desviación estándar de los últimos 20 períodos. Se expanden cuando la volatilidad aumenta y se contraen cuando disminuye.

```
Banda superior = SMA(20) + 2σ(20)
Banda media    = SMA(20)
Banda inferior = SMA(20) - 2σ(20)
```

Precio tocando banda superior → posible sobrecompra. Precio tocando banda inferior → posible sobreventa. El **Bollinger Squeeze** (bandas muy estrechas) anticipa movimiento brusco inminente.

**RSI — Relative Strength Index**

Oscilador entre 0 y 100 que mide velocidad y magnitud de cambios de precio. Desarrollado por J. Welles Wilder (1978).

```
RS      = Ganancia media N períodos / Pérdida media N períodos
RSI     = 100 - 100 / (1 + RS)
```

RSI > 70 → sobrecompra. RSI < 30 → sobreventa. Período estándar: 14 días.

**MACD — Moving Average Convergence Divergence**

Mide diferencia entre dos EMAs para capturar cambios de momentum. Desarrollado por Gerald Appel (1979).

```
MACD       = EMA(12) - EMA(26)
Señal      = EMA(9) del MACD
Histograma = MACD - Señal
```

Cruce del MACD sobre la señal → señal alcista. El histograma muestra la fuerza del momentum con colores verde (positivo) y rojo (negativo).

**Oscilador Estocástico**

Compara el precio de cierre con el rango High-Low de los últimos K períodos. Desarrollado por George Lane (1950s).

```
%K = 100 × (Cierre - Mínimo_K) / (Máximo_K - Mínimo_K)
%D = SMA(3) de %K
```

%K > 80 → sobrecompra. %K < 20 → sobreventa. Cruce de %K sobre %D en zonas extremas genera señales de entrada.

### Implementación técnica

Todos los indicadores se calculan en Python puro sobre `pd.Series` sin librerías externas de indicadores técnicos. El gráfico principal superpone precio, SMA, EMA y Bollinger en la misma figura. RSI, MACD y Estocástico se grafican en figuras separadas. Las velas usan `#00D4AA` para días alcistas y `#FF6B6B` para bajistas.

---

## Módulo 2 · Rendimientos

**Ruta:** `/m2` | **Peso en nota:** 8%

### Objetivo

Caracterizar estadísticamente los rendimientos de cada activo, verificar formalmente si siguen una distribución normal e identificar los hechos estilizados de los mercados financieros.

### Tipos de rendimiento

El módulo ofrece toggle entre dos tipos:

```
Rendimiento simple:   rₜ = (Pₜ - Pₜ₋₁) / Pₜ₋₁
Log-rendimiento:      rₜ = ln(Pₜ / Pₜ₋₁)
```

Los log-rendimientos son preferidos porque son aditivos en el tiempo, aproximadamente simétricos, y facilitan el cálculo de estadísticas como la varianza anualizada. La conversión de volatilidad diaria a anual usa el factor √252 (días de trading en un año).

### Estadísticas descriptivas

Se calculan y muestran 9 estadísticos en chips de color en tiempo real:

| Estadístico | Fórmula | Color |
|------------|---------|-------|
| Media diaria | μ = Σrₜ/N | Verde si positiva, rojo si negativa |
| Media anualizada | μ × 252 | Verde si positiva |
| Desv. Std. diaria | σ = √(Σ(rₜ-μ)²/N) | Gris |
| Desv. Std. anual | σ × √252 | Gris |
| Asimetría | E[(r-μ)³]/σ³ | Dorado |
| Curtosis exceso | E[(r-μ)⁴]/σ⁴ - 3 | Rojo si \|K\|>3 |
| Mínimo | min(rₜ) | Gris |
| Máximo | max(rₜ) | Gris |
| N observaciones | len(r) | Gris |

### Visualizaciones

**Histograma con curva normal:** El histograma de frecuencias se superpone con la densidad de una distribución normal con la misma media y desviación estándar. La brecha visible en las colas evidencia la no-normalidad.

**Q-Q Plot:** Grafica cuantiles empíricos vs cuantiles teóricos de la normal. Si los datos fueran normales, todos los puntos caerían sobre la línea diagonal. Las desviaciones en los extremos confirman colas pesadas.

**Rendimientos² (Agrupamiento de volatilidad):** Al graficar rₜ² en el tiempo, los valores altos se concentran en ciertos períodos, evidenciando que la volatilidad no es constante. Esta es la motivación directa para los modelos GARCH del Módulo 3.

**Boxplot comparativo:** Muestra la distribución de log-rendimientos de los 5 activos simultáneamente, con colores predefinidos para cada ticker, facilitando comparación de mediana, dispersión y outliers entre activos.

### Pruebas de normalidad

**Jarque-Bera:** Basada en asimetría (S) y curtosis (K), especialmente potente para detectar colas pesadas.

```
JB = N/6 × (S² + K²/4)
H₀: distribución normal,   Rechazo si p-valor < 0.05
```

**Shapiro-Wilk:** Prueba general de normalidad aplicada sobre muestra de hasta 5.000 observaciones.

```
H₀: muestra proviene de distribución normal,   Rechazo si p-valor < 0.05
```

En series financieras, ambas pruebas rechazan H₀ casi siempre debido a colas pesadas y asimetría. Esto implica que el VaR paramétrico del Módulo 5 subestimará el riesgo real si asume normalidad, y que los modelos GARCH deberían usar distribución t-Student.

### Hechos estilizados

1. **Colas pesadas:** Curtosis de exceso positiva → eventos extremos más frecuentes de lo que predice la normal.
2. **Agrupamiento de volatilidad:** Períodos de alta volatilidad se agrupan. Motivación directa para GARCH.
3. **Asimetría negativa:** Los mercados caen más rápido de lo que suben. Pérdidas grandes más probables que ganancias equivalentes.
4. **Efecto apalancamiento:** Caídas del precio aumentan la volatilidad más que subidas de igual magnitud. Genera correlación negativa entre rendimientos pasados y volatilidad futura.

---

## Módulo 3 · ARCH / GARCH

**Ruta:** `/m3` | **Peso en nota:** 12%

### Objetivo

Modelar la volatilidad condicional de los activos para capturar el agrupamiento de volatilidad evidenciado en el Módulo 2. Comparar tres especificaciones y seleccionar la mejor según criterios de información.

### Justificación — Prueba ARCH-LM

Antes de ajustar cualquier modelo, se verifica formalmente la existencia de heterocedasticidad condicional mediante la **prueba ARCH-LM** de Engle (1982), implementada con `statsmodels.stats.diagnostic.het_arch` (se eligió statsmodels sobre `arch.tests.linear` por mayor estabilidad entre versiones).

```
εₜ² = α₀ + α₁εₜ₋₁² + ... + α₅εₜ₋₅² + υₜ

H₀: α₁ = ... = α₅ = 0  (no hay efecto ARCH)
Rechazo H₀ si p-valor < 0.05  → justifica usar GARCH
```

### Los tres modelos

**ARCH(1) — AutoRegressive Conditional Heteroskedasticity (Engle, 1982)**

```
σₜ² = ω + α₁εₜ₋₁²
Parámetros: ω > 0, α₁ ≥ 0
```

Modelo base. La varianza condicional depende únicamente del cuadrado del error anterior. Limitado por no tener memoria larga de la volatilidad.

**GARCH(1,1) — Generalized ARCH (Bollerslev, 1986)**

```
σₜ² = ω + α₁εₜ₋₁² + β₁σₜ₋₁²
Persistencia: α₁ + β₁  (debe ser < 1 para estacionariedad)
Vol. largo plazo: σ² = ω / (1 - α₁ - β₁)
```

Estándar de la industria para volatilidad diaria. Añade la varianza condicional del período anterior, capturando persistencia de la volatilidad.

**GJR-GARCH(1,1,1) — Glosten, Jagannathan y Runkle (1993)**

```
σₜ² = ω + α₁εₜ₋₁² + γ₁εₜ₋₁² × 𝟙(εₜ₋₁ < 0) + β₁σₜ₋₁²

Buenas noticias (εₜ₋₁ > 0): impacto = α₁
Malas noticias  (εₜ₋₁ < 0): impacto = α₁ + γ₁
```

Si γ₁ > 0, las malas noticias tienen mayor impacto → efecto apalancamiento confirmado.

### Comparación de modelos — AIC y BIC

```
AIC = -2 × LogL + 2k
BIC = -2 × LogL + k × ln(N)
```

Menor AIC → mejor balance ajuste/parsimonia. El BIC penaliza más los parámetros adicionales. El mejor modelo por AIC se marca automáticamente en la tabla con ★.

### Diagnóstico de residuos

Los residuos estandarizados (εₜ/σₜ) de un modelo bien especificado deben comportarse como ruido blanco. Se grafican en serie temporal y Q-Q plot, y se aplica Jarque-Bera sobre ellos. Si p-valor < 0.05, los residuos aún tienen colas pesadas, sugiriendo usar distribución t-Student en el modelo.

### Pronóstico de volatilidad

El pronóstico N-pasos se obtiene con `res.forecast(horizon=N)`. Para GARCH(1,1):

```
σ²ₜ₊₁|ₜ = ω + α₁εₜ² + β₁σₜ²
σ²ₜ₊ₕ|ₜ → ω/(1-α₁-β₁) cuando h → ∞  (reversión a la media)
```

El horizonte es ajustable via slider (5–60 días). La banda de incertidumbre de ±10% alrededor del pronóstico puntual comunica la incertidumbre de la estimación.

Los rendimientos se expresan en % (multiplicados por 100) para la librería `arch`, que requiere esta escala para la estabilidad numérica del algoritmo de estimación por máxima verosimilitud.

---

## Módulo 4 · CAPM y Beta

**Ruta:** `/m4` | **Peso en nota:** 8%

### Objetivo

Cuantificar el riesgo sistemático de cada activo mediante Beta y estimar su rendimiento esperado según el CAPM, con la tasa libre de riesgo obtenida automáticamente desde la API.

### Tasa libre de riesgo desde la API

```python
irx = yf.download("^IRX", period="5d")
rf_anual  = ultimo_valor / 100   # % → decimal
rf_diaria = rf_anual / 252       # tasa diaria
```

El banner en la parte superior del módulo siempre muestra la fuente, valor y fecha de la tasa usada. Si `^IRX` no está disponible, se usa automáticamente 5.25% con indicación de "Referencia manual".

### Cálculo del Beta por MCO

Beta se estima mediante regresión por Mínimos Cuadrados Ordinarios de los log-rendimientos diarios del activo sobre los log-rendimientos del S&P 500:

```
Rᵢ = α + β × Rm + εᵢ

β = Cov(Rᵢ, Rm) / Var(Rm)       ← implementado con scipy.stats.linregress
α = E[Rᵢ] - β × E[Rm]
```

Se reportan: Beta, Alpha anualizado (α × 252), R², p-valor de β y error estándar.

### Clasificación por Beta

| Condición | Clasificación | Significado |
|-----------|--------------|-------------|
| β > 1.2 | Agresivo | Amplifica movimientos del mercado |
| 0.8 ≤ β ≤ 1.2 | Neutro | Se mueve en línea con el mercado |
| β < 0.8 | Defensivo | Amortigua movimientos del mercado |

### Fórmula CAPM

```
E[Rᵢ] = Rf + βᵢ × (E[Rm] − Rf)

Rf       = Tasa libre de riesgo (^IRX desde Yahoo Finance)
E[Rm]    = Media histórica diaria del S&P 500 × 252 (anualizado)
E[Rm]-Rf = Prima de riesgo del mercado
```

### Security Market Line (SML)

La SML grafica el rendimiento esperado teórico para cualquier valor de Beta. Activos sobre la SML están subvalorados (ofrecen más retorno del que predice el CAPM); activos bajo la SML están sobrevalorados. Los 5 activos del portafolio se grafican sobre la SML junto con el punto Rf (β=0).

### Banda de confianza al 95% en la regresión

```
IC₉₅ = ŷ ± 1.96 × SE × √(1/N + (x - x̄)² / Σ(xᵢ - x̄)²)
```

Una banda estrecha indica estimación de Beta más precisa.

### Descomposición del riesgo

```
Var(Rᵢ)  = β² × Var(Rm)  +  Var(εᵢ)
           Riesgo sist.      Riesgo no-sist.

% Sist.     = β² × Var(Rm) / Var(Rᵢ) × 100
% No-sist.  = Var(εᵢ) / Var(Rᵢ) × 100
```

El riesgo sistemático no puede eliminarse por diversificación y es el que el CAPM recompensa. El riesgo no sistemático puede eliminarse combinando activos con baja correlación, por eso el CAPM no lo compensa con mayor retorno esperado.

---

## Módulos Pendientes

| Módulo | Ruta | Peso | Contenido planificado |
|--------|------|------|-----------------------|
| Módulo 5: VaR & CVaR | `/m5` | 12% | VaR paramétrico, histórico y Montecarlo + CVaR (Expected Shortfall) |
| Módulo 6: Markowitz | `/m6` | 12% | Frontera eficiente, portafolio mínima varianza y máximo Sharpe |
| Módulo 7: Señales ⭐ | `/m7` | 10% | Panel de alertas tipo semáforo por activo con umbrales configurables |
| Módulo 8: Macro ⭐ | `/m8` | 8% | Alpha de Jensen, Tracking Error, Information Ratio, máximo drawdown |

---

## Despliegue en la Nube

El tablero puede desplegarse gratuitamente en **Render** (aplica para la bonificación):

1. Crear cuenta en [render.com](https://render.com)
2. **New → Web Service → Connect a repository**
3. Seleccionar el repositorio de GitHub
4. Configurar:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:server`
   - **Environment:** Python 3
5. El tablero queda disponible en `https://risklab-xxxx.onrender.com`

No se necesitan variables de entorno ya que no se usan API keys con autenticación.

---

## Uso de IA

Este proyecto fue desarrollado con asistencia de **Claude (Anthropic)** como herramienta de apoyo para la arquitectura del proyecto, implementación de cálculos estadísticos y financieros, diseño del sistema de caché, y revisión y corrección de bugs. De acuerdo con la política del proyecto, todo el código fue revisado y comprendido por los integrantes, y cada uno puede explicar y defender cualquier sección en la sustentación oral. La IA fue usada como **asistente**, no como sustituto del aprendizaje.

---

## Bibliografía

1. Moscote Flórez, O. *Elementos de estadística en riesgo financiero*. USTA, 2013.
2. Holton, G. A. *Value at Risk: Theory and Practice*. [value-at-risk.net](https://www.value-at-risk.net)
3. Markowitz, H. (1952). Portfolio Selection. *The Journal of Finance*, 7(1), 77–91.
4. Sharpe, W. F. (1964). Capital Asset Prices. *The Journal of Finance*, 19(3), 425–442.
5. Engle, R. F. (1982). Autoregressive Conditional Heteroscedasticity. *Econometrica*, 50(4), 987–1007.
6. Bollerslev, T. (1986). Generalized Autoregressive Conditional Heteroskedasticity. *Journal of Econometrics*, 31(3), 307–327.
7. Glosten, L., Jagannathan, R. y Runkle, D. (1993). On the Relation Between the Expected Value and the Volatility of the Nominal Excess Return on Stocks. *The Journal of Finance*, 48(5), 1779–1801.
8. Tsay, R. S. (2010). *Analysis of Financial Time Series*. 3rd ed., Wiley.
9. Hull, J. C. (2018). *Risk Management and Financial Institutions*. 5th ed., Wiley.
10. Material de clase: Notebooks R Markdown, Prof. Javier Mauricio Sierra — USTA.
