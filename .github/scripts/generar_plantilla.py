#!/usr/bin/env python3
"""Genera el contenido YAML de la plantilla 'Nuevo Item Jerárquico' poblado
con los issues existentes de cada nivel (Epica, Feature, Historia de Usuario).

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


def opciones(items, vacio):
    """Genera las líneas YAML de opciones para un dropdown (8 espacios de indentación)."""
    if not items:
        return ["        - '" + vacio + "'"]
    vistos = set()
    resultado = []
    for item in items:
        n = item.get('number')
        if n in vistos:
            continue
        vistos.add(n)
        titulo = item.get('title') or ''
        if len(titulo) > 80:
            titulo = titulo[:77] + '...'
        titulo_limpio = titulo.replace("'", "").replace('"', '')
        resultado.append("        - '#" + str(n) + " - " + titulo_limpio + "'")
        if len(resultado) >= 100:
            break
    return resultado


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        print('ERROR: No se pudo leer el JSON desde stdin.', file=sys.stderr)
        sys.exit(1)

    epicas = opciones(
        data.get('epicas', []),
        '(Aún no hay Epicas. Crea una Epica primero.)'
    )
    features = opciones(
        data.get('features', []),
        '(Aún no hay Features. Crea un Feature primero.)'
    )
    historias = opciones(
        data.get('historias', []),
        '(Aún no hay Historias de Usuario. Crea una Historia primero.)'
    )

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
        '        > Selecciona **SOLO** el campo de padre que corresponde a tu nivel:\n'
        '        > - **Feature** → usa **Padre (Epica)**\n'
        '        > - **Historia De Usuario** → usa **Padre (Feature)**\n'
        '        > - **Tarea** → usa **Padre (Historia de Usuario)**\n'
        '        > - **Bug** → usa **Padre (Historia de Usuario)**\n'
        '        >\n'
        '        > La lista de opciones se genera automáticamente con los issues existentes\n'
        '        > de cada nivel. Si no aparece el padre que necesitas, créalo primero.\n'
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
        '    id: padre_epica\n'
        '    attributes:\n'
        '      label: "Padre (Epica)"\n'
        '      description: "Para nivel Feature. Elige la Epica superior."\n'
        '      options:\n'
        + '\n'.join(epicas) + '\n'
        '    validations:\n'
        '      required: false\n'
        '\n'
        '  - type: dropdown\n'
        '    id: padre_feature\n'
        '    attributes:\n'
        '      label: "Padre (Feature)"\n'
        '      description: "Para nivel Historia De Usuario. Elige el Feature superior."\n'
        '      options:\n'
        + '\n'.join(features) + '\n'
        '    validations:\n'
        '      required: false\n'
        '\n'
        '  - type: dropdown\n'
        '    id: padre_historia\n'
        '    attributes:\n'
        '      label: "Padre (Historia de Usuario)"\n'
        '      description: "Para nivel Tarea o Bug. Elige la Historia de Usuario superior."\n'
        '      options:\n'
        + '\n'.join(historias) + '\n'
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