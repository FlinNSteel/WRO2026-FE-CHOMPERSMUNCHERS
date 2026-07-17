Notechoques_giroimproved_5_29_2026

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait, StopWatch

# --- INICIALIZACIÓN DE HARDWARE ---
hub = PrimeHub()

# Set up all devices.
sensor_ad = UltrasonicSensor(Port.F)                # Es el sensor de adelante
sensor_izq = UltrasonicSensor(Port.D)               # Es el sensor de izquierda
sensor_der = UltrasonicSensor(Port.C)               # Es el sensor de derecha
drive = Motor(Port.B, Direction.COUNTERCLOCKWISE)   # es el motor que conduce
steering = Motor(Port.A, Direction.CLOCKWISE)       # es el que cambia de direccion 

#Clock
reloj = StopWatch()

# Variables
velocidad_base = 800
limit_der = -89     # limite de giro derecha
limit_izq = 66      # limite de giro izquierda
angulo_steering_recto = 10
transformacion = 0


# --- PARÁMETROS DE CONFIGURACIÓN ---
VELOCIDAD_AVANCE = velocidad_base # Grados por segundo del motor de tracción
RUMBO_OBJETIVO = 0      # Queremos mantenernos en 0 grados (línea recta)

# Ganancias del control de rumbo (Ajustables)
KP_YAW = 3
KD_YAW = 1
error_yaw = 0

# Valores de componente integral
KI_YAW = 0.01
dt = 0
previous_error = 0
error_integral = 0

# Límites físicos estrictos del motor para evitar sobreesfuerzos
LIMITE_IZQ = -47
LIMITE_DER = 67
LIMITE_ROT = 1000
LIMITE_AD = 80
LIMITE_FR = 530 # Cantidad de cm que necesita el robot (Censor de frente) a pared para girar


def Mover_por_mm(distancia_en_mm, velocidad_base = 500):
    global transformacion
    transformacion = (distancia_en_mm * 360) / (62*3.1416)
    drive.run_angle(velocidad_base, transformacion)

def iniciar_robot():
    print("--- CONTROL DESDE 0: AVANCE RECTO ---")
    # IMPORTANTE: Pon las ruedas perfectamente rectas antes de dar PLAY
    steering.run_target(800,angulo_steering_recto)
    steering.reset_angle(0)
    hub.imu.reset_heading(0)
    drive.run(VELOCIDAD_AVANCE)

# def adignore: #esto probablemente falle pq esta en prueba

def girar(diferencia):

    if (diferencia > 0):
        drive.stop()
        # giro esta calibrado, horray!
        steering.run_target(500, -32)

        yaw_actual = hub.imu.heading()
        
        while abs(yaw_actual) < 88:
            yaw_actual = hub.imu.heading()
            drive.run(800)
        
        drive.stop()
        steering.run_target(900, angulo_steering_recto)
        Mover_por_mm(100)
    else:
        drive.stop()
        # giro esta calibrado, horray!
        yaw_actual = hub.imu.heading()
        steering.run_target(500, 32)
        
        while abs(yaw_actual) < 88:
            yaw_actual = hub.imu.heading()
            drive.run(800)
        
        drive.stop()
        steering.run_target(900, angulo_steering_recto)
        Mover_por_mm(100)
    return
    

def mantener_linea_recta():
    global error_yaw
    global error_integral
    drive.run(VELOCIDAD_AVANCE)

    previous_error = error_yaw  #Eo

    # 1. Leer variables del giroscopio interno del Hub
    yaw_actual = hub.imu.heading()
    error_rate = hub.imu.angular_velocity()[2] # Velocidad de rotación en el eje Z/Va


    # 2. Calcular error de rumbo (Cuánto nos hemos desviado del 0)
    error_yaw = RUMBO_OBJETIVO - yaw_actual # E: error

    # dt = (E-Eo)/Va

    dt = (error_yaw  - previous_error)/error_rate

    error_integral += error_yaw * dt
    
    # 3. Calcular los grados que debe moverse el motor de dirección (Control PD)
    #angulo_motor = (KP_YAW * error_yaw) - (KD_YAW * error_rate)
    
    angulo_motor = KP_YAW * error_yaw + KD_YAW * error_rate + KI_YAW*error_integral

    # =========================================================================
    # PRUEBA DE INVERSIÓN CRÍTICA:
    # Si notas que el robot se desvía un poco y en lugar de corregir gira MÁS
    # hacia ese error, quita el símbolo '#' de la línea de abajo para invertirlo:
    # angulo_motor = -angulo_motor
    # =========================================================================
    
    # 4. Filtrar el ángulo con límites seguros para que el motor no sufra
    angulo_seguro = angulo_motor
    if angulo_seguro > LIMITE_DER: angulo_seguro = LIMITE_DER
    if angulo_seguro < LIMITE_IZQ: angulo_seguro = LIMITE_IZQ
    
    # 5. Ordenar el movimiento al motor de dirección
    steering.track_target(angulo_seguro)
    
    # Telemetría en consola para diagnóstico rápido
    
    if reloj.time() % 200 < 20:
        print('yaw:', round(yaw_actual,2),'e:', round(error_yaw,2), 'dt:', round(dt,2), 'Va',error_rate,
              'ang:', angulo_motor, 'ang_s', angulo_seguro, 'ang_R',steering.angle())
        
# --- BUCLE PRINCIPAL ---
iniciar_robot()

try:
    while True:

        # Detener con el botón central si es necesario
        if Button.CENTER in hub.buttons.pressed():
            break

        diferencia = 0
        n = 10
        diferencia_acumulada = 0
        distancia_adelante = 0


        
        for i in range (n):
            dist_ad = sensor_ad.distance()
            dist_izq = sensor_izq.distance()
            dist_der = sensor_der.distance()

            distancia_adelante += dist_ad
            diferencia_acumulada += dist_izq - dist_der
            wait(10)
            

        diferencia = diferencia_acumulada/n
        distancia_adelante = distancia_adelante/n

        #agregar or distancia_adelante < LIMITE_AD
        # print('Distancia restante: ', distancia_adelante, 'Target value:', RUMBO_OBJETIVO, 'Censor YAW', hub.imu.heading(), )

        
        mantener_linea_recta()
        
    





        
        if abs(diferencia) < LIMITE_ROT:
            print("distancia es:", diferencia)
            mantener_linea_recta()
        else:
            # print("distancia es:", diferencia, "parar")
            girar(diferencia)
            diferencia = 0
            RUMBO_OBJETIVO =+ 90
            print ('Nuevo rumbo:' + str(RUMBO_OBJETIVO))
        
        


        wait(10)



except Exception as e:
    print("Error en ejecución:", e)

finally:
    # Apagado total de seguridad
    drive.stop()
    steering.stop()
    print("--- ROBOT DETENIDO ---")

