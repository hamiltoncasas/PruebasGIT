# PruebasGIT123
Uso para pruebas iniciales

## 🌿 Gestión de Items Jerárquicos

El repositorio incluye un sistema para crear issues con jerarquía:

**Epica > Feature > Historia De Usuario > Tarea**
(Bug está al mismo nivel que Tarea)

### ➜ [✨ ABRIR CREADOR VISUAL CON FILTRADO AUTOMÁTICO DEL PADRE](https://hamiltoncasas.github.io/PruebasGIT/crear-item.html)

Al seleccionar el **Nivel**, el campo **Padre** se llena automáticamente **solo con los issues del nivel inmediatamente superior**:
- **Feature** → solo Epicas
- **Historia De Usuario** → solo Features
- **Tarea / Bug** → solo Historias de Usuario
- **Epica** → sin padre

La app consulta los issues abiertos en tiempo real y abre el formulario de GitHub pre-llenado en la misma pestaña.

> **Importante (GitHub Pages):** el creador visual vive en `.github/crear-item.html` y se publica automáticamente vía GitHub Actions (`deploy-pages.yml`) cuando se suben cambios. Para que funcione la URL, habilita GitHub Pages en el repositorio:
> **Settings → Pages → Source: "GitHub Actions"** (seleccionar Actions como proveedor).
> La URL será `https://<tu-usuario>.github.io/PruebasGIT/crear-item.html`

### 🗂️ Formulario nativo de GitHub
También se puede usar el formulario estándar de issues ("Nuevo Item Jerárquico"), que incluye un dropdown **Padre** cuyas opciones muestran el nivel entre paréntesis:
`(Epica) #13 - Título`, `(Feature) #12 - Título`, `(Historia De Usuario) #15 - Título`.

### 🤖 Automatizaciones (GitHub Actions)
- **Procesar Jerarquía de Issue**: al abrir un issue, asigna etiqueta según nivel, valida el padre, crea la relación `parent-N`, y agrega al Project v2 el issue **y todos los issues que estén por encima**.
- **Sincronizar Plantilla de Items**: actualiza automáticamente las opciones del dropdown "Padre" con los issues existentes (se ejecuta con cada push o cambio de issues).
- **Deploy GitHub Pages**: publica el creador visual de `.github/crear-item.html` en el sitio.