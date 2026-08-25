# main_vision_v3.py — visión WRO con Y/X + esquive gradual + recuperación odométrica
# Pareja OpenMV: ingenieros/openmv/vision_ing_v3.py
# Requiere: pupremote_hub.py + vision_remote_v3.py
#
# Puertos: A=volante  B=cámara  C=us der  D=us izq  E=color  F=tracción
#
# Protocolo BBBB: cmd, y_cm, x_code, meta(conf|fase_cam|critico_cam|xy_ok)
# La FASE de maniobra la decide este hub (Y_SUAVE / Y_SUAVE_CRITICO / …).
# Rojo(10)→derecha(+1)  Verde(11)→izquierda(-1)
# RECTO | ESQUIVE_* | RECUPERAR_CARRIL | GIRO_ESQUINA
# Ultrasonidos: solo protección anti-pared (NO centrado de carril)
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, UltrasonicSensor, ColorSensor
from pybricks.parameters import Port, Direction, Button, Color
from pybricks.tools import wait as wait_ms, StopWatch, run_task, multitask
from umath import sin, radians
import gc

import vision_remote_v3 as vision

print("main_vision_v3: iniciando dispositivos...")
hub = PrimeHub()
sensor_izq = UltrasonicSensor(Port.D)
sensor_der = UltrasonicSensor(Port.C)
sensor_color = ColorSensor(Port.E)
drive = Motor(Port.B, Direction.COUNTERCLOCKWISE)
steering = Motor(Port.A, Direction.CLOCKWISE)
print("main_vision_v3: dispositivos OK, conectando camara...")

print("main_vision_v3: vision lista")

# --- constantes movimiento ---
VELOCIDAD_AVANCE = 1000
VELOCIDAD_ESQUIVE = 800
# Límites físicos (calibrar_steering): min≈-69  max≈53 — margen ~5–8°
LIMITE_IZQ = -60
LIMITE_DER = 48
LIMITE_DIST_RECTO = 150
ROT_TIME_MIN = 2600
SECCIONES_TOTALES = 16
KP_YAW = 3
KD_YAW = 1
KI_YAW = 0.01
CMD_PILLAR_RED = 10
CMD_PILLAR_GREEN = 11
CONF_MIN_INICIO = 2

# --- odometría (calibrar_odometria.py) ---
DIAMETRO_RUEDA_NOMINAL_MM = 56.0
RELACION_MOTOR_A_RUEDA = 1.0
SIGNO_ENCODER_AVANCE = 1
SIGNO_IMU_DERECHA = 1
CM_POR_GRADO_MOTOR = 0.049925

# --- fases / modos hub ---
FASE_VIGILAR = 0
FASE_SUAVE = 1
FASE_ACTUAR = 2
FASE_EMERGENCIA = 3

MODO_RECTO = 0
MODO_ESQUIVE_SUAVE = 1
MODO_ESQUIVE_ACTUAR = 2
MODO_ESQUIVE_EMERGENCIA = 3
MODO_RECUPERAR = 4
MODO_GIRO_ESQUINA = 5

# --- CUÁNDO maniobrar (decidido en HUB; no hace falta tocar OpenMV) ---
# Y en cm (adelante). Más alto = empieza antes.
Y_EMERGENCIA = 18
Y_ACTUAR = 28
Y_SUAVE = 38
Y_SUAVE_CRITICO = 40   # rojo a der / verde a izq
X_CRITICO_CM = 6       # |X| para marcar lado crítico

# Ángulos de volante por fase (+ bonus crítico)
# Ajuste en pista: subir si pasa demasiado cerca; bajar si sobrevira.
ANG_SUAVE = 28
ANG_ACTUAR = 38
ANG_EMERGENCIA = 45
BONUS_CRITICO_SUAVE = 10
BONUS_CRITICO_ACTUAR = 8

# Recuperación de carril (diagonal abierta, variables de usuario)
# Tras esquive: PID a rumbo_objetivo - sentido*CORRECCION_DIAGONAL_DEG
# durante T_DIAGONAL_MS; luego PID normal a rumbo_objetivo.
#   RECUPERACION_ACTIVA=0 → tras pasar el pilar vuelve a recto sin diagonal
RECUPERACION_ACTIVA = 1
CORRECCION_DIAGONAL_DEG = 70   # grados de diagonal (editable)
T_DIAGONAL_MS = 2000            # ms en diagonal (editable)
PILLAR_SUPERADO_Y = 14
FRAMES_SIN_PILAR = 5
PERDIDA_MS = 50
Y_NUEVO_PILAR_CANCELA = 25

