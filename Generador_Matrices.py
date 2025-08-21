import numpy as np

def es_entera(matriz):
    return np.all(np.mod(matriz, 1) == 0)


def generar_matrices_enteras_inversibles(cantidad=6):
    matrices = []
    intentos = 0

    while len(matrices) < cantidad and intentos < 10000:
        A = np.random.randint(-5, 6, (3, 3))  # Matriz con enteros entre -5 y 5
        det = round(np.linalg.det(A))

        try:
            A_inv = np.linalg.inv(A)
            if det in [1, -1] and es_entera(A_inv):
                matrices.append((A, A_inv))
        except np.linalg.LinAlgError:
            continue  # Matriz no invertible
        intentos += 1

    return matrices


# Generar matrices
matrices = generar_matrices_enteras_inversibles()

# Mostrar resultados
for i, (A, A_inv) in enumerate(matrices):
    print(f"\n🔢 Matriz #{i + 1} (A):\n{A}")
    print(f"\n🧮 Inversa (A⁻¹):\n{A_inv.astype(int)}")

    # Ejemplo de ecuaciones simultáneas
    B = np.random.randint(1, 10, (3, 1))
    X = A_inv @ B
    print(f"\n📘 Ejemplo: Resolviendo A·X = B")
    print(f"B =\n{B}")
    print(f"X = A⁻¹·B =\n{X.astype(int)}")