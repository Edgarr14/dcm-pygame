# DCM PYGAME: Car Parking Simulator

Simulador interactivo de maniobras de estacionamiento en vista superior (*top-down*) desarrollado en Python con Pygame para la asignatura **Diseño y Control de Modelos (DCM)**. 

El proyecto modela la física real de conducción a bajas velocidades combinando el **Modelo Cinemático de Bicicleta** (geometría de dirección vehicular) con **dinámica longitudinal con fricción**, permitiendo modificar parámetros físicos en tiempo real y validar los resultados frente a datos empíricos de referencia.

---

## Estructura del Proyecto

```text
├── src/
│   ├── main.py              # Game Loop, captura de eventos y controles
│   ├── physics_model.py     # Motor matemático/físico (Ecuaciones, Euler semi-implícito y colisiones OBB)
│   └── ui.py                # Renderizado del estacionamiento, obstáculos y HUD de telemetría
├── validation/
│   ├── comparativa.py       # Script de validación automatizada y generación de gráficas
│   ├── comparativa_validacion.png
│   └── tabla_resultados.csv
├── requirements.txt         # Dependencias del proyecto (pygame-ce, numpy, matplotlib)
└── README.md
```

---

## Instalación y Cómo Jugar

### 1. Clonar el repositorio
```powershell
git clone https://github.com/Edgarr14/dcm-pygame.git
cd dcm-pygame
```

### 2. Crear y activar el entorno virtual (`venv`)
**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**En Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las librerías necesarias
```powershell
pip install -r requirements.txt
```

### 4. Ejecutar el simulador
```powershell
python src/main.py
```

### Controles del Juego
| Tecla | Acción |
| :--- | :--- |
| **`↑` / `W`** | Acelerar hacia adelante |
| **`↓` / `S`** | Reversa |
| **`←` / `A` y `→` / `D`** | Girar volante (izquierda / derecha) |
| **`ESPACIO`** | Freno de emergencia |
| **`R`** | Reiniciar vehículo a la posición inicial |
| **`1` / `2`** | Disminuir / Aumentar distancia entre ejes ($L$) |
| **`3` / `4`** | Disminuir / Aumentar coeficiente de fricción ($\mu$) |

---

## Validación y Comparativa del Modelo

Para contrastar el comportamiento del motor físico contra datos de referencia empíricos (radio de giro según el ángulo de dirección y distancia de frenado según el coeficiente de rozamiento del pavimento), ejecuta el script de validación con el entorno virtual activo:

```powershell
python validation/comparativa.py
```

Al ejecutarse, el script realiza simulaciones *headless* a 60 FPS utilizando directamente la clase `CarPhysicsModel` y genera automáticamente dos archivos dentro de la carpeta `validation/`:
1. **`comparativa_validacion.png`:** Gráficas comparativas entre los valores de referencia y los resultados arrojados por el simulador.
2. **`tabla_resultados.csv`:** Tabla con los valores numéricos y el cálculo del error relativo porcentual de cada prueba.

---

## Integrantes

* **Edgar Guerra V-30.225.820**
* **Eilyn Martinez V-28.434.193**