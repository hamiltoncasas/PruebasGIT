# PruebasGIT123
Uso para pruebas iniciales

## 🌿 Gestión de Items Jerárquicos

El repositorio incluye un sistema para crear issues jerárquicos:

**Epica > Feature > Historia De Usuario > Tarea**
(Bug está al mismo nivel que Tarea)

### 📝 Formulario de creación de issues
Al crear un issue se usa el formulario **"Nuevo Item Jerárquico"**, que incluye:

- **Nivel** (combobox): Epica, Feature, Historia De Usuario, Tarea, Bug
- **Status** (combobox): Nuevo, En Progreso, En Revisión, Completado
- **Fechas**: Previsto Inicio/Fin y Real Inicio/Fin (formato `AAAA-MM-DD`)
- **Descripción**: detalle del item
- **Assignees**: el campo nativo de asignación de responsables (ya viene por defecto en GitHub)

> **Nota:** los campos de fecha son de texto con formato `AAAA-MM-DD` porque GitHub Issue Forms no tiene un selector de fecha nativo (usar `type: date` invalida el formulario).

### 🤖 Automatizaciones (GitHub Actions)
- **Procesar Jerarquía de Issue**: al abrir un issue, extrae los datos del formulario, asigna la etiqueta según el nivel (`epic`, `feature`, `user-story`, `task`, `bug`) y actualiza el campo **Nivel** en el Project v2.