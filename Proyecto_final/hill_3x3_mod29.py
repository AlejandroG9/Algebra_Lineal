# hill_3x3_mod29.py
# Genera matrices 3x3 invertibles mod 29, verifica inversa, convierte texto<->números
# y cifra/descifra mensajes por bloques de 3 (tipo Hill Cipher).
# Alfabeto (m=29): A=0,...,N=13, Ñ=14, O=15,...,Z=26, " " (espacio)=27, "."=28

import random
import unicodedata
from typing import List, Tuple

M = 29  # módulo primo
SYMS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÑ ."
# Indices: A..Z (0..26), Ñ (14), espacio (27), punto (28)
# Mapeo
char2num = {ch: i for i, ch in enumerate(SYMS)}
num2char = {i: ch for i, ch in enumerate(SYMS)}

def normalize_keep_enye(s: str) -> str:
    """Quita acentos, conserva Ñ/ñ y mayusculiza; elimina caracteres no permitidos."""
    s = s.replace("Ñ", "__ENYE__").replace("ñ", "__ENYE__")
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = s.upper().replace("__ENYE__", "Ñ")
    # Validación de caracteres
    for ch in s:
        if ch not in SYMS:
            raise ValueError(f"Carácter no permitido: {repr(ch)}")
    return s

def text_to_numbers(text: str) -> List[int]:
    text = normalize_keep_enye(text)
    return [char2num[ch] for ch in text]

def numbers_to_text(nums: List[int]) -> str:
    return "".join(num2char[(n % M)] for n in nums)

def pad_to_block3(nums: List[int]) -> List[int]:
    # relleno con espacio (27) hasta múltiplo de 3
    r = len(nums) % 3
    if r != 0:
        nums = nums + [char2num[" "]] * (3 - r)
    return nums

def blocks3(nums: List[int]) -> List[List[int]]:
    return [nums[i:i+3] for i in range(0, len(nums), 3)]

def mat_mul_vec_mod(A: List[List[int]], v: List[int], m: int = M) -> List[int]:
    return [sum(A[i][j]*v[j] for j in range(3)) % m for i in range(3)]

def mat_mul_mod(A: List[List[int]], B: List[List[int]], m: int = M) -> List[List[int]]:
    return [[sum(A[i][k]*B[k][j] for k in range(3)) % m for j in range(3)] for i in range(3)]

def mat_det_mod(A: List[List[int]], m: int = M) -> int:
    # determinante 3x3
    a,b,c = A[0]; d,e,f = A[1]; g,h,i = A[2]
    det = (a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)) % m
    return det

def inv_mod(a: int, m: int = M) -> int:
    # m es primo => inverso modular a^(m-2) mod m (Fermat)
    a %= m
    if a == 0:
        raise ZeroDivisionError("No existe inverso de 0 mod m.")
    return pow(a, m-2, m)

def mat_adj_mod(A: List[List[int]], m: int = M) -> List[List[int]]:
    # adj(A) = cofactores^T
    a,b,c = A[0]; d,e,f = A[1]; g,h,i = A[2]
    C11 = (e*i - f*h) % m
    C12 = (-(d*i - f*g)) % m
    C13 = (d*h - e*g) % m
    C21 = (-(b*i - c*h)) % m
    C22 = (a*i - c*g) % m
    C23 = (-(a*h - b*g)) % m
    C31 = (b*f - c*e) % m
    C32 = (-(a*f - c*d)) % m
    C33 = (a*e - b*d) % m
    # Transpuesta de cofactores
    return [
        [C11, C21, C31],
        [C12, C22, C32],
        [C13, C23, C33],
    ]

def mat_inv_mod(A: List[List[int]], m: int = M) -> List[List[int]]:
    det = mat_det_mod(A, m)
    if det % m == 0:
        raise ValueError("Matriz no invertible mod m (det ≡ 0).")
    det_inv = inv_mod(det, m)
    adj = mat_adj_mod(A, m)
    return [[(det_inv * adj[i][j]) % m for j in range(3)] for i in range(3)]

def random_invertible_matrix_3x3(m: int = M) -> List[List[int]]:
    while True:
        A = [[random.randrange(m) for _ in range(3)] for _ in range(3)]
        if mat_det_mod(A, m) % m != 0:
            return A

def verify_inverse(A: List[List[int]], Ainv: List[List[int]], m: int = M) -> bool:
    I = mat_mul_mod(A, Ainv, m)
    # verificar identidad
    return I == [[1,0,0],[0,1,0],[0,0,1]]

def encrypt_with_key(K: List[List[int]], text: str) -> List[int]:
    nums = text_to_numbers(text)
    nums = pad_to_block3(nums)
    c = []
    for blk in blocks3(nums):
        out = mat_mul_vec_mod(K, blk, M)
        c.extend(out)
    return c

def decrypt_with_key(K: List[List[int]], cipher_nums: List[int]) -> str:
    Kinv = mat_inv_mod(K, M)
    plain = []
    for blk in blocks3(cipher_nums):
        out = mat_mul_vec_mod(Kinv, blk, M)
        plain.extend(out)
    return numbers_to_text(plain)

def package_for_student(student_id: int, phrase: str):
    if (len(phrase) % 3) != 0 or not (90 <= len(phrase) <= 110):
        raise ValueError("La frase debe ser multiplo de 3 y ~100 caracteres.")
    K = random_invertible_matrix_3x3(M)
    cipher = encrypt_with_key(K, phrase)
    return K, cipher

def pretty_matrix(A: List[List[int]]) -> str:
    return "\n".join(str(row) for row in A)

if __name__ == "__main__":
    random.seed(2025)

    # Ejemplo rápido con una frase corta (solo para probar):
    demo = "HOLA UAT. " * 12  # 108 chars; se recorta a ejemplo
    demo = demo[:100]
    K = random_invertible_matrix_3x3()
    print("Matriz llave K:")
    print(pretty_matrix(K))
    print("det(K) mod 29 =", mat_det_mod(K))
    Kinv = mat_inv_mod(K)
    print("Verificación inversa:", verify_inverse(K, Kinv))

    c = encrypt_with_key(K, demo)
    print("Primeros 18 números cifrados:", c[:18])

    rec = decrypt_with_key(K, c)
    print("¿Recupera exactamente?", rec == demo)
    print("Texto recuperado (primeros 120):", rec[:120])