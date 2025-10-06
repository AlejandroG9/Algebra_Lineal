# hill_3x3_gauss.py
# Cifrado/descifrado Hill 3x3 sin módulo, con matrices unimodulares (det = ±1).
# Inversa exacta (entera) vía adjunta. Ideal para Gauss–Jordan en clase.

import random
from typing import List, Tuple

# ---------- Mapeo ----------
ALPHABET_FWD = {
    **{chr(ord('A') + i): i + 1 for i in range(26)},
    ' ': 27, ',': 28, '.': 29
}
ALPHABET_INV = {v: k for k, v in ALPHABET_FWD.items()}

def normalize_text(s: str) -> str:
    out = []
    for ch in s.upper():
        if ch in ALPHABET_FWD:
            out.append(ch)
        elif ch == 'Á': out.append('A')
        elif ch == 'É': out.append('E')
        elif ch == 'Í': out.append('I')
        elif ch == 'Ó': out.append('O')
        elif ch == 'Ú': out.append('U')
        elif ch == 'Ñ': out.append('N')
        # Otros caracteres se descartan o convierten a espacio si prefieres
    return ''.join(out)

def text_to_numbers(s: str) -> List[int]:
    return [ALPHABET_FWD[ch] for ch in normalize_text(s)]

def numbers_to_text(nums: List[int]) -> str:
    txt = []
    for n in nums:
        if n in ALPHABET_INV:
            txt.append(ALPHABET_INV[n])
        else:
            # Si aparece algo fuera de 1..29, lo marcamos (no debería ocurrir)
            txt.append('?')
    return ''.join(txt)

# ---------- Utilidades de matrices 3x3 ----------
def det3(M: List[List[int]]) -> int:
    a,b,c = M[0]
    d,e,f = M[1]
    g,h,i = M[2]
    return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)

def cofactor_matrix(M: List[List[int]]) -> List[List[int]]:
    a,b,c = M[0]; d,e,f = M[1]; g,h,i = M[2]
    C11 =  (e*i - f*h)
    C12 = -(d*i - f*g)
    C13 =  (d*h - e*g)
    C21 = -(b*i - c*h)
    C22 =  (a*i - c*g)
    C23 = -(a*h - b*g)
    C31 =  (b*f - c*e)
    C32 = -(a*f - c*d)
    C33 =  (a*e - b*d)
    return [[C11, C12, C13],
            [C21, C22, C23],
            [C31, C32, C33]]

def transpose(M: List[List[int]]) -> List[List[int]]:
    return [list(row) for row in zip(*M)]

def adjugate3(M: List[List[int]]) -> List[List[int]]:
    return transpose(cofactor_matrix(M))

def inv_unimodular(M: List[List[int]]) -> List[List[int]]:
    """ Inversa entera: inv(M) = adj(M) / det(M), con det = ±1 """
    d = det3(M)
    if d not in (1, -1):
        raise ValueError(f"La matriz no es unimodular (det={d}).")
    Adj = adjugate3(M)
    if d == 1:
        return Adj
    else:  # d == -1
        return [[-x for x in row] for row in Adj]

def mat_vec_mul(M: List[List[int]], v: List[int]) -> List[int]:
    return [M[0][0]*v[0] + M[0][1]*v[1] + M[0][2]*v[2],
            M[1][0]*v[0] + M[1][1]*v[1] + M[1][2]*v[2],
            M[2][0]*v[0] + M[2][1]*v[1] + M[2][2]*v[2]]

def mat_mul(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    BT = transpose(B)
    return [[sum(a*b for a,b in zip(row, col)) for col in BT] for row in A]

def pretty_matrix(M: List[List[int]]) -> str:
    return "\n".join("".join(f"{x:6d}" for x in row) for row in M)

# ---------- Generación de K ----------
def random_unimodular_matrix(max_abs: int = 5) -> List[List[int]]:
    for _ in range(100000):  # límite alto por seguridad
        K = [[random.randint(-max_abs, max_abs) for _ in range(3)] for _ in range(3)]
        if det3(K) in (1, -1):
            return K
    raise RuntimeError("No se encontró una matriz unimodular en el rango dado.")

# ---------- Bloques y cifrado ----------
def chunk3(nums: List[int], pad: int = 27) -> List[List[int]]:
    r = nums[:]
    while len(r) % 3 != 0:
        r.append(pad)
    return [r[i:i+3] for i in range(0, len(r), 3)]

def flatten(list_of_lists: List[List[int]]) -> List[int]:
    return [x for row in list_of_lists for x in row]

def encrypt(K: List[List[int]], nums: List[int]) -> List[int]:
    blocks = chunk3(nums)
    enc_blocks = [mat_vec_mul(K, v) for v in blocks]
    return flatten(enc_blocks)

def decrypt(K: List[List[int]], cipher: List[int]) -> List[int]:
    invK = inv_unimodular(K)  # entera
    blocks = [cipher[i:i+3] for i in range(0, len(cipher), 3)]
    dec_blocks = [mat_vec_mul(invK, v) for v in blocks]
    return flatten(dec_blocks)

# ---------- API para tu generador ----------
def package_for_student(i: int, frase: str) -> Tuple[List[List[int]], List[int]]:
    """Genera (K, cadena_cifrada) dados id y frase."""
    K = random_unimodular_matrix(max_abs=5)
    nums = text_to_numbers(frase)
    cipher = encrypt(K, nums)
    # (opcional) verificación de vuelta:
    back = decrypt(K, cipher)
    assert back[:len(nums)] == nums, "Verificación de cifrado/descifrado falló."
    return K, cipher

# ---------- Prueba rápida ----------
if __name__ == "__main__":
    frase = "CODIGO SECRETO"
    K = random_unimodular_matrix()
    nums = text_to_numbers(frase)
    cipher = encrypt(K, nums)
    back = decrypt(K, cipher)

    print("Matriz K:")
    print(pretty_matrix(K))
    print("Determinante:", det3(K))
    print("\nFrase original:", frase)
    print("A números      :", nums)
    print("Cifrado (enteros):", cipher)
    print("Descifrado nums :", back[:len(nums)])
    print("Descifrado texto:", numbers_to_text(back)[:len(frase)])