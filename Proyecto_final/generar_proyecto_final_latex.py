# generar_proyecto_final_latex_v2.py
# Proyecto Final de Álgebra Lineal con portada, introducción, instrucciones, ejemplo y formato por alumno

import json
from textwrap import wrap
from pathlib import Path

carpeta = "frases/"
ARCHIVO_ENTRADA = f"{carpeta}paquetes_300_alumnos.json"
ARCHIVO_SALIDA = f"{carpeta}Proyecto_Final_Algebra_Lineal_v2.tex"

# Leer datos
with open(ARCHIVO_ENTRADA, "r", encoding="utf-8") as f:
    data = json.load(f)

def formatear_matriz(K):
    filas = [" & ".join(str(x) for x in fila) for fila in K]
    return "\\\\\n".join(filas)

def formatear_cadena(cifrado, por_linea=13):
    filas = [" & ".join(map(str, cifrado[i:i+por_linea])) + r"\\" for i in range(0, len(cifrado), por_linea)]
    return "\n".join(filas)

# ==================== ENCABEZADO DEL DOCUMENTO ====================
header = r"""
\documentclass[12pt]{article}
\usepackage[spanish]{babel}
\usepackage{amsmath, amssymb}
\usepackage[a4paper,margin=2cm]{geometry}
\usepackage{multicol}
\usepackage{graphicx}
\usepackage{fancyhdr}
\setlength{\parindent}{0pt}

\pagestyle{fancy}
\fancyhf{}
\rfoot{\thepage}
\lhead{Facultad de Ingeniería Tampico -- UAT}
\rhead{Proyecto Final de Álgebra Lineal}
\setlength{\headheight}{16pt} % ✅ Evita warnings de fancyhdr

\begin{document}

% ==================== PORTADA ====================
\begin{titlepage}
    \begin{center}
        %\includegraphics[width=3cm]{logo_uat.png}\\[0.5cm]
        {\Large \textbf{Universidad Autónoma de Tamaulipas}}\\[0.3cm]
        {\large \textbf{Facultad de Ingeniería Tampico}}\\[2cm]
        {\LARGE \textbf{Proyecto Final de Álgebra Lineal}}\\[0.5cm]
        {\Large Descifrado de Mensajes mediante Inversas Modulares}\\[2cm]
        \textbf{Profesor:}\\ 
        Dr. Alejandro González Turrubiates\\[0.5cm]
        Dr. David Moreno Ramos\\[0.5cm]
        \textbf{Periodo:} 2025-3\\[0.5cm]
        \vfill
        \textbf{Tampico, Tamaulipas}\\[0.2cm]
        \today
    \end{center}
\end{titlepage}

% ==================== INTRODUCCIÓN ====================
\section*{Introducción}
En este proyecto aplicarás los conceptos de \textbf{matrices inversas} y \textbf{aritmética modular}
para resolver un problema de descifrado de mensajes. Cada estudiante recibe una
\textbf{matriz llave $K$} y una \textbf{cadena cifrada} que representa un mensaje oculto.
Tu tarea consiste en obtener la inversa modular de $K$ módulo 29, y usarla para recuperar el mensaje original.

Este proyecto forma parte del \textit{Producto Integrador de Álgebra Lineal},
y busca que apliques el conocimiento adquirido para resolver una situación de codificación y comunicación segura.

\section*{Objetivo del Proyecto}
Aplicar el concepto de matriz inversa modular para descifrar un mensaje codificado,
demostrando dominio en el manejo de operaciones matriciales en aritmética modular.

% ==================== INSTRUCCIONES ====================
\section*{Instrucciones Generales}
\begin{enumerate}
    \item Calcula la inversa modular $K^{-1}$ de la matriz llave $K$ módulo 29.
    \item Multiplica $K^{-1}$ por los bloques de 3 números de la cadena cifrada para recuperar el mensaje.
    \item Usa la siguiente tabla de equivalencias:
\[
\text{A}=0,\ \text{B}=1,\ \ldots,\ \text{Ñ}=14,\ \ldots,\ \text{Z}=26,\ \text{espacio}=27,\ \text{punto}=28
\]
    \item Escribe el mensaje descifrado y una breve interpretación del mismo.
    \item Entrega un reporte con:
    \begin{itemize}
        \item Desarrollo completo de los cálculos de la inversa modular.
        \item Proceso de descifrado (multiplicaciones mod 29).
        \item Mensaje final obtenido.
        \item Reflexión sobre la utilidad de las matrices en problemas reales.
    \end{itemize}
\end{enumerate}

% ==================== EJEMPLO RESUELTO ====================
\section*{Ejemplo de Resolución}
Supongamos que la matriz llave es:
\[
K = \begin{pmatrix} 2 & 3 \\ 1 & 4 \end{pmatrix} \pmod{29}
\]
El determinante es $\det(K) = 2(4) - 3(1) = 5$, y su inverso módulo 29 es $5^{-1} = 6$.
Entonces:
\[
K^{-1} = 6 \begin{pmatrix} 4 & -3 \\ -1 & 2 \end{pmatrix} =
\begin{pmatrix} 24 & 11 \\ 23 & 12 \end{pmatrix} \pmod{29}
\]

Si la cadena cifrada es:
\[
\begin{bmatrix} 7 \\ 4 \end{bmatrix},\ 
\begin{bmatrix} 0 \\ 2 \end{bmatrix},\ 
\begin{bmatrix} 14 \\ 11 \end{bmatrix}
\]
entonces multiplicando cada bloque por $K^{-1}$ módulo 29 se obtiene la secuencia descifrada,
que puede traducirse según la tabla alfabética para obtener el mensaje original.

\bigskip
\hrule
\bigskip

\section*{Proyectos Individuales}
A continuación se presentan los proyectos asignados a cada estudiante.
Cada uno cuenta con un espacio para anotar su información personal y desarrollar su descifrado.
"""

# ==================== BLOQUES DE PROYECTOS ====================
bloques = []
for alumno in data:
    i = alumno["id"]
    K = alumno["K"]
    cif = alumno["cadena_cifrada"]

    bloque = rf"""
\textbf{{Proyecto {i:03d}}}

\textbf{{Nombre del alumno:}} \underline{{\hspace{{13cm}}}}\\\
\vspace{{1cm}}
\textbf{{Matrícula:}} \underline{{\hspace{{4cm}}}} \hspace{{1cm}}
\textbf{{Grupo:}} \underline{{\hspace{{2cm}}}}
\textbf{{Fecha de entrega:}} \underline{{\hspace{{2cm}}}}

\medskip

Matriz llave:
\[
K = \begin{{pmatrix}}
{formatear_matriz(K)}
\end{{pmatrix}} \pmod{{29}}
\]

Cadena cifrada:
\begin{{center}}
$\begin{{array}}{{lllllllllllll}}
{formatear_cadena(cif)}
\end{{array}}$
\end{{center}}

\newpage
"""
    bloques.append(bloque)

footer = r"\end{document}"

Path(ARCHIVO_SALIDA).write_text(header + "\n".join(bloques) + footer, encoding="utf-8")
print(f"✅ Documento completo generado: {ARCHIVO_SALIDA}")