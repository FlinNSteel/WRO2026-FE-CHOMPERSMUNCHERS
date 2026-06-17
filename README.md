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

Despite the fact that no one was stuck to a specific role, there were things some of us excelled at and as so did for most of our time.

### Leonardo Cubeddu

He was in charge of all things coding, making sure that our code was able to work reliably and nudging the little software details to ensure everything was right on track, besides that he also helped a lot with adjusting the robot and ensuring that we didn't wreck the robot doing tasks like replacing the battery.

*Born*: 2010, Venezuelan

### Ana Lozano

She was mostly in charge of documentation, making every change be noted and ensuring that everyone was always up to date with what to do, may it be by looking up rules when needed or keeping a record of all changes done during each meeting.

*Born*: 2010, Panamenian

### Verónica Perozo 

She was in charge of everything mechanical, doing tweaks and adjustments may it be to the design of the robot to optimize for speed or checking around things like PID to ensure that the robot was always running smoothly and having the best performance it could have.

*Born*: 2011, Venezuelan

### Dwight Sutherland

Dwight is our mentor, he guides us along the way laying the basics for everything we do and making sure we can make the most out of what we have, checking our work and correcting us when needed to ensure that we are on the right path.

*Born*: 2001, Panamenian
 
## Robot overview ⚙️
For our robot, we were aiming for a beginner friendly yet functional design, which is why we used the help of **Pybricks** and **Lego SPIKE** to develop our machine. This was done because, despite the fact we wanted to learn as much as possible, topics like wiring and electronics requiered a skill level we would need more time to reach than we had and we wanted to have the machine working in its best form for the time of the competition as much as we wanted to learn from making it.

<img src="https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/main/v-photos/right-view.jpg?raw=true" width="50%" height="50%">

## Mechanical Systems 🛠️

### Why lego?
As an up and coming team, there was bound to be a lot of trial and error with basic concepts which would mean lots of prototyping on parts that seemed "simple" or "basic". Which is why the lego "Spike" kit was ideal for us, with lego providing a solid toolset with all the basic materials needed for the robot along with the proper flexibility to commit any changes needed on the fly, we are planning in the future to pivot towards more professional hardware such as switching out the lego hub for a raspberry or audino, however lego ended up being the best option for the time being since most of the team members had little to no expirience with electronics, making this is a perfect opportunity to ensure a decent amount of customizability without overwhelming any of the members with details like learning breadboards or soddering.

### Basic Structure and framing
We aimed to make the robot as lightweight as possible while still not compromising on stability, which would be crucial specially at higher speeds as the challenge went on and more optimizations were added. For this we connected a "main frame" of sorts to the bottom of a hub to act as an anchor for all the other parts of the robot, with side parts like the sensors being placed directly on the sides connected to technic beams as to make sure they did not interfere with any of the drive's business. The structure uses long beams, cross connectors, and double supports to reduce flexing when the robot turns or changes direction. This helps prevent the chassis from deforming under the approximate weight of 1.34 kg.

We were not too worried on trying to make it so that our robot could hit a full 360 on rotations, as there were very little situations during the challenge where we saw that we would need an inmideate turn beyond 90 degrees, instead opting for an ackermann steering (more details below). This mainly happened as our drive motor and steering motor were relatively the same (as they were the type of motors provided by the kit), however with one having the angle repourposed to become a built in encoder of sorts which was especially helpful during segments like parking where maximum precision was needed, although we didn't try too hard to get a full specialized encoder made specifically for that purpose as it was not used enough for that to make too much of a difference.

### Ackermann steering

As our robot has limited power to use with the wheel, ackermann sterring permitted us to be able to invest as much of that power as possible fueling every turn and letting as much of that power be invested in just two of the wheels (resulting in more power by result) instead of having to try to get the motor to feed every single wheel at a time. To further add speed to this setup, we opted for a gear up mechanism, with this being the best way to increase speed as much as possible without compromising on weight or not adding too many things as to not overwhelm the motors.

