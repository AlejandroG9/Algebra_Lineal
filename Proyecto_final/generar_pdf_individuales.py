# ======================================================
# Archivo: generar_pdf_individuales.py
# Genera un PDF por alumno con instrucciones, ejemplo y su proyecto cifrado.
# ======================================================

from pylatex import Document, Command, NoEscape
import json, os
import unicodedata
import re

os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"

# ----------------------------------------
# CONFIGURACIÓN DE RUTAS
# ----------------------------------------
RUTA_JSON = "frases/paquetes_300_docente.json"
RUTA_INSTRUCCIONES = "instrucciones_y_ejemplo.tex"
CARPETA_SALIDA = "Proyecto_final_individual/pdfs_alumnos"

os.makedirs(CARPETA_SALIDA, exist_ok=True)

# ----------------------------------------
# LECTURA DE ARCHIVOS
# ----------------------------------------
with open(RUTA_JSON, "r", encoding="utf-8") as f:
    paquetes = json.load(f)

with open(RUTA_INSTRUCCIONES, "r", encoding="utf-8") as f:
    instrucciones_y_ejemplo = f.read()

# ----------------------------------------
# FUNCIÓN PARA FORMATEAR MATRICES Y CADENAS
# ----------------------------------------
def formatear_matriz(K):
    return " \\\\\n".join([" & ".join(map(str, fila)) for fila in K])

def formatear_cadena(cifrado, por_linea=12):
    filas = []
    for i in range(0, len(cifrado), por_linea):
        chunk = " & ".join(map(str, cifrado[i:i+por_linea]))
        # Solo añade "\\" si no es la última línea
        if i + por_linea < len(cifrado):
            chunk += r" \\"
        filas.append(chunk)
    return "\n".join(filas)

def limpiar_texto(s):
    return s.replace("–", "-").replace("—", "-")



def limpiar_latex(s):
    """
    Limpia texto para evitar errores de compilación en LaTeX.
    - Elimina acentos y caracteres no ASCII
    - Escapa símbolos reservados: _, %, &, #, {, }, $
    - Sustituye guiones y comillas
    """
    import unicodedata, re
    if not isinstance(s, str):
        return ""

    # Normaliza acentos
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode()

    # Sustituye comillas y guiones largos
    s = s.replace("“", "\"").replace("”", "\"").replace("–", "-").replace("—", "-")

    # Escapa caracteres reservados de LaTeX
    for c in ["_", "%", "&", "#", "{", "}", "$"]:
        s = s.replace(c, f"\\{c}")

    # Quita caracteres fuera de rango ASCII o invisibles
    s = re.sub(r"[^\x20-\x7E]", "", s)

    return s.strip()

# ----------------------------------------
# GENERADOR DE BLOQUE DEL PROYECTO
# ----------------------------------------
def bloque_proyecto_tex(p):
    return rf"""
\newpage
\vspace{{0.5em}}
\noindent\textbf{{Proyecto {p['id']:03d}}}\\%\\[0.5cm]
\noindent\hrule
\vspace{{1em}}

\noindent\textbf{{Nombre del alumno:}} \underline{{\hspace{{11.8cm}}}}\\[8pt]
\noindent\textbf{{Matrícula:}} \underline{{\hspace{{4cm}}}} 
\textbf{{Grupo:}} \underline{{\hspace{{1.9cm}}}}
\textbf{{Fecha de entrega:}} \underline{{\hspace{{2.5cm}}}}\\[12pt]

\textbf{{Matriz llave:}}
\[
K = \begin{{pmatrix}}
{formatear_matriz(p['K'])}
\end{{pmatrix}} \pmod{{29}}
\]

\textbf{{Cadena cifrada:}}
\begin{{center}}
$\begin{{array}}{{lllllllllllllll}}
{formatear_cadena(p['cadena_cifrada'])}
\end{{array}}$
\end{{center}}

\bigskip
\textbf{{Espacio para cálculos y observaciones:}}\\[6pt]
\rule{{\linewidth}}{{0.4pt}}\\[10pt]
\rule{{\linewidth}}{{0.4pt}}\\[10pt]
\rule{{\linewidth}}{{0.4pt}}\\[10pt]
\rule{{\linewidth}}{{0.4pt}}\\[10pt]
"""

# ----------------------------------------
# GENERACIÓN DE LOS PDF INDIVIDUALES
# ----------------------------------------

for p in paquetes:
    p["frase_original"] = limpiar_latex(p.get("frase_original", ""))
    nombre_pdf = os.path.join(CARPETA_SALIDA, f"Proyecto_{p['id']:03d}")
    doc = Document(nombre_pdf, documentclass="article")

    # ====== Configuración de márgenes ======
    doc.packages.append(NoEscape(r"\usepackage[a4paper, margin=2.5cm, headheight=16pt]{geometry}"))

    # ====== Tamaño de fuente ======
    doc.preamble.append(NoEscape(r"\renewcommand\normalsize{\fontsize{12}{14}\selectfont}"))
    doc.preamble.append(NoEscape(r"\normalsize"))
    doc.packages.append(NoEscape(r"\usepackage[spanish,es-noshorthands]{babel}"))
    doc.packages.append(NoEscape(r"\usepackage[T1]{fontenc}"))
    doc.packages.append(NoEscape(r"\usepackage{amsmath, amssymb, setspace, fancyhdr}"))
    doc.preamble.append(Command("pagestyle", "fancy"))
    doc.preamble.append(NoEscape(r"\fancyhf{}"))
    doc.preamble.append(NoEscape(r"\lhead{Facultad de Ingeniería Tampico – UAT}"))
    doc.preamble.append(NoEscape(r"\rhead{Proyecto Final de Álgebra Lineal}"))
    doc.preamble.append(NoEscape(r"\setlength{\headheight}{16pt}"))

    # Agregar instrucciones y ejemplo
    doc.append(NoEscape(instrucciones_y_ejemplo))

    # Agregar bloque del proyecto del alumno
    doc.append(NoEscape(bloque_proyecto_tex(p)))

    # Generar PDF individual
    # Guardar .tex manualmente en UTF-8 antes de compilar
    with open(nombre_pdf + ".tex", "w", encoding="utf-8") as tex_out:
        tex_out.write(doc.dumps())  # dump genera todo el código LaTeX del documento

    try:
        doc.generate_pdf(nombre_pdf, clean_tex=False)
        print(f"✅ Se genero {nombre_pdf} en: {CARPETA_SALIDA}/")
    except Exception as e:
        print(f"⚠️ Error al generar {nombre_pdf}.tex")

        # Intentamos decodificar de varias maneras
        salida = None
        if hasattr(e, "output") and e.output:
            for codec in ("utf-8", "latin-1", "cp1252"):
                try:
                    salida = e.output.decode(codec, errors="ignore")
                    break
                except Exception:
                    continue
        if salida:
            print(salida[:500])  # imprime solo el inicio del log
        else:
            print("No se pudo decodificar la salida del compilador (probablemente AppleRoman).")

print(f"✅ Se generaron {len(paquetes)} PDFs individuales en: {CARPETA_SALIDA}/")