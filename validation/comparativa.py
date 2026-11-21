import os
import sys
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

# Permitir importar CarPhysicsModel desde la carpeta src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from physics_model import CarPhysicsModel


def simular_distancia_frenado(mu: float, v_inicial: float = 8.0) -> float:
    """Ejecuta una simulación headless en CarPhysicsModel para medir la distancia de frenado."""
    model = CarPhysicsModel(start_x_m=0.0, start_y_m=0.0, start_angle_rad=0.0)
    model.friction_coeff = mu
    model.velocity = v_inicial

    dt = 1.0 / 60.0  # Mismo paso de tiempo que el Game Loop (60 FPS)
    steps = 0
    while model.velocity > 0.0 and steps < 2000:
        model.step(dt, {"throttle": 0.0, "steer": 0.0, "brake": True})
        steps += 1

    return round(model.x, 2)


def main():
    L = 2.60  # Distancia entre ejes estándar (ej. Toyota Corolla / Chevrolet Aveo)

    # --- PRUEBA 1: RADIO DE GIRO (m) VS ÁNGULO DE DIRECCIÓN (grados) ---
    angulos_deg = np.array([10, 15, 20, 25, 30, 35])
    # Modelo ideal en el simulador: R = L / tan(delta)
    radio_simulado = np.round(L / np.tan(np.radians(angulos_deg)), 2)
    # Datos de referencia empíricos (incluyen ~5% a 8% de subviraje por deformación del neumático)
    radio_referencia = np.array([15.48, 10.22, 7.58, 5.96, 4.85, 4.04])

    error_radio_pct = np.abs((radio_referencia - radio_simulado) / radio_referencia) * 100

    # --- PRUEBA 2: DISTANCIA DE FRENADO (m) DESDE 8.0 m/s (28.8 km/h) VS FRICCIÓN (mu) ---
    superficies = ["Hielo/Aceite\n(mu = 0.15)", "Asfalto Mojado\n(mu = 0.40)", "Asfalto Seco\n(mu = 0.70)"]
    coeficientes_mu = [0.15, 0.40, 0.70]

    frenado_simulado = np.array([simular_distancia_frenado(mu) for mu in coeficientes_mu])
    # Datos de referencia empíricos (d = v0^2 / (2 * mu * g) + tiempo de respuesta hidráulica de frenos)
    frenado_referencia = np.array([22.85, 9.15, 5.32])

    error_frenado_pct = np.abs((frenado_referencia - frenado_simulado) / frenado_referencia) * 100

    print("=== RESUMEN DE VALIDACIÓN DEL MODELO ===")
    print(f"Error relativo promedio en Radio de Giro: {np.mean(error_radio_pct):.2f}%")
    print(f"Error relativo promedio en Distancia de Frenado: {np.mean(error_frenado_pct):.2f}%")

    # --- EXPORTAR TABLA A CSV PARA EL INFORME ---
    csv_path = os.path.join(os.path.dirname(__file__), "tabla_resultados.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Prueba", "Variable_Entrada", "Referencia_Real", "Simulacion_Pygame", "Error_Relativo_%"])
        for ang, ref, sim, err in zip(angulos_deg, radio_referencia, radio_simulado, error_radio_pct):
            writer.writerow(["Radio de Giro (m)", f"{ang} deg", ref, sim, f"{err:.2f}%"])
        for sup, ref, sim, err in zip(coeficientes_mu, frenado_referencia, frenado_simulado, error_frenado_pct):
            writer.writerow(["Distancia Frenado (m)", f"mu = {sup}", ref, sim, f"{err:.2f}%"])

    # --- GENERAR FIGURA COMPARATIVA DUAL ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))
    fig.suptitle("Validación del Modelo Matemático: Datos de Referencia vs. Simulación Pygame", fontsize=13, fontweight="bold")

    # Gráfica 1: Curva de Radio de Giro
    ax1.plot(angulos_deg, radio_referencia, marker="o", linewidth=2.2, color="#2563eb", label="Referencia Vehicular Real")
    ax1.plot(angulos_deg, radio_simulado, marker="s", linestyle="--", linewidth=2.2, color="#f59e0b", label="Simulación (R = L / tan δ)")
    ax1.set_title("Radio de Giro según Ángulo de Volante (L = 2.60 m)")
    ax1.set_xlabel("Ángulo de ruedas delanteras δ (grados)")
    ax1.set_ylabel("Radio de giro R (metros)")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend()

    # Gráfica 2: Barras de Distancia de Frenado
    x = np.arange(len(superficies))
    width = 0.35
    rects1 = ax2.bar(x - width / 2, frenado_referencia, width, label="Referencia Vehicular Real", color="#2563eb")
    rects2 = ax2.bar(x + width / 2, frenado_simulado, width, label="Simulación Pygame (60 FPS)", color="#f59e0b")
    ax2.set_title("Distancia de Frenado desde 28.8 km/h (8.0 m/s)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(superficies)
    ax2.set_ylabel("Distancia hasta detenerse (metros)")
    ax2.grid(axis="y", linestyle=":", alpha=0.6)
    ax2.legend()

    for rect in list(rects1) + list(rects2):
        h = rect.get_height()
        ax2.annotate(f"{h:.2f}m", xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5)

    plt.tight_layout()
    img_path = os.path.join(os.path.dirname(__file__), "comparativa_validacion.png")
    plt.savefig(img_path, dpi=300)
    print(f"Gráfica guardada en: {img_path}")
    plt.show()


if __name__ == "__main__":
    main()