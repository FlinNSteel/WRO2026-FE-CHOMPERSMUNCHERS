from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor, UltrasonicSensor

# Set up all devices.
izquierda = UltrasonicSensor(Port.D)
derecha = UltrasonicSensor(Port.C)
adelante = UltrasonicSensor(Port.F)
drive = Motor(Port.B, Direction.COUNTERCLOCKWISE)
steering = Motor(Port.A, Direction.CLOCKWISE)

# Variables
velocidad_base = 500
limit_der = -89     # limite de giro derecha
limit_izq = 66      # limite de giro izquierda
transformacion = 0



def Mover_por_mm(distancia_en_mm, velocidad_base = 500):
    global transformacion
    transformacion = (distancia_en_mm * 360) / (62*3.1416)
    drive.run_angle(velocidad_base, transformacion)




def Estacionamiento_salida_izquierda():
    # The main program starts here.
    steering.run_target(500, 50)
    Mover_por_mm(-130)
    steering.run_target(500, -45)
    Mover_por_mm(300)
    steering.run_target(500, 50)
    Mover_por_mm(520)
    steering.run_target(500, -10)



def Estacionamiento_salida_derecha():
    # The main program starts here.
    steering.run_target(500,-45)
    Mover_por_mm(-120)
    steering.run_target(500, 50)
    Mover_por_mm(430)
    steering.run_target(500, -45)
    Mover_por_mm(380)
    steering.run_target(500, 20)

'''
def Estacionamiento_entrada_derecha():
    Mover_por_mm(800)
    steering.run_target(500,-45)
    Mover_por_mm(-120)
    steering.run_target(500, 50)
    Mover_por_mm(430)
    steering.run_target(500, -45)
    Mover_por_mm(380)
    steering.run_target(500, 20)
'''

    



if izquierda.distance() > derecha.distance():
    Estacionamiento_salida_izquierda()
else:
    Estacionamiento_salida_derecha()
     

#"Mover_por_mm(1000)"
# distancia entre caja y caja de de 36 cm y el robot de 24 cm"

def Estacionamiento_entrada_izquierda():
    steering.run_target(500,-50)
    Mover_por_mm(-300)
    steering.run_target(500,55)
    Mover_por_mm(-300)
    steering.run_target(500,-50)
    Mover_por_mm(120)
    steering.run_target(800, 20)
'''
steering.run_target(500, 60)
Mover_por_mm(-250)
steering.run_target(500, -50)
Mover_por_mm(-250)
steering.run_target(500,50)
Mover_por_mm(120)
steering.run_target(500, 20)
'''
'''
steering.run_target(500,-55)
Mover_por_mm(-350)
steering.run_target(500,55)
Mover_por_mm(-220)
steering.run_target(500,-50)
Mover_por_mm(160)
steering.run_target(800,40)
Mover_por_mm(-150)
steering.run_target(800,-20)
Mover_por_mm(100)
steering.run_target(800,-10)
'''
