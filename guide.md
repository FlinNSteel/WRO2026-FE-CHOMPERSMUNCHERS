# Plan de Acción y Mejoras Técnicas: CHOMPERSMUNCHERS (WRO 2026)

Este documento detalla las modificaciones, cálculos técnicos y reestructuraciones requeridas en el *Engineering Journal* y el repositorio de GitHub para elevar la puntuación del equipo al rango máximo de **Advanced Engineering (30/30 pts)** en la categoría *Future Engineers*.

---

## 🛠️ 1. Movilidad y Diseño Mecánico (Meta: 6/6 pts)

El diseño actual es puramente descriptivo. Se exige la transición de un modelo "armado" a uno "calculado mediante física y cinemática".

- [ ] **Desarrollar la Geometría de Dirección (Ackermann):**
  - Incluir el diagrama geométrico acotado que demuestre el punto de intersección de las ruedas delanteras alineado con el eje trasero.
  - Añadir la fórmula matemática de validación de los ángulos de giro interno ($\theta_i$) y externo ($\theta_o$):
    $$\cot(\theta_o) - \cot(\theta_i) = \frac{w}{l}$$
    *(Donde $w$ es el ancho de la vía y $l$ es la distancia entre ejes).*
- [ ] **Análisis de Dinámica y Transmisión (Torque/Velocidad):**
  - Graficar o tabular la curva de Torque-Velocidad ($T-\omega$) del motor DC seleccionado.
  - Justificar matemáticamente la relación de reducción de los engranajes en función del peso real del vehículo (1.34 kg), el diámetro de las ruedas y el torque de pérdida (*stall torque*) para garantizar la aceleración óptima sin saturar el driver.
- [ ] **Análisis del Centro de Masa (CoM) y Transferencia de Peso:**
  - Dado que la altura del vehículo es considerable (215 mm) en relación con su longitud (282 mm), documentar el cálculo del Centro de Masa.
  - Explicar mediante un diagrama de fuerzas el comportamiento de transferencia de carga lateral en curvas para justificar que el coche no sufrirá de subviraje o volcado.
- [ ] **Planos Técnicos:**
  - Sustituir los renders simples por planos mecánicos en 2D/3D con cotas dimensionales normalizadas, tolerancias e indicación de los materiales empleados (ej. PLA, filamento de carbono, aluminio).

---

## ⚡ 2. Arquitectura de Energía y Sensores (Meta: 6/6 pts)

- [ ] **Crear el Presupuesto de Potencia (*Power Budget*):**
  - Diseñar una tabla que desglose el consumo de corriente en miliamperios (mA) de cada componente en tres escenarios: *Idle* (reposo), *Nominal* (carrera continua) y *Stall/Peak* (pico máximo de motores y procesamiento).
  - Justificar la autonomía de la batería LiPo elegida calculando el tiempo de operación máximo teórico con base en su capacidad (mAh) y su tasa de descarga (C-rating).
- [ ] **Análisis de Modos de Falla Electrónicos (FMEA):**
  - Documentar las estrategias de mitigación contra fallas críticas (ej. caídas de voltaje causadas por el motor de tracción que reinicien el microcontrolador).
  - Detallar la separación de tierras (*ground loops*) o el uso de capacitores de desacoplo para el ruido electromagnético (EMI).

---

## 💻 3. Arquitectura de Software y Estrategia (Meta: 6/6 pts)

- [ ] **Modelado por Máquina de Estados Finita (FSM):**
  - Implementar e incluir en el Journal un diagrama formal de FSM que gobierne el script principal.
  - Definir explícitamente estados de emergencia o transiciones críticas: `START`, `SEARCHING_PILLARS`, `AVOIDING_OBSTACLE`, `LOST_REFERENCE_RECOVERY`, `PARKING_SEQUENCE`.
- [ ] **Tratamiento de Casos Límite (*Edge Cases*):**
  - Documentar en texto y código qué hace el coche si un pilar obstruye totalmente el rango del sensor de visión o si la lectura ultrasónica produce un "falso positivo" por rebote de señal.
- [ ] **Métricas de Rendimiento del Lazo de Control:**
  - Medir y publicar la frecuencia de actualización (en Hz) del lazo de control PID de dirección y del procesamiento de imágenes. Demostrar que el tiempo de ejecución es determinista.

---

## 🧠 4. Pensamiento de Sistemas y Decisiones de Ingeniería (Meta: 6/6 pts)

- [ ] **Construir Matrices de Decisión (*Trade-off Matrices*):**
  - Eliminar los párrafos cualitativos ("elegimos este sensor porque es bueno").
  - Introducir tablas comparativas cuantitativas puntuadas (escala 1-5) con pesos ponderados basados en las restricciones del proyecto (Peso, Costo, Consumo de Corriente, Precisión, Tiempo de Procesamiento).
  - *Ejemplo de matriz requerida:* Sensor de visión clásico vs. Cámara inteligente; Motor DC convencional vs. Motor Brushless.

---

## 🐙 5. Gobernanza de Código y Reproducibilidad en GitHub (Meta: 6/6 pts)

- [ ] **Estandarizar el Historial de Git (Commits Semánticos):**
  - Adoptar la convención de *Conventional Commits*. Los futuros mensajes no deben ser genéricos. Usar la estructura:
    * `feat(mec):` para cambios en modelos CAD o mecánicos.
    * `fix(nav):` para correcciones en el algoritmo de evasión.
    * `docs(journal):` para actualizaciones en la documentación.
- [ ] **Gobernanza de Versiones:**
  - Utilizar el sistema de etiquetas (*Tags*) de GitHub para marcar hitos estables del desarrollo (ej. `v1.0.0-alpha`, `v1.0.0-beta`, `v2.0.0-stable`).
- [ ] **Guía de Reproducibilidad Total:**
  - Añadir al `README.md` un apartado exclusivo de despliegue que describa los pasos exactos para reproducir el entorno de desarrollo:
    * Versión exacta del sistema operativo o entorno embebido.
    * Archivo de dependencias (`requirements.txt` para Python o configuración de CMake/PlatformIO para C++).
    * Comandos de terminal necesarios para compilar y flashear el código sin errores desde una computadora limpia.
