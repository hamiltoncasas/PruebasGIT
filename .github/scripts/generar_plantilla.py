#!/usr/bin/env python3
"""Genera el contenido YAML de la plantilla 'Nuevo Item Jerárquico'.

El formulario tiene UN SOLO dropdown "Padre" cuyas opciones muestran el
nivel entre paréntesis, por ejemplo:
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
    """Genera las líneas YAML de opciones para el dropdown 'Padre' (8 espacios).

    GitHub Forms exige un MÍNIMO de 2 opciones por dropdown."""
    resultado = []
    vistos = set()
    if con_nivel:
        for nivel, items in con_nivel:
            for item in items:
                n = item.get('number')
                if n in vistos:
                    continue
                vistos.add(n)
                titulo = item.get('title') or ''
                if len(titulo) > 80:
                    titulo = titulo[:77] + '...'
                titulo_limpio = titulo.replace("'", "").replace('"', '')
                resultado.append("        - '(" + nivel + ") #" + str(n) + " - " + titulo_limpio + "'")
                if len(resultado) >= 100:
                    break
            if len(resultado) >= 100:
                break
    # Garantizar mínimo 2 opciones (requisito de GitHub Forms)
    if not resultado:
        resultado = [
            "        - '(Crea primero el nivel superior para que aparezca aquí)'",
            "        - '(Crea más issues del nivel superior para ver más opciones)'"
        ]
    elif len(resultado) == 1:
        resultado.append("        - '(Crea más issues del nivel superior para ver más opciones)'")
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
    ops_padre = opciones(con_nivel)

    yml = (
        'name: "Nuevo Item Jerárquico"\n'
        'description: "Crea un item con su nivel y relación padre-hijo"\n'
        'title: "[Nivel] - Título"\n'
        'labels: ["needs-triage"]\n'
        'body:\n'
        '  - type: markdown\n'
        '    attributes:\n'
        '      value: |\n'
        '        ## Jerarquía: Epica > Feature > Historia De Usuario > Tarea\n'
        '\n'
        '        ### ➜ [✨ ABRIR CREADOR VISUAL CON FILTRADO AUTOMÁTICO DEL PADRE](https://hamiltoncasas.github.io/PruebasGIT/crear-item.html)\n'
        '        > _Seleccionas el Nivel y el campo Padre se llena solo con el nivel inmediatamente superior._\n'
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
        '      description: "Issue superior. Las opciones muestran el nivel entre paréntesis. Elegir solo el inmediatamente superior: Feature→(Epica), Historia→(Feature), Tarea/Bug→(Historia)"\n'
        '      options:\n'
        + '\n'.join(ops_padre) + '\n'
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