from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait, StopWatch

# ==========================================
# 1. INICIALIZACIÓN DE HARDWARE
# ==========================================
hub = PrimeHub()

sensor_ad = UltrasonicSensor(Port.F)
sensor_izq = UltrasonicSensor(Port.D)
sensor_der = UltrasonicSensor(Port.C)

drive = Motor(Port.B, Direction.CLOCKWISE) # esta a lreves
steering = Motor(Port.A, Direction.CLOCKWISE)

# ==========================================
# 2. CONSTANTES Y CONFIGURACIÓN
# ==========================================
VELOCIDAD_AVANCE = 800
VELOCIDAD_BASE = 500

# Límites físicos y lógicos
LIMITE_IZQ = -47
LIMITE_DER = 67
LIMITE_ROT = 1000
LIMITE_AD = 600
LIMITE_DIST_RECTO = 150
ROT_TIME_MIN = 4000      # Milisegundos mínimos entre giros
MAX_VUELTA = 3
SECCIONES_TOTALES = MAX_VUELTA * 4 

# Ganancias del control de rumbo
KP_YAW = 3
KD_YAW = 1
KI_YAW = 0.01

# Parámetros de Sensores (No bloqueantes)
N_MUESTRAS = 9
INTERVALO_MUESTREO = 60

# ==========================================
# 3. ESTADOS Y BÚFERES (Sustituyen a los Globals)
# ==========================================
lecturas_izq = []
lecturas_der = []
lecturas_ad = []

# Relojes
reloj_sensores = StopWatch()
reloj_rot = StopWatch()
reloj_telemetria = StopWatch()

# Estado general del robot
robot_state = {
    "rumbo_objetivo": 0,
    "seccion_actual": 1,
    "cant_giros": 0,
    "giro_direc": None  # 1 (Izq) o 0 (Der)
}

# Estado del controlador PID
pid_state = {
    "integral": 0,
    "prev_error": 0
}

# ==========================================
# 4. FUNCIONES DE UTILIDAD
# ==========================================

def mover_por_mm(distancia_en_mm, rumbo):
    """Mueve el robot una distancia exacta manteniendo el control PID de rumbo y velocidad global."""
    # Transformación de milímetros a grados del motor (Rueda de 62mm)
    transformacion_grados = (distancia_en_mm * 360) / (62 * 3.1416)
    
    # Reiniciamos el contador del motor
    drive.reset_angle(0)
    
    print("\n" + "="*40)
    print(f"--- Moviendo {distancia_en_mm} mm con PID al rumbo {rumbo}° ---")
    print("="*40)
    
    # Mientras los grados rotados sean menores a nuestro objetivo
    while abs(drive.angle()) < transformacion_grados:
        
        # Invocamos el PID usando la velocidad por defecto (VELOCIDAD_AVANCE)
        mantener_linea_recta(rumbo)
        
        # Pausa de 5 milisegundos para no asfixiar la CPU del Hub
        wait(5)
        
    # Una vez alcanzada la distancia, detenemos los motores
    drive.stop()
    steering.stop()
    print(">> Movimiento de distancia completado.\n")

def iniciar_robot():
    print("\n==========================================")
    print("--- CONTROL DESDE 0: AVANCE RECTO ---")
    print("==========================================\n")
    steering.reset_angle(0)
    hub.imu.reset_heading(0)
    drive.run(VELOCIDAD_AVANCE)

def leer_sensores():
    """Lee sensores sin bloquear y retorna las medianas si el búfer está lleno."""
    if reloj_sensores.time() < INTERVALO_MUESTREO:
        return None, None, None

    reloj_sensores.reset()

    lecturas_izq.append(sensor_izq.distance())
    lecturas_der.append(sensor_der.distance())
    lecturas_ad.append(sensor_ad.distance())

    if len(lecturas_izq) > N_MUESTRAS:
        lecturas_izq.pop(0)
        lecturas_der.pop(0)
        lecturas_ad.pop(0)

    # Solo evalúa cuando el búfer tiene las muestras necesarias
    if len(lecturas_izq) == N_MUESTRAS:
        med_izq = sorted(lecturas_izq)[N_MUESTRAS // 2]
        med_der = sorted(lecturas_der)[N_MUESTRAS // 2]
        med_ad = sorted(lecturas_ad)[N_MUESTRAS // 2]
        return med_izq, med_der, med_ad
    
    return None, None, None

def mantener_linea_recta(rumbo):
    """Aplica control PID para mantener el rumbo especificado."""
    drive.run(VELOCIDAD_AVANCE)

    yaw_actual = hub.imu.heading()
    error_rate = hub.imu.angular_velocity()[2]
    error_yaw = rumbo - yaw_actual

    # Prevención de división por cero si la velocidad angular es 0
    if error_rate != 0:
        dt = (error_yaw - pid_state["prev_error"]) / error_rate
    else:
        dt = 0.01  # Valor de fallback seguro

    pid_state["integral"] += error_yaw * dt
    pid_state["prev_error"] = error_yaw
    
    angulo_motor = (KP_YAW * error_yaw) + (KD_YAW * error_rate) + (KI_YAW * pid_state["integral"])
    
    # Límites seguros
    angulo_seguro = max(LIMITE_IZQ, min(LIMITE_DER, angulo_motor))
    steering.track_target(angulo_seguro)

    # Telemetría de consola (Restringida a 2 veces por segundo para no saturar)
    if reloj_telemetria.time() > 500:
        print(f"Yaw Actual: {yaw_actual:5.1f}°  |  Yaw Objetivo: {rumbo:5.1f}°")
        reloj_telemetria.reset()


def giro_ajuste():
    """
    Ajuste continuo y proporcional si el robot se acerca demasiado a una pared.
    No bloquea el código (sin waits ni whiles) y se integra suavemente con el PID.
    """
    # Leemos los sensores (Pybricks es rápido, esto es casi instantáneo)
    dist_izq = sensor_izq.distance()
    dist_der = sensor_der.distance()

    # --- PARÁMETROS AJUSTABLES ---
    # KP_REPULSION: Qué tan fuerte empuja el volante por cada mm que invade la zona.
    # ANGULO_MAX_ESCAPE: Límite de seguridad para que el robot no gire bruscamente.
    KP_REPULSION = 0.6 
    ANGULO_MAX_ESCAPE = 35 

    # 1. Evaluar Pared Izquierda
    # Usamos "0 < dist_izq" porque a veces los sensores fallan y devuelven 0 por error.
    if 0 < dist_izq < LIMITE_DIST_RECTO:
        
        # Calculamos cuántos milímetros hemos invadido la zona de peligro
        invasion = LIMITE_DIST_RECTO - dist_izq
        
        # Multiplicamos la invasión por el factor de repulsión (limitado al máximo seguro)
        angulo_escape = min(ANGULO_MAX_ESCAPE, invasion * KP_REPULSION)
        
        # Sobrescribimos temporalmente el motor de dirección hacia la DERECHA (positivo)
        steering.track_target(angulo_escape)
        
        # Imprimimos la advertencia sin saturar la consola
        if reloj_telemetria.time() > 500:
            print(f">> Peligro IZQ ({dist_izq}mm). Empujando volante a {angulo_escape:.1f}°")

    # 2. Evaluar Pared Derecha
    elif 0 < dist_der < LIMITE_DIST_RECTO:
        
        invasion = LIMITE_DIST_RECTO - dist_der
        angulo_escape = min(ANGULO_MAX_ESCAPE, invasion * KP_REPULSION)
        
        # Sobrescribimos temporalmente el motor de dirección hacia la IZQUIERDA (negativo)
        steering.track_target(-angulo_escape)
        
        if reloj_telemetria.time() > 500:
            print(f">> Peligro DER ({dist_der}mm). Empujando volante a -{angulo_escape:.1f}°")


def girar(diferencia, med_izq, med_der):
    """Lógica principal de giro en esquinas para circuitos rectangulares."""
    
    # 1. Determinar la dirección PERMANENTEMENTE en el primer giro
    if robot_state["seccion_actual"] == 1:
        if diferencia > 0:
            robot_state["giro_direc"] = 1 # Izquierda
        else:
            robot_state["giro_direc"] = 0 # Derecha

    # 2. Configurar parámetros mecánicos según la dirección bloqueada
    if robot_state["giro_direc"] == 1:
        direccion_texto = "Izquierda"
        angulo_giro_motor = -50  # Volante a la izquierda
        cambio_rumbo = -90
    else:
        direccion_texto = "Derecha"
        angulo_giro_motor = 50   # Volante a la derecha
        cambio_rumbo = 90

    # Calculamos a dónde tiene que llegar el giroscopio
    nuevo_objetivo = robot_state["rumbo_objetivo"] + cambio_rumbo

    # --- TELEMETRÍA ---
    print("\n" + "-"*50)
    print(">> EVALUACIÓN DE SENSORES PARA GIRO:")
    print(f"   Sensor Izquierdo: {med_izq} mm")
    print(f"   Sensor Derecho:   {med_der} mm")
    print(f"   Diferencia (Izq - Der): {diferencia} mm")
    print(f">> Iniciando giro a {direccion_texto.upper()} | Objetivo: {nuevo_objetivo}°")
    print("-" * 50 + "\n")

    # 3. Ejecutar el giro mecánico puro
    hub.speaker.volume(100)
    hub.speaker.beep(200, 100)
    
    # Forzamos el volante a la posición máxima de giro (wait=False evita que el código se pause aquí)
    steering.run_target(800, angulo_giro_motor, wait=False)
    
    # Mantenemos el motor de tracción avanzando
    drive.run(VELOCIDAD_AVANCE)

    # 4. Esperar a que la IMU (Giroscopio) detecte que completamos el giro
    yaw_actual = hub.imu.heading()
    
    if robot_state["giro_direc"] == 1:
        # Giro a la izquierda: el rumbo disminuye (ej: -90 a -180).
        # Usamos +5 grados de margen para soltar el volante un poquito antes y evitar pasarnos.
        while yaw_actual > nuevo_objetivo + 5:
            yaw_actual = hub.imu.heading()
            wait(5)
    else:
        # Giro a la derecha: el rumbo aumenta (ej: 90 a 180).
        while yaw_actual < nuevo_objetivo - 5:
            yaw_actual = hub.imu.heading()
            wait(5)

    # 5. Limpieza y consolidación de datos post-giro
    lecturas_izq.clear()
    lecturas_der.clear()
    lecturas_ad.clear()
    reloj_sensores.reset()

    # Guardamos el nuevo objetivo oficialmente. Al salir de esta función,
    # el controlador PID (mantener_linea_recta) tomará el control para alinear el robot perfectamente.
    robot_state["rumbo_objetivo"] = nuevo_objetivo


# ==========================================
# 5. BUCLE PRINCIPAL
# ==========================================
iniciar_robot()
reloj_sensores.reset()
reloj_telemetria.reset()
reloj_rot.reset()

try:
    while robot_state["seccion_actual"] <= SECCIONES_TOTALES:
        
        # 1. Parada de emergencia
        if Button.CENTER in hub.buttons.pressed():
            print(">> Parada manual solicitada por el usuario.")
            break

        # 2. Control Continuo
        mantener_linea_recta(robot_state["rumbo_objetivo"])
        giro_ajuste()

        # 3. Lectura de Sensores y Decisión
        med_izq, med_der, med_ad = leer_sensores()

        # Si tenemos lecturas válidas (el búfer se llenó)
        if med_izq is not None:
            diferencia = med_izq - med_der

            # Evaluar posibilidad de giro basado en el temporizador
            if reloj_rot.time() >= ROT_TIME_MIN or robot_state["cant_giros"] == 0:
                
                # Condición de giro cumplida
                if abs(diferencia) >= LIMITE_ROT:
                    
                    # Llamar a la función de giro (que se encarga de imprimir la telemetría)
                    girar(diferencia, med_izq, med_der)

                    # Actualizar contadores
                    robot_state["seccion_actual"] += 1
                    robot_state["cant_giros"] += 1
                    reloj_rot.reset()

        # Pausa del sistema para no asfixiar la CPU
        wait(5)

    # Una vez terminadas las secciones
    mover_por_mm(800,robot_state["rumbo_objetivo"])

except Exception as e:
    print("\n>> ERROR EN EJECUCIÓN:", e)

finally:
    drive.stop()
    steering.stop()
    print("\n==========================================")
    print("--- ROBOT DETENIDO ---")
    print("==========================================")
