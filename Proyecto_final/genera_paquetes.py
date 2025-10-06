# generar_paquetes_300_final.py
# Genera 300 matrices llave y mensajes cifrados, exportando versión docente y versión alumno.

import json, random
from hill_3x3_gauss import package_for_student, pretty_matrix

carpeta = "frases/"
RUTA_FRASES = f"{carpeta}frases_300_motivacionales_v3.txt"
SALIDA_DOCENTE = f"{carpeta}paquetes_300_docente.json"
SALIDA_ALUMNOS = f"{carpeta}paquetes_300_alumnos.json"

# Leer frases y tipo (sin alterar longitud ni borrar espacios internos)
frases, tipos = [], []
with open(RUTA_FRASES, "r", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n\r")                     # quitar solo saltos de línea
        if "| " in line or "|" in line:
            left, _, tipo = line.partition("|")         # separa la frase del tipo
            frase = left.split(": ", 1)[1]              # elimina el índice inicial
            frases.append(frase)
            tipos.append(tipo.strip())

print(f"Se cargaron {len(frases)} frases (longitud promedio: {sum(len(f) for f in frases)/len(frases):.1f} caracteres).")

# Generar matrices llave e información cifrada
paquetes_docente, paquetes_alumnos = [], []

for i, frase in enumerate(frases, start=1):
    K, cipher = package_for_student(i, frase)
    tipo = tipos[i - 1] if i - 1 < len(tipos) else (
        "easter" if i <= 100 else ("celebre" if i <= 200 else "motivacional")
    )

    # Versión completa (docente)
    paquetes_docente.append({
        "id": i,
        "tipo": tipo,
        "frase_original": frase,
        "longitud": len(frase),
        "K": K,
        "cadena_cifrada": cipher
    })

    # Versión reducida (alumno)
    paquetes_alumnos.append({
        "id": i,
        "K": K,
        "cadena_cifrada": cipher
    })

    # Mostrar solo las primeras 3
    if i <= 3:
        print(f"\nAlumno {i:03d} ({tipo})")
        print("Longitud frase:", len(frase))
        print("Matriz K:\n", pretty_matrix(K))
        print("Primeros 15 números cifrados:", cipher[:15])

# Guardar ambos archivos
with open(SALIDA_DOCENTE, "w", encoding="utf-8") as f:
    json.dump(paquetes_docente, f, ensure_ascii=False, indent=2)

with open(SALIDA_ALUMNOS, "w", encoding="utf-8") as f:
    json.dump(paquetes_alumnos, f, ensure_ascii=False, indent=2)

print(f"\n✅ Archivos generados:\n  - {SALIDA_DOCENTE} (docente)\n  - {SALIDA_ALUMNOS} (alumnos)")