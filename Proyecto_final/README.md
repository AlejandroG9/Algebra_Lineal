# 🔢 Proyecto Final de Álgebra Lineal  
### Cifrado y Descifrado de Mensajes mediante Matrices 3x3 (Método de Gauss–Jordan)

Este proyecto genera automáticamente **300 versiones únicas** del proyecto final de Álgebra Lineal.  
Cada alumno recibe una **matriz llave invertible 3×3** y una **cadena cifrada** correspondiente a una frase oculta.  
Su tarea es descifrarla aplicando el **método de Gauss–Jordan** para calcular la inversa de la matriz.

---

## 🧭 Estructura del Proyecto

```
Proyecto_final/
│
├── generar_paquetes.py                  # Script principal para generar los 300 ejercicios
├── hill_3x3_gauss.py                    # Módulo con las funciones de cifrado y generación de matrices
│
├── frases/
│   ├── frases_300_motivacionales_v3.txt # Archivo fuente con frases motivacionales
│   ├── paquetes_300_docente.json        # Salida con toda la información (matriz + frase original)
│   └── paquetes_300_alumnos.json        # Salida con solo matriz y cadena cifrada
│
└── Proyecto_final_individual/
    └── pdfs_alumnos/                    # Carpeta donde se guardan los PDFs individuales
```

---

## ⚙️ Instalación

1. **Crear entorno virtual (recomendado)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate      # Windows
   ```

2. **Instalar dependencias**

   ```bash
   pip install numpy pylatex
   ```

3. **Verifica que tienes `latexmk` y `pdflatex` instalados**

   En macOS (Homebrew):

   ```bash
   brew install mactex
   ```

   En Ubuntu/Debian:

   ```bash
   sudo apt install texlive-latex-extra latexmk
   ```

---

## 🚀 Flujo General

### 1️⃣ Generar las matrices y frases cifradas

Ejecuta el script principal:

```bash
python generar_paquetes.py
```

Esto generará dos archivos JSON dentro de la carpeta `frases/`:

- `paquetes_300_docente.json` → contiene **la matriz, la cadena cifrada y la frase original** (para el profesor).  
- `paquetes_300_alumnos.json` → contiene **solo la matriz y la cadena cifrada** (para los alumnos).

Cada registro tiene este formato:

```json
{
  "id": 1,
  "tipo": "motivacional",
  "frase_original": "La perseverancia vence a la inteligencia.",
  "longitud": 40,
  "K": [[2, 5, 7], [1, 6, 3], [4, 0, 8]],
  "cadena_cifrada": [125.0, 232.0, 97.0, ...]
}
```

---

### 2️⃣ Generar los PDFs individuales

El script `generar_pdf_individuales.py` usa el archivo `paquetes_300_docente.json` para crear un **PDF personalizado para cada alumno** con:

- Encabezado institucional  
- Instrucciones generales  
- Ejemplo ilustrativo del proceso de descifrado  
- Espacio para cálculos  
- Matriz llave y cadena cifrada únicas  

Ejecutar:

```bash
python generar_pdf_individuales.py
```

Cada archivo se guarda con el nombre:

```
Proyecto_final_individual/pdfs_alumnos/Proyecto_001.pdf
Proyecto_final_individual/pdfs_alumnos/Proyecto_002.pdf
...
```

---

## 🧮 Descripción del Método

Cada alumno recibe una matriz 3×3 llamada **matriz llave K**, y una secuencia de números que representa un **mensaje cifrado**.

El procedimiento consiste en:

1. Calcular la **inversa de K** usando el método de **Gauss–Jordan**.  
   No se usa módulo ni operaciones en cuerpos finitos.

2. Agrupar los números cifrados en bloques de 3.

3. Multiplicar cada bloque por la inversa \( K^{-1} \) para obtener los números originales.

4. Convertir los números a letras usando la tabla:
   ```
   A=1, B=2, ..., Z=26, Espacio=27, ,=28, .=29
   ```

5. Escribir la frase resultante.

---

## 📘 Ejemplo de Descifrado

Suponga que se da la matriz:

\$
K =
\begin{pmatrix}
2 & 5 & 7 \\
1 & 6 & 3 \\
4 & 0 & 8
\end{pmatrix}
\quad \text{y la cadena cifrada } [7,18,3,4,9,2,15,21,5]
\$

1. Calcular \( K^{-1} \) con el método de Gauss–Jordan.
2. Multiplicar \( K^{-1} \) por cada bloque de 3 números.
3. Convertir los resultados en letras según la tabla.
4. Se obtiene el mensaje: **"CÓDIGO SECRETO"**.

---

## 🧑‍🏫 Recomendaciones para el Docente

- Asigna a cada alumno un **número de proyecto** (del 001 al 300).  
- Puedes distribuir los PDF por correo o por Teams.
- Guarda el archivo `paquetes_300_docente.json` en un lugar seguro: contiene las frases originales.

---

## 🧰 Archivos Clave

| Archivo | Descripción |
|----------|--------------|
| `hill_3x3_gauss.py` | Define cómo se generan las matrices y cómo se cifra cada frase. |
| `generar_paquetes.py` | Crea los archivos JSON con la información para los 300 alumnos. |
| `generar_pdf_individuales.py` | Genera los PDFs personalizados para entregar a los estudiantes. |
| `instrucciones_y_ejemplo.tex` | Archivo LaTeX que se inserta en cada PDF con las instrucciones y el ejemplo. |

---

## 📦 Exportar o Modificar

Si deseas generar menos proyectos, edita esta línea en `generar_pdf_individuales.py`:

```python
for p in paquetes[:10]:
```

Y reemplázala por:

```python
for p in paquetes:
```

Para incluir los 300.

---

## 📄 Licencia

Este material ha sido desarrollado por **Dr. Alejandro González Turrubiates**,  
Facultad de Ingeniería Tampico, Universidad Autónoma de Tamaulipas.  
Uso académico permitido para fines educativos y de evaluación.
