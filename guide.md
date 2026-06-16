# Plan de Acción y Mejoras Técnicas: CHOMPERSMUNCHERS (LEGO & Pybricks Edition)

Este documento detlana las modificaciones, cálculos técnicos y justificaciones de software que debes integrar en tu *Engineering Journal* y repositorio de GitHub para alcanzar los **30/30 puntos** utilizando la plataforma LEGO y el entorno Pybricks.

---

## 🛠️ 1. Movilidad y Diseño Mecánico (Meta: 6/6 pts)

El uso de piezas LEGO exige demostrar que el chasis cumple con rigidez estructural y precisión geométrica, alejándose del paradigma de "bloques de construcción" casuales.

- [ ] **Geometría de Dirección Ackermann en LEGO:**
  - Los pivotes y brazos de dirección de LEGO Technic tienen distancias discretas (medidas en *studs* o unidades LEGO: $1\text{ stud} = 8\text{ mm}$). Debes incluir el diagrama geométrico exacto de tus liftarms y vigas.
  - Demuestra matemáticamente que la disposición de los conectores cumple o se aproxima a la ecuación de Ackermann:
    $$\cot(\theta_o) - \cot(\theta_i) = \frac{w}{l}$$
    *(Donde $w$ es la distancia entre los pivotes de dirección y $l$ es la distancia entre el eje delantero y trasero, expresado en studs o mm).*
- [ ] **Justificación de Transmisión (Relación de Engranajes LEGO):**
  - No basta con decir "usamos un motor Large". Debes documentar la relación de reducción usando los dientes de los engranajes LEGO (ej. piñón de 12t a corona de 36t para una reducción 3:1).
  - Justifica esa reducción calculando la velocidad máxima teórica en pista y el torque disponible en las ruedas traseras basándote en las especificaciones oficiales del motor angular de SPIKE Prime/Mindstorms (~$175\text{ rpm}$ nominal, ~$0.25\text{ Nm}$ de stall torque a $9\text{V}$).
- [ ] **Análisis de Flexión y Rigidez del Chasis:**
  - Explica cómo mitigaste la flexibilidad inherente de los conectores LEGO (*pins*) bajo la carga de 1.34 kg (ej. uso de marcos Technic rectangulares, vigas dobles o fijaciones cruzadas para evitar que el chasis se doble en curvas de alta velocidad).

---

## ⚡ 2. Arquitectura de Energía y Sensores (Meta: 6/6 pts)

- [ ] **Presupuesto de Potencia del Hub LEGO:**
  - La batería interna del Hub (SPIKE Prime / Inventor) proporciona una corriente máxima limitada antes de activar la protección térmica o causar caídas de voltaje (*brownouts*) que congelen los sensores o la CPU.
  - Crea una tabla de consumo estimando la corriente (mA) del motor de tracción bajo esfuerzo, el servo de dirección, el consumo del propio Hub y de los sensores externos (como cámaras OpenMV/ESP32 si están conectadas por UART/I2C).
- [ ] **Justificación Geométrica de Sensores con Pybricks:**
  - Explica la altura y el ángulo de inclinación de los sensores ultrasónicos o de distancia LEGO analizando el cono de detección en studs para asegurar que detecten los pilares de la WRO sin ver el suelo ni saltarse los obstáculos.

---

## 💻 3. Arquitectura de Software y Estrategia (Meta: 6/6 pts)

Pybricks te da control directo sobre los algoritmos internos del Hub. Debes documentar cómo aprovechas este firmware avanzado.

- [ ] **Explicación del Lazo Cerrado de Pybricks (`control.pid`):**
  - El gran valor de Pybricks es su control PID nativo para motores con encoder. Debes documentar cómo configuraste los parámetros del motor de tracción y dirección.
  - Si modificaste las tolerancias o ganancias por defecto usando `motor.control.pid()`, justifica por qué los valores de fábrica no eran suficientes para la dinámica del coche en las curvas de la WRO.
- [ ] **Máquina de Estados Finita (FSM) en MicroPython:**
  - Incluye el diagrama de flujo o matriz de estados de tu script principal en Python.
  - Detalla cómo gestionas los estados de navegación síncrona/asíncrona (ej. usando un bucle `while True` estructurado o la librería `uasyncio` si ejecutas tareas concurrentes).
- [ ] **Manejo de Casos Límite (*Edge Cases*):**
  - Explica cómo reacciona el código en Pybricks si la lectura de un pilar da un valor fuera de rango o si el coche experimenta un *stall* (atasco de motor detectado mediante `motor.control.stalled()`).

---

## 🧠 4. Pensamiento de Sistemas y Decisiones de Ingeniería (Meta: 6/6 pts)

- [ ] **Matrices de Decisión Cuantitativas (*Trade-offs*):**
  - Justifica con datos por qué decidieron migrar de la plataforma oficial de LEGO (Blockly/Python estándar de SPIKE) hacia **Pybricks**. 
  - *Ejemplo de matriz de decisión:* Compara tiempos de ejecución, precisión en la sincronización de motores, estabilidad del emparejamiento y acceso a protocolos de comunicación (I2C/UART avanzados) entre ambas plataformas de software.

---

## 🐙 5. Reproducibilidad y Calidad de GitHub (Meta: 6/6 pts)

- [ ] **Instrucciones de Construcción LEGO:**
  - En lugar de archivos CAD genéricos en formato STEP, sube al repositorio el archivo de diseño en **BrickLink Studio 2.0 (`.io`)** o un PDF con las instrucciones paso a paso generadas por el mismo programa. Esto garantiza que cualquier juez o equipo pueda replicar exactamente tu chasis mecánico.
- [ ] **Guía de Despliegue de Pybricks:**
  - En el `README.md`, detalla los pasos exactos para cargar el código: qué versión del compilador de Pybricks se utilizó (ej. Pybricks v3.x), si se requiere la extensión de VS Code, Pybricks Code Web, o la herramienta de línea de comandos `pybricksdev` para flashear el Hub.