DEBUG = 0  # 1 = telemetría (gasta RAM)

# --- estado ---
rumbo_objetivo = 0
seccion_actual = 1
cant_giros = 0
giro_direc = -1
modo = MODO_RECTO
sentido_esquive = 0
pid_integral = 0
pid_prev_error = 0

# Odometría de maniobra
rumbo_inicio_esquive = 0.0
encoder_anterior = 0
x_estimado_cm = 0.0
vio_pilar_cerca = 0
frames_sin_pilar = 0
reloj_perdida = StopWatch()
reloj_recup = StopWatch()
en_perdida = 0
critico_actual = 0
fase_actual = 0
y_actual = 0
x_actual = 0

reloj_rot = StopWatch()
reloj_telemetria = StopWatch()
reloj_gc = StopWatch()

Color.ORANGE = Color(h=0, s=100, v=100)
Color.BLUE = Color(h=240, s=100, v=30)
# Color.YELLOW ya existe en Pybricks; no redefinir


def reset_pid():
    global pid_integral, pid_prev_error
    pid_integral = 0
    pid_prev_error = 0


def clamp(v, lo, hi):
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


def es_critico_hub(cmd, x_cm):
    """Lado que bloquea el paso WRO."""
    if cmd == CMD_PILLAR_RED:
        return x_cm > X_CRITICO_CM
    if cmd == CMD_PILLAR_GREEN:
        return x_cm < -X_CRITICO_CM
    return False


def calcular_fase_hub(y_cm, critico):
    """Decisión de fase en el hub (umbrales editables arriba)."""
    if y_cm <= Y_EMERGENCIA:
        return FASE_EMERGENCIA
    if y_cm <= Y_ACTUAR:
        return FASE_ACTUAR
    lim = Y_SUAVE_CRITICO if critico else Y_SUAVE
    if y_cm <= lim:
        return FASE_SUAVE
    return FASE_VIGILAR


def actualizar_luz():
    if modo == MODO_ESQUIVE_SUAVE:
        hub.light.on(Color.YELLOW)
    elif modo == MODO_ESQUIVE_ACTUAR or modo == MODO_ESQUIVE_EMERGENCIA:
        hub.light.on(Color.RED if sentido_esquive > 0 else Color.ORANGE)
    elif modo == MODO_RECUPERAR:
        hub.light.on(Color.ORANGE)
    elif modo == MODO_GIRO_ESQUINA:
        hub.light.on(Color.BLUE)
    else:
        hub.light.on(Color.GREEN)


def iniciar_robot():
    print("MAIN VISION v3: F=traccion B=cam BBBB")
    print(
        "Y suave/crit/act/emer=",
        Y_SUAVE, Y_SUAVE_CRITICO, Y_ACTUAR, Y_EMERGENCIA,
    )
    print(
        "diag=", CORRECCION_DIAGONAL_DEG, "deg",
        "T=", T_DIAGONAL_MS, "ms",
    )
    steering.reset_angle(0)
    hub.imu.reset_heading(0)
    drive.run(VELOCIDAD_AVANCE)
    actualizar_luz()


def mantener_linea_recta(rumbo=None):
    """PID de rumbo. Si rumbo=None usa rumbo_objetivo de sección."""
    global pid_integral, pid_prev_error
    if rumbo is None:
        rumbo = rumbo_objetivo

    yaw_actual = hub.imu.heading()
    error_rate = hub.imu.angular_velocity()[2]
    error_yaw = rumbo - yaw_actual

    if error_rate != 0:
        dt = (error_yaw - pid_prev_error) / error_rate
    else:
        dt = 0.01

    pid_integral += error_yaw * dt
    pid_prev_error = error_yaw

    angulo = (KP_YAW * error_yaw) + (KD_YAW * error_rate) + (KI_YAW * pid_integral)
    angulo = clamp(angulo, LIMITE_IZQ, LIMITE_DER)
    steering.track_target(angulo)

    if DEBUG and reloj_telemetria.time() > 1000:
        print("yaw", int(yaw_actual), "obj", int(rumbo), "xest", int(x_estimado_cm))
        reloj_telemetria.reset()


async def giro_ajuste():
    """Solo emergencia de pared; NO centrado de carril."""
    dist_izq = await sensor_izq.distance()
    dist_der = await sensor_der.distance()
    if dist_izq > 0 and dist_izq < LIMITE_DIST_RECTO:
        angulo = (LIMITE_DIST_RECTO - dist_izq) * 0.6
        if angulo > 35:
            angulo = 35
        steering.track_target(angulo)
    elif dist_der > 0 and dist_der < LIMITE_DIST_RECTO:
        angulo = (LIMITE_DIST_RECTO - dist_der) * 0.6
        if angulo > 35:
            angulo = 35
        steering.track_target(-angulo)


def actualizar_odometria():
    """Integra x_estimado_cm con encoder + IMU (signos calibrados)."""
    global encoder_anterior, x_estimado_cm
    enc_now = drive.angle()
    delta = SIGNO_ENCODER_AVANCE * (enc_now - encoder_anterior)
    encoder_anterior = enc_now
    ds = delta * CM_POR_GRADO_MOTOR
    theta = radians(SIGNO_IMU_DERECHA * (hub.imu.heading() - rumbo_inicio_esquive))
    x_estimado_cm += ds * sin(theta)


def iniciar_esquive(cmd, fase, critico, y_cm=0, x_cm=0):
    global modo, sentido_esquive
    global rumbo_inicio_esquive, encoder_anterior, x_estimado_cm
    global vio_pilar_cerca, frames_sin_pilar, en_perdida, critico_actual

    sentido_esquive = 1 if cmd == CMD_PILLAR_RED else -1
    critico_actual = 1 if critico else 0
    rumbo_inicio_esquive = hub.imu.heading()
    encoder_anterior = drive.angle()
    x_estimado_cm = 0.0
    vio_pilar_cerca = 0
    frames_sin_pilar = 0
    en_perdida = 0
    reset_pid()
    drive.run(VELOCIDAD_ESQUIVE)

    if fase >= FASE_EMERGENCIA:
        modo = MODO_ESQUIVE_EMERGENCIA
    elif fase >= FASE_ACTUAR:
        modo = MODO_ESQUIVE_ACTUAR
    else:
        modo = MODO_ESQUIVE_SUAVE

    actualizar_luz()
    aplicar_esquive(fase, critico_actual)
    nombre = "ROJO" if cmd == CMD_PILLAR_RED else "VERDE"
    print(
        "ESQUIVE ON", nombre,
        "Y=", y_cm, "cm",
        "X=", x_cm, "cm",
        "fase=", fase,
        "crit=", critico_actual,
    )


def aplicar_esquive(fase, critico):
    if fase >= FASE_EMERGENCIA:
        base = ANG_EMERGENCIA
        bonus = 0
    elif fase >= FASE_ACTUAR:
        base = ANG_ACTUAR
        bonus = BONUS_CRITICO_ACTUAR if critico else 0
    else:
        base = ANG_SUAVE
        bonus = BONUS_CRITICO_SUAVE if critico else 0

    angulo = sentido_esquive * (base + bonus)
    angulo = clamp(angulo, LIMITE_IZQ, LIMITE_DER)
    steering.track_target(angulo)


def actualizar_modo_esquive(fase):
    global modo
    if fase >= FASE_EMERGENCIA:
        nuevo = MODO_ESQUIVE_EMERGENCIA
    elif fase >= FASE_ACTUAR:
        nuevo = MODO_ESQUIVE_ACTUAR
    elif fase >= FASE_SUAVE:
        nuevo = MODO_ESQUIVE_SUAVE
    else:
        # En vigilar pero aún en maniobra: mantener suave si no hemos pasado
        nuevo = modo
        if modo < MODO_ESQUIVE_SUAVE or modo > MODO_ESQUIVE_EMERGENCIA:
            nuevo = MODO_ESQUIVE_SUAVE
    if nuevo != modo:
        modo = nuevo
        actualizar_luz()


def iniciar_recuperacion():
    global modo, en_perdida, frames_sin_pilar
    modo = MODO_RECUPERAR
    en_perdida = 0
    frames_sin_pilar = 0
    reset_pid()
    drive.run(VELOCIDAD_AVANCE)
    reloj_recup.reset()
    actualizar_luz()
    # sentido_esquive se conserva: diagonal = sentido contrario
    
    rumbo_diag = rumbo_objetivo - sentido_esquive * CORRECCION_DIAGONAL_DEG
    print(
        "diagonal",
        "rumbo=", int(rumbo_diag),
        "corr=", CORRECCION_DIAGONAL_DEG,
        "ms=", T_DIAGONAL_MS,
    )


def aplicar_recuperacion():
    """PID a rumbo de sección ± diagonal (contra el sentido del esquive)."""
    rumbo_diag = rumbo_objetivo - sentido_esquive * CORRECCION_DIAGONAL_DEG
    mantener_linea_recta(rumbo_diag)


def volver_recto():
    global modo, sentido_esquive, vio_pilar_cerca, frames_sin_pilar
    global en_perdida, critico_actual
    modo = MODO_RECTO
    sentido_esquive = 0
    vio_pilar_cerca = 0
    frames_sin_pilar = 0
    en_perdida = 0
    critico_actual = 0
    reset_pid()
    drive.run(VELOCIDAD_AVANCE)
    actualizar_luz()
    print("recto")


def esta_esquivando():
    return (
        modo == MODO_ESQUIVE_SUAVE
        or modo == MODO_ESQUIVE_ACTUAR
        or modo == MODO_ESQUIVE_EMERGENCIA
    )


def actualizar_modo_vision(cmd, y_cm, x_cm, conf, fase, critico, xy_ok):
    global modo, sentido_esquive, vio_pilar_cerca, frames_sin_pilar
    global en_perdida, critico_actual, fase_actual, y_actual, x_actual

    fase_actual = fase
    y_actual = y_cm
    x_actual = x_cm

    if modo == MODO_GIRO_ESQUINA:
        return

    pilar_ok = (
        xy_ok
        and conf >= CONF_MIN_INICIO
        and (cmd == CMD_PILLAR_RED or cmd == CMD_PILLAR_GREEN)
    )

    # --- RECTO: iniciar esquive ---
    if modo == MODO_RECTO:
        if pilar_ok:
            # Distancia al pilar más cercano (cámara) mientras se acerca
            if reloj_telemetria.time() > 300:
                nombre = "ROJO" if cmd == CMD_PILLAR_RED else "VERDE"
                print(
                    "pilar", nombre,
                    "Y=", y_cm, "cm",
                    "X=", x_cm, "cm",
                    "fase=", fase,
                    "conf=", conf,
                )
                reloj_telemetria.reset()
            if fase >= FASE_SUAVE:
                iniciar_esquive(cmd, fase, critico, y_cm, x_cm)
        return

    # --- RECUPERAR: diagonal un tiempo, luego recto ---
    if modo == MODO_RECUPERAR:
        # Nuevo pilar cerca cancela la diagonal
        if pilar_ok and y_cm <= Y_NUEVO_PILAR_CANCELA and fase >= FASE_SUAVE:
            iniciar_esquive(cmd, fase, critico, y_cm, x_cm)
            return
        aplicar_recuperacion()
        if reloj_recup.time() >= T_DIAGONAL_MS:
            volver_recto()
        return

    # --- ESQUIVE ---
    if esta_esquivando():
        actualizar_odometria()

        if pilar_ok:
            frames_sin_pilar = 0
            en_perdida = 0
            critico_actual = 1 if critico else 0
            if cmd == CMD_PILLAR_RED:
                sentido_esquive = 1
            elif cmd == CMD_PILLAR_GREEN:
                sentido_esquive = -1

            if y_cm <= PILLAR_SUPERADO_Y:
                vio_pilar_cerca = 1

            actualizar_modo_esquive(fase)
            # Si la fase baja a vigilar pero seguimos viendo el pilar,
            # usar el modo actual para no suavizar de golpe.
            fase_cmd = fase
            if fase_cmd < FASE_SUAVE:
                if modo == MODO_ESQUIVE_EMERGENCIA:
                    fase_cmd = FASE_EMERGENCIA
                elif modo == MODO_ESQUIVE_ACTUAR:
                    fase_cmd = FASE_ACTUAR
                else:
                    fase_cmd = FASE_SUAVE
            aplicar_esquive(fase_cmd, critico_actual)
        else:
            # Sin detección estable
            frames_sin_pilar += 1
            if en_perdida == 0:
                en_perdida = 1
                reloj_perdida.reset()

            # Mantener ángulo según modo mientras esperamos pérdida estable
            if modo == MODO_ESQUIVE_EMERGENCIA:
                fase_hold = FASE_EMERGENCIA
            elif modo == MODO_ESQUIVE_ACTUAR:
                fase_hold = FASE_ACTUAR
            else:
                fase_hold = FASE_SUAVE
            aplicar_esquive(fase_hold, critico_actual)

            perdio = (
                frames_sin_pilar >= FRAMES_SIN_PILAR
                or reloj_perdida.time() >= PERDIDA_MS
            )
            if vio_pilar_cerca and perdio:
                if RECUPERACION_ACTIVA:
                    iniciar_recuperacion()
                else:
                    # Validación sin recuperación: volver a recto tras pasar
                    volver_recto()
            elif (not vio_pilar_cerca) and perdio and fase_actual == FASE_VIGILAR:
                # Falsa alarma / faro perdido lejos: volver a recto
                if frames_sin_pilar >= FRAMES_SIN_PILAR + 2:
                    volver_recto()


async def girar_esquina(diferencia):
    global modo, rumbo_objetivo, giro_direc, sentido_esquive
    global vio_pilar_cerca, frames_sin_pilar, en_perdida, x_estimado_cm

    modo = MODO_GIRO_ESQUINA
    actualizar_luz()

    if giro_direc < 0:
        giro_direc = 1 if diferencia > 0 else 0

    if giro_direc == 1:
        angulo_volante = LIMITE_IZQ
        cambio_rumbo = -90
    else:
        angulo_volante = LIMITE_DER
        cambio_rumbo = 90

    nuevo = rumbo_objetivo + cambio_rumbo
    print("giro esquina ->", nuevo)
    hub.speaker.beep(200, 80)
    steering.track_target(angulo_volante)

    yaw = hub.imu.heading()
    if giro_direc == 1:
        while yaw > nuevo + 20:
            yaw = hub.imu.heading()
            await wait_ms(5)
    else:
        while yaw < nuevo - 20:
            yaw = hub.imu.heading()
            await wait_ms(5)

    rumbo_objetivo = nuevo
    sentido_esquive = 0
    vio_pilar_cerca = 0
    frames_sin_pilar = 0
    en_perdida = 0
    x_estimado_cm = 0.0
    reset_pid()
    drive.run(VELOCIDAD_AVANCE)
    modo = MODO_RECTO
    actualizar_luz()


async def loop_robot():
    global seccion_actual, cant_giros

    iniciar_robot()
    reloj_telemetria.reset()
    reloj_rot.reset()
    reloj_gc.reset()

    try:
        while seccion_actual <= SECCIONES_TOTALES:
            if Button.CENTER in hub.buttons.pressed():
                print("stop")
                break

            cmd, y_cm, x_code, meta = await vision.get_vision_data()
            conf, _fase_cam, _crit_cam, xy_ok = vision.unpack_meta(meta)
            x_cm = vision.decode_x(x_code)

            # Fase/crítico los decide el HUB (umbrales Y_* / X_CRITICO_CM)
            critico = 0
            fase = FASE_VIGILAR
            if xy_ok and (cmd == CMD_PILLAR_RED or cmd == CMD_PILLAR_GREEN):
                critico = 1 if es_critico_hub(cmd, x_cm) else 0
                fase = calcular_fase_hub(y_cm, critico)

            actualizar_modo_vision(cmd, y_cm, x_cm, conf, fase, critico, xy_ok)

            if modo == MODO_RECTO:
                mantener_linea_recta()
                await giro_ajuste()

                # Giro de esquina por color DESACTIVADO (prueba sin mapa)
                # if reloj_rot.time() >= ROT_TIME_MIN or cant_giros == 0:
                #     color = await sensor_color.color()
                #     if color == Color.BLUE:
                #         print("color detectado: BLUE -> giro izq")
                #         await girar_esquina(1)
                #         seccion_actual += 1
                #         cant_giros += 1
                #         reloj_rot.reset()
                #     elif color == Color.RED:
                #         print("color detectado: RED -> giro der")
                #         await girar_esquina(0)
                #         seccion_actual += 1
                #         cant_giros += 1
                #         reloj_rot.reset()

            # En esquive/recuperación el control ya se aplicó en actualizar_modo_vision
            # Protección de pared también en esquive suave si está muy cerca
            if esta_esquivando() or modo == MODO_RECUPERAR:
                # opcional: no llamar giro_ajuste aquí para no pelear con esquive
                pass

            if DEBUG and reloj_telemetria.time() > 500:
                print(
                    "m", modo, "cmd", cmd, "Y", y_cm, "X", x_cm,
                    "f", fase, "c", conf, "xest", int(x_estimado_cm)
                )
                reloj_telemetria.reset()

            if reloj_gc.time() > 2000:
                gc.collect()
                reloj_gc.reset()

            await wait_ms(10)

    finally:
        drive.stop()
        steering.stop()
        print("ROBOT DETENIDO")


async def main():
    await multitask(vision.process_remote(), loop_robot())


run_task(main())
