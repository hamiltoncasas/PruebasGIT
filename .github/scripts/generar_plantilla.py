#!/usr/bin/env python3
"""Genera el contenido YAML de la plantilla 'Nuevo Item Jerárquico' con un
único combobox "Padre" cuyas opciones muestran el nivel entre paréntesis:
  (Epica) #1 - Título
  (Feature) #2 - Título
  (Historia De Usuario) #3 - Título

Recibe por stdin un JSON con la forma:
{
  "epicas":   [{"number": 1, "title": "..."}],
  "features": [{"number": 2, "title": "..."}],
  "historias":[{"number": 3, "title": "..."}]
}

E imprime por stdout el YAML completo de la plantilla.
"""
import json
import sys

if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def opciones(con_nivel):
    """Genera las líneas YAML de opciones para el dropdown 'Padre'."""
    if not con_nivel:
        return ["        - '(Sin padres creados aún. Crea primero el nivel superior para que aparezca aquí.)'"]
    vistos = set()
    resultado = []
    for nivel, items in con_nivel:
        for item in items:
            n = item.get('number')
            if n in vistos:
                continue
            vistos.add(n)
            titulo = item.get('title') or ''
            if len(titulo) > 70:
                titulo = titulo[:67] + '...'
            titulo_limpio = titulo.replace("'", "").replace('"', '')
            resultado.append("        - '(" + nivel + ") #" + str(n) + " - " + titulo_limpio + "'")
            if len(resultado) >= 100:
                return resultado
    return resultado


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        print('ERROR: No se pudo leer el JSON desde stdin.', file=sys.stderr)
        sys.exit(1)

    con_nivel = [
        ('Epica', data.get('epicas', [])),
        ('Feature', data.get('features', [])),
        ('Historia De Usuario', data.get('historias', [])),
    ]
    opciones_padre = opciones(con_nivel)

    yml = (
        'name: "Nuevo Item Jerárquico"\n'
        'description: "Crea un item con su nivel y relación padre-hijo"\n'
        'title: "[Nivel] - Título"\n'
        'labels: ["needs-triage"]\n'
        'body:\n'
        '  - type: markdown\n'
        '    attributes:\n'
        '      value: |\n'
        '        ## Selecciona el nivel y el padre (si aplica)\n'
        '        > **Importante:** Solo los items que NO son Epica necesitan un padre.\n'
        '        > **Jerarquía:** Epica > Feature > Historia De Usuario > Tarea (Bug está al mismo nivel que Tarea).\n'
        '        >\n'
        '        > **¿Cómo elegir el padre?** En el campo **"Padre"** cada opción\n'
        '        > muestra el nivel entre paréntesis: `(Epica) #1 - Título`,\n'
        '        > `(Feature) #2 - Título`, `(Historia De Usuario) #3 - Título`.\n'
        '        > Elige **solo** la opción cuyo nivel sea el **inmediatamente superior** al tuyo:\n'
        '        > - **Feature** → elige una opción `(Epica)`\n'
        '        > - **Historia De Usuario** → elige una opción `(Feature)`\n'
        '        > - **Tarea o Bug** → elige una opción `(Historia De Usuario)`\n'
        '        > - **Epica** → deja el padre vacío\n'
        '        >\n'
        '        > ⚠️ El formulario de GitHub no permite listas dinámicas: debes\n'
        '        > **crear primero el nivel superior** para que aparezca en la lista.\n'
        '        > La lista se actualiza automáticamente con cada issue creado.\n'
        '        >\n'
        '        > 💡 **Alternativa recomendada:** Si tu repositorio tiene habilitada la\n'
        '        > función "Sub-issues" (Settings → General → Issues), al crear el issue\n'
        '        > verás en el panel derecho el campo **Parent issue**, que es un buscador\n'
        '        > dinámico. Puedes usarlo en lugar del combobox de abajo si prefieres.\n'
        '        >\n'
        '        > El título del issue es obligatorio y debe reemplazar el placeholder.\n'
        '\n'
        '  - type: dropdown\n'
        '    id: nivel\n'
        '    attributes:\n'
        '      label: "Nivel"\n'
        '      description: "Elige el tipo de item"\n'
        '      options:\n'
        '        - Epica\n'
        '        - Feature\n'
        '        - Historia De Usuario\n'
        '        - Tarea\n'
        '        - Bug\n'
        '    validations:\n'
        '      required: true\n'
        '\n'
        '  - type: dropdown\n'
        '    id: padre\n'
        '    attributes:\n'
        '      label: "Padre"\n'
        '      description: "Selecciona el issue superior (su nivel aparece entre paréntesis). Aparece en la lista al crear primero el superior."\n'
        '      options:\n'
        + '\n'.join(opciones_padre) + '\n'
        '    validations:\n'
        '      required: false\n'
        '\n'
        '  - type: dropdown\n'
        '    id: status\n'
        '    attributes:\n'
        '      label: "Status"\n'
        '      description: "Selecciona el estado del item"\n'
        '      options:\n'
        '        - Nuevo\n'
        '        - En Progreso\n'
        '        - En Revisión\n'
        '        - Completado\n'
        '    validations:\n'
        '      required: false\n'
        '\n'
        '  - type: input\n'
        '    id: fecha_previsto_inicio\n'
        '    attributes:\n'
        '      label: "Fecha Previsto Inicio"\n'
        '      description: "Fecha estimada de inicio (formato: AAAA-MM-DD)"\n'
        '      placeholder: "AAAA-MM-DD"\n'
        '    validations:\n'
        '      required: false\n'
        '\n'
        '  - type: input\n'
        '    id: fecha_previsto_fin\n'
        '    attributes:\n'
        '      label: "Fecha Previsto Fin"\n'
        '      description: "Fecha estimada de término (formato: AAAA-MM-DD)"\n'
        '      placeholder: "AAAA-MM-DD"\n'
        '    validations:\n'
        '      required: false\n'
        '\n'
        '  - type: input\n'
        '    id: fecha_real_inicio\n'
        '    attributes:\n'
        '      label: "Fecha Real Inicio"\n'
        '      description: "Fecha real de inicio (formato: AAAA-MM-DD)"\n'
        '      placeholder: "AAAA-MM-DD"\n'
        '    validations:\n'
        '      required: false\n'
        '\n'
        '  - type: input\n'
        '    id: fecha_real_final\n'
        '    attributes:\n'
        '      label: "Fecha Real Final"\n'
        '      description: "Fecha real de término (formato: AAAA-MM-DD)"\n'
        '      placeholder: "AAAA-MM-DD"\n'
        '    validations:\n'
        '      required: false\n'
        '\n'
        '  - type: textarea\n'
        '    id: descripcion\n'
        '    attributes:\n'
        '      label: "Descripción"\n'
        '      description: "Detalla el contenido de este item"\n'
        '    validations:\n'
        '      required: false\n'
    )
    sys.stdout.write(yml)


if __name__ == '__main__':
    main()