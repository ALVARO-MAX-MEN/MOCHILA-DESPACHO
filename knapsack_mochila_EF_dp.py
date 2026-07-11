import time
import random
import itertools
import matplotlib.pyplot as plt

# =========================================================
# 1. PROGRAMACION DINAMICA (Bottom-Up) - Algoritmo elegido
# =========================================================
def programacion_dinamica(pesos, valores, capacidad):
    n = len(pesos)
    # tabla[i][w] = mejor valor usando los primeros i items con capacidad w
    tabla = [[0] * (capacidad + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        peso_i = pesos[i - 1]
        valor_i = valores[i - 1]
        for w in range(capacidad + 1):
            if peso_i <= w:
                tabla[i][w] = max(
                    tabla[i - 1][w],
                    tabla[i - 1][w - peso_i] + valor_i,
                )
            else:
                tabla[i][w] = tabla[i - 1][w]

    # Reconstruccion del subconjunto optimo (backtracking)
    w = capacidad
    seleccion = []
    for i in range(n, 0, -1):
        if tabla[i][w] != tabla[i - 1][w]:
            seleccion.append(i - 1)
            w -= pesos[i - 1]
    seleccion.reverse()

    return tabla[n][capacidad], tuple(seleccion)


# =========================================================
# 2. FUERZA BRUTA - usada como referencia de validacion
# =========================================================
def fuerza_bruta(pesos, valores, capacidad):
    n = len(pesos)
    mejor_valor = 0
    mejor_seleccion = ()

    for r in range(n + 1):
        for combo in itertools.combinations(range(n), r):
            peso_total = sum(pesos[i] for i in combo)
            if peso_total <= capacidad:
                valor_total = sum(valores[i] for i in combo)
                if valor_total > mejor_valor:
                    mejor_valor = valor_total
                    mejor_seleccion = combo

    return mejor_valor, mejor_seleccion


# =========================================================
# 3. ALGORITMO VORAZ (Greedy) - por relacion valor/peso
# =========================================================
def voraz(pesos, valores, capacidad):
    n = len(pesos)
    indices = sorted(range(n), key=lambda i: valores[i] / pesos[i], reverse=True)

    peso_actual = 0
    valor_total = 0
    seleccion = []

    for i in indices:
        if peso_actual + pesos[i] <= capacidad:
            seleccion.append(i)
            peso_actual += pesos[i]
            valor_total += valores[i]

    return valor_total, tuple(sorted(seleccion))


# =========================================================
# CASO DE PRUEBA: Despacho logistico - capacidad = 50 kg
# =========================================================
if __name__ == "__main__":
    nombres = ["Lote A", "Lote B", "Lote C", "Lote D", "Lote E"]
    pesos =   [10, 20, 30, 25, 8]
    valores = [60, 100, 120, 80, 35]
    capacidad = 50

    print("=" * 70)
    print(" CASO DEMOSTRATIVO: Despacho logistico - capacidad = 50 kg")
    print("=" * 70)
    print(f"{'Producto':<10}{'Peso(kg)':<12}{'Valor(S/.)':<10}")
    for nom, p, v in zip(nombres, pesos, valores):
        print(f"{nom:<10}{p:<12}{v:<10}")
    print("-" * 70)

    v_fb, s_fb = fuerza_bruta(pesos, valores, capacidad)
    v_vz, s_vz = voraz(pesos, valores, capacidad)
    v_dp, s_dp = programacion_dinamica(pesos, valores, capacidad)

    print(f"Fuerza bruta        -> valor = {v_fb:3d} | seleccion = {[nombres[i] for i in s_fb]}")
    print(f"Voraz (greedy)       -> valor = {v_vz:3d} | seleccion = {[nombres[i] for i in s_vz]}")
    print(f"Programacion dinamica-> valor = {v_dp:3d} | seleccion = {[nombres[i] for i in s_dp]}")
    print(f"\n% del optimo alcanzado por el voraz: {v_vz / v_fb * 100:.1f}%")

    # =====================================================
    # ANALISIS EMPIRICO: n pequeno (fuerza bruta viable)
    # =====================================================
    print("\n" + "=" * 70)
    print(" ANALISIS EMPIRICO DE TIEMPOS DE EJECUCION")
    print("=" * 70)

    random.seed(42)

    def generar_datos(n, cap_factor=0.4):
        pesos = [random.randint(1, 50) for _ in range(n)]
        valores = [random.randint(10, 200) for _ in range(n)]
        capacidad = int(sum(pesos) * cap_factor)
        return pesos, valores, capacidad

    n_pequenos = [10, 14, 18, 20]
    resultados_pequenos = []  # (n, t_fb, t_vz, t_dp)

    print(f"\n{'n':<6}{'Fuerza bruta (s)':<20}{'Voraz (s)':<15}{'Prog. Dinamica (s)':<20}")
    for n in n_pequenos:
        p, v, c = generar_datos(n)

        t0 = time.perf_counter()
        fuerza_bruta(p, v, c)
        t_fb = time.perf_counter() - t0

        t0 = time.perf_counter()
        voraz(p, v, c)
        t_vz = time.perf_counter() - t0

        t0 = time.perf_counter()
        programacion_dinamica(p, v, c)
        t_dp = time.perf_counter() - t0

        resultados_pequenos.append((n, t_fb, t_vz, t_dp))
        print(f"{n:<6}{t_fb:<20.6f}{t_vz:<15.6f}{t_dp:<20.6f}")

    # =====================================================
    # ANALISIS EMPIRICO: n grande (fuerza bruta inviable)
    # =====================================================
    n_grandes = [100, 500, 1000, 5000]
    resultados_grandes = []  # (n, t_vz, t_dp, pct_optimo)
    CAPACIDAD_FIJA = 3000  # capacidad fija para no disparar la memoria O(n*W) con n grande

    print("\nn grandes: fuerza bruta se omite (tiempo no viable)")
    print(f"{'n':<8}{'Voraz (s)':<15}{'Prog. Dinamica (s)':<20}")
    for n in n_grandes:
        p = [random.randint(1, 30) for _ in range(n)]
        v = [random.randint(10, 200) for _ in range(n)]
        c = CAPACIDAD_FIJA

        t0 = time.perf_counter()
        v_vz_g, _ = voraz(p, v, c)
        t_vz = time.perf_counter() - t0

        t0 = time.perf_counter()
        v_dp_g, _ = programacion_dinamica(p, v, c)
        t_dp = time.perf_counter() - t0

        pct = v_vz_g / v_dp_g * 100 if v_dp_g else 0
        resultados_grandes.append((n, t_vz, t_dp, pct))
        print(f"{n:<8}{t_vz:<15.6f}{t_dp:<20.6f}(voraz logra {pct:.1f}% del valor optimo)")

    # Caso limite: capacidad = 0
    v0, s0 = programacion_dinamica(pesos, valores, 0)
    print(f"\nPrueba caso limite (capacidad = 0) -> valor = {v0}, seleccion = {s0}")

    # =====================================================
    # FIGURA 1: Comparacion empirica de tiempos de ejecucion
    # =====================================================
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    fig.suptitle("Figura 1. Comparacion empirica de tiempos de ejecucion")

    ns_p = [r[0] for r in resultados_pequenos]
    fb_p = [r[1] for r in resultados_pequenos]
    vz_p = [r[2] for r in resultados_pequenos]
    dp_p = [r[3] for r in resultados_pequenos]

    ax = axes[0]
    ax.plot(ns_p, fb_p, "o-", color="tab:orange", label="Fuerza bruta O(2^n)")
    ax.plot(ns_p, dp_p, "o-", color="tab:green", label="Prog. dinamica O(n*W)")
    ax.plot(ns_p, vz_p, "o-", color="tab:olive", label="Voraz O(n log n)")
    ax.set_yscale("log")
    ax.set_xlabel("n (numero de items)")
    ax.set_ylabel("Tiempo de ejecucion (s) - escala log")
    ax.set_title("n pequeno: crecimiento exponencial\nde la fuerza bruta")
    ax.legend()
    ax.grid(alpha=0.3)

    ns_g = [r[0] for r in resultados_grandes]
    vz_g = [r[1] for r in resultados_grandes]
    dp_g = [r[2] for r in resultados_grandes]

    ax = axes[1]
    ax.plot(ns_g, dp_g, "o-", color="tab:green", label="Prog. dinamica O(n*W)")
    ax.plot(ns_g, vz_g, "o-", color="tab:olive", label="Voraz O(n log n)")
    ax.set_xlabel("n (numero de items)")
    ax.set_ylabel("Tiempo de ejecucion (s)")
    ax.set_title("n grande: crecimiento polinomico\nde la programacion dinamica")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("figura1_comparacion.png", dpi=150)
    print("\nGrafico guardado como 'figura1_comparacion.png'")
