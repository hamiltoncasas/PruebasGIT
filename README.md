# PruebasGIT123
Uso para pruebas iniciales

## 🌿 Gestión de Items Jerárquicos

El repositorio incluye un sistema para crear issues con jerarquía:

**Epica > Feature > Historia De Usuario > Tarea**
(Bug está al mismo nivel que Tarea)

### 📱 App web de creación con filtrado automático
Para crear un issue de forma visual y con **filtrado automático del padre** según el nivel:

👉 **https://hamiltoncasas.github.io/PruebasGIT/crear-item.html**

Al seleccionar el **Nivel**, el campo **Padre** se llena automáticamente **solo con los issues del nivel inmediatamente superior**:
- **Feature** → solo Epicas
- **Historia De Usuario** → solo Features
- **Tarea / Bug** → solo Historias de Usuario
- **Epica** → sin padre

La app consulta los issues abiertos en tiempo real y genera el enlace para crear el issue en GitHub con el formulario pre-llenado.

> **Nota sobre GitHub Pages:** si la URL anterior no funciona aún, habilita GitHub Pages en el repositorio:
> Settings → Pages → Source: `Deploy from a branch` → Branch: `main`/`master` + `/ (root)` → Save.
> La URL será `https://<tu-usuario>.github.io/PruebasGIT/crear-item.html`

### 🗂️ Formulario nativo de GitHub
También se puede usar el formulario estándar de issues ("Nuevo Item Jerárquico"), que incluye un dropdown **Padre** cuyas opciones muestran el nivel entre paréntesis:
`(Epica) #13 - Título`, `(Feature) #12 - Título`, `(Historia De Usuario) #15 - Título`.

### 🤖 Automatizaciones (GitHub Actions)
- **Procesar Jerarquía de Issue**: al abrir un issue, asigna etiqueta según nivel, valida el padre, crea la relación `parent-N`, y agrega al Project v2 el issue **y todos los issues que estén por encima**.
- **Sincronizar Plantilla de Items**: actualiza automáticamente las opciones del dropdown "Padre" con los issues existentes (se ejecuta con cada push o cambio de issues).