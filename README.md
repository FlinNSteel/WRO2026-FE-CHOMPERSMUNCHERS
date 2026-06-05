# WRO2026-FE-ChompersMunchers
Chompers Munchers is a Panama based team comprised of three students which aim to learn the most of what is possible with our skillsets and aim to learn even more along the way, we are participating in the "WRO FE 2026: Self Driving Cars" challenge. In this documentation you'll be able to find everything about the team and robot, from details on each members to the creations and composition of Notechoques.

## Overview of the repository 📋
[**1. Meet the Munchers!**](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS#meet-the-munchers)

[**2. Robot Overview**](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS#robot-overview)

   [2.1 Mechanical Systems](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS#mechanical-systems)

   [2.2 Command Based Parking](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS#command-based-parking)

[**3. Robot Structure**](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS#robot-structure)

   [3.1 Robot Dimensions](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS#robot-dimensions)

   [3.2 Robot Materials](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS#robot-materials)

## Meet the munchers! 🙌
We can't exactly label anyone with a specific role, as we kind of had every role at once, with everyone helping to build prototypes, code the robot and make sure the robot didn't blow up.
### Leonardo Cubeddu
I worked on the code for the robot and had my hand in the making of "NoTeChoques" (our robot's nickname).Aside from that, my last name is pronounced koo-BEH-doo so please pronounce it right 
*Born*: 2010, Venezuelan
### Ana Lozano
My main job relies on the documentation and research for making the robot come to life, anything from checking rules thousands of times to testing the robot's parameters to make the coding expirience smoother for everyone else on the team.
*Born*: 2010, Panamenian
### Dwight Sutherland
Dwight is our mentor, he guides us along the way laying the basics for everything we do and making sure we can make the most out of what we have.
*Born*: 2001, Panamenian
***
Things we have to put:
- Photos and media of the robot and the team, include videos of robot driving
- Description of how robot works or at least what we did. 
- Code commits like justin case.
 
## Robot overview ⚙️
For our robot, we were aiming for a beginner friendly yet functional design, which is why we used the help of **Pybricks** and **Lego SPIKE** to develop our machine. This was done because, despite the fact we wanted to learn as much as possible, topics like wiring and electronics requiered a skill level we would need more time to reach than we had and we wanted to have the machine working in its best form for the time of the competition as much as we wanted to learn from making it.

(PONER OTRA VEZ A NOTECHOQUES DESPUES DE MEJORAR EL MEDIA)


### Mechanical Systems 

The robot's steering system was made with mechanical differential drive, with gears ensuring maximum customizability of the robot's speed for the wheels, the steering was done with an acherman directional in the front of the vehicle, with the back being hooked up to a rotatory motor which allows it to quickly adjust the speed of the robot, at least enough for it to do everything we need it to.

### Command based parking
<img src="https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/main/other/Parking.gif" alt="parking" width="50%" height="50%">

- We based our parking on the *pybricks* system by making a series of commands for the basic actions of **steering** and **moving**, with variables set to control the turn angle, intensity of the movement and distance covered.

- We is use the sensor to detect the distance in the two side (left,right) when it detects which one is the farthest it will activate one of the two codes
  
- If right is the farthest it will go and exit right if left is the farthest then it will exit left

### Open Challenge Core loop
Our core loop consist of a relatively simple but effective "mantener_linea_recta" function, which guides the robot to stay as aligned to its initial position which is measured by our gyro, with it reseting to 0 at the start of the round and then trying to maintain itself as close to 0 with the help of our PID.
#### PID
Our PID is what keeps the robot stable, which we integrated into the code's "mantener_linea_recta" function with a series of formulas to calculate how far the robot deviated and how big the oscilation has to be to ensure the robot stays as stable as possible.

>     # 1. Leer variables del giroscopio interno del Hub
    yaw_actual = hub.imu.heading()
    error_rate = hub.imu.angular_velocity()[2] # Velocidad de rotación en el eje Z/Va

```
    # 2. Calcular error de rumbo (Cuánto nos hemos desviado del 0)
    error_yaw = RUMBO_OBJETIVO - yaw_actual # E: error

    # dt = (E-Eo)/Va

    dt = (error_yaw  - previous_error)/error_rate

    error_integral += error_yaw * dt
```
In here, we acquired the values of the current yaw and the error-rate. These values are then run through to find the error integral, or how much error is happening.
```
    angulo_motor = KP_YAW * error_yaw + KD_YAW * error_rate + KI_YAW*error_integral
```
With this, we simply ran that value through our PID variables (which we obtained through rigorous testing) to have it determine how much does the steering motor have to turn to be able to correct the flaw.
#### Identifying turns
In simple terms, we have the lateral motors constantly running and set one of them to - and the other to +, causing a subtraction to happen, this is our **difference**. When this difference exceeds the limit we set, it will automatically go into "girar" or "turn" mode, where it will turn the set angle, depending on if the difference is above or below 0 to determine the direction.

```
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
```

However, to ensure that this mechanism is not accidentally triggered by the sensors (as they tend to be unreliable at times), a timer got set which works as a cooldown of sorts, only allowing turns to happen after a certain time frame has passed, if any turn related to the sensor difference values is detected beforehand, it will be blocked.

## Robot structure

### Robot Dimensions 📏

**Height**: 10CM

**Width**: 15CM

**Lenght**: 22CM

**Wheel-Diametre**: 56MM


### Robot Materials

| Materials | Material Descriptions |
|--------|--------|
| <img src="https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/main/other/Lego-Spike-Wheel.jpg" alt="Wheel" lenght="50px" width="50px"> |Lego Technic Spike wheel|
|<img src="https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/main/other/Ultra_Sonic_Sensor.jpg" alt="Sensor" lenght="50px" width="50px">|Lego Technic Spike Prime ultrasonic sensor| 
|<img src="https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/main/other/Power_Hub.jpg" alt="Lego Hub" lenght="50px" width="50px"> |Lego Spike Prime Large Hub|
|<img src="https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/main/other/Rotatory_Motor.jpg" alt="Angular Motor" lenght="50px" width="50px"> |Lego Spike Prime big angular motor|