<img src="https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/main/Other/Ackermann-steering-sketch.png?raw=true">

This ~3:1 reduction between gears cascading downwards towards the motor (from largest to smallest) allowed for a lot less work to be needed from the motor and so a much smoother and quicker robot.

<img src="https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/main/other/guided-back-view.png?raw=true" width="50%" height="50%">
      *Guided back view of the robot, the gears are right behind the "drive motor" area".
      
## Software design and strategy 💻

- **Programming language:** Pybricks micropython for rapid development and testing
- **Development interphase:** Bluetooth connection from the computer using the program to lego SPIKE hub
- **Libraries used:** Pybricks base library
### loading up the code

To access the code, the .py archive is opened inside of the pybricks website with the "code with python" option, fully replacing the templace since the libraries that come included with the software are already included inside of the code. It is reccomended this device being used has an easy acess to a good bluetooth connection as it is critical to test the code, for testing changes a "copy" system was used where various copies of the codes were made for every major change and tagged on the documentation.

### Command based parking

<img src="https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/main/other/Parking.gif" alt="parking" width="50%" height="50%">

- We based our parking on the *pybricks* system by making a series of commands for the basic actions of **steering** and **moving**, with variables set to control the turn angle, intensity of the movement and distance covered.

- We is use the sensor to detect the distance in the two side (left,right) when it detects which one is the farthest it will activate one of the two codes
  
- If right is the farthest it will go and exit right if left is the farthest then it will exit left

### Open Challenge Core loop

### Main loop flow chart ➿

      Original file in [other's](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/tree/main/other) tab
<img src="https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/main/other/main-loop-chart.png?raw=true" width="50%" height="50%">

Our core loop consist of a relatively simple but effective "mantener_linea_recta" function, which guides the robot to stay as aligned to its initial position which is measured by our gyro, with it reseting to 0 at the start of the round and then trying to maintain itself as close to 0 with the help of our PID.

#### PID

Our PID is what keeps the robot stable, which we integrated into the code's "mantener_linea_recta" function with a series of formulas to calculate how far the robot deviated and how big the oscilation has to be to ensure the robot stays as stable as possible.

```
    if error_rate != 0:
        dt = (error_yaw - pid_state["prev_error"]) / error_rate
    else:
        dt = 0.01  # Valor de fallback seguro

    pid_state["integral"] += error_yaw * dt
    pid_state["prev_error"] = error_yaw
    
    angulo_motor = (KP_YAW * error_yaw) + (KD_YAW * error_rate) + (KI_YAW * pid_state["integral"])
```

With this, we simply ran that value through our PID variables (which we obtained through rigorous testing) to have it determine how much does the steering motor have to turn to be able to correct the flaw.

### Turning

The first turn is used as a "template" of sorts for every other turn between two sections to happen through any lap, setting a "robot state" which stays unaltered for the rest of the lap's duration as to avoid having the robot accidentally turn the opposite way, this was done as a measure to force the robot to minimize the amount of mistakes it could make and having the robot become slightly independent from the sensors for the rest of the laps as they're relatively prone to give errors in the form of jaggies which could affect performance.

```

    if actual-section == 1:
        if diferencia > 0:
         robot state = turn left
        else:
         robot state = turn right
   else

```

When the first turn is finished, a timer is started to be taken into account which measures ~3.5 seconds (3500 milliseconds) and completely blocks any turns between two sections unless the timer is finished, with this being used to further ensure no jaggies affect robot performance or avoid any false positives in the odd case it accidentally reads a big difference while doing tasks like adjusting during a section. When the timer is over and a big difference is detected yet again, the robot will shift its gyro objective, adding or subtracting 90 depending on the "robot state" established on the first turn.


```

if rotation-timer < 3500:
   if difference > 1000:
      if robot state > 0:
         add 90 to objective
         go to objective
      else
         add -90 to objective
         go to objective
else

```


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
