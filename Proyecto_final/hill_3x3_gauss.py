# ======================================================
# Archivo: hill_3x3_gauss.py
# Genera una matriz llave 3x3 invertible y cifra una frase SIN módulo.
# ======================================================

import numpy as np
import random

# ------------------------------------------------------
# 1. Mapeo de letras a números y viceversa
# ------------------------------------------------------
alfabeto = {chr(i + 64): i for i in range(1, 27)}  # A=1,...,Z=26
alfabeto[' '] = 27
alfabeto[','] = 28
alfabeto['.'] = 29
inverso = {v: k for k, v in alfabeto.items()}

# ------------------------------------------------------
# 2. Generar matriz llave invertible (3x3)
# ------------------------------------------------------
def generar_matriz_llave():
    while True:
        K = np.random.randint(1, 10, (3, 3)).astype(float)
        if abs(np.linalg.det(K)) > 1e-6:
            return K.round(2).tolist()

# ------------------------------------------------------
# 3. Convertir texto a números
# ------------------------------------------------------
def frase_a_numeros(frase: str):
    nums = []
    for c in frase.upper():
        if c in alfabeto:
            nums.append(alfabeto[c])
    while len(nums) % 3 != 0:
        nums.append(27)  # relleno con espacio
    return np.array(nums)

# ------------------------------------------------------
# 4. Cifrar frase
# ------------------------------------------------------
def cifrar_frase(K, frase):
    K = np.array(K)
    nums = frase_a_numeros(frase)
    cifrado = []
    for i in range(0, len(nums), 3):
        bloque = nums[i:i+3]
        resultado = K.dot(bloque)
        cifrado.extend(resultado.round(2).tolist())
    return cifrado

# ------------------------------------------------------
# 5. Paquete por estudiante (mantiene compatibilidad)
# ------------------------------------------------------
def package_for_student(i, frase):
    K = generar_matriz_llave()
    cifrado = cifrar_frase(K, frase)
    return K, cifrado

# ------------------------------------------------------
# 6. Formato bonito de matrices
# ------------------------------------------------------
def pretty_matrix(K):
    if isinstance(K, list):
        K = np.array(K)
    return "\n".join(["  ".join(f"{x:5.2f}" for x in fila) for fila in K])