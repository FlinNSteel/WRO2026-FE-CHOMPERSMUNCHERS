# Software architecture
This section will go into detail on how the code works, including **firmware**, libraries and **modular functions** run in the code to make it work. This code is implemented in **micropython** for the Large Hub for SPIKE™ Prime from the (now retired) lego technic series and for the **Open MV cam M7**.

---

## 1. Libraries used
### Main Pybricks code
* **``pybricks.hub:``** The standard library for all hubs coded with pybricks.
* **``pybricks.pupdevices:``** Imports all the functions for sensors and motors, ensuring that we can detect them being connected to the hub.
* **``pybricks.parameters:``** The standard pybricks library to be able to indicate how censors move, such as orientation, when to start or stop and so on.
* **``pybricks.tools:``** Mostly used to extract time related tools like **wait** and **Stopwatch**, which would allows us to be able to set small waits to avoid overwhelming CPUs and make actions be available to be executed after certain time limits such as the ``ROT_TIME_MIN``.

> **Note!**
> As you may have noticed, most of these libraries fall under the **pybricks** umbrella, this is because **micropython** is very limited when it comes to importing any external libraries and so we decided to try to do our code with as little reliance on anything outside of base python as we could.

### Camera code

* **``sensor:``** Works as a "settings" of sorts, letting us disable automatic adjusting of the camera in favor of a set brightness, contrast and saturation to ensure a consistent image being projected to the camera, making us have to do less calibrating since it is all done by hand.
* **``image:``** Lets us use commands like ``find.blobs`` to track any visual input given by the camera to turn into feedback for the hub.
* **``time:``** Allowed us to do waits on the code to avoid saturating cpu and increasing perfomance by having it not constantly run everything.

---
> **Note!** As you may have noticed, most of these libraries fall under the **pybricks** or **OpenMV** (any built in library for the hardware used) umbrella, this is because **micropython** is very limited when it comes to importing any external libraries and so we decided to try to do our code with as little reliance on anything outside of base python as we could.
---
## 2. Modular functions

This will go into detail with the **firmware** and **custom functions** made to be able to complete each one of the functions of the robot, these will be displayed in the guide below by category.

### 2.1 lalalalalala
* *italics:* Any function in *i* has yet to be finished, its either being worked on currently or planned to be done in the future, this section will stop being updated after the competition ends.
* **bold:** Any function in **b** is custom, meaning that it wasn't picked out of any library and you'll most likely have to look at the given description for since it isn't shown on any external documentation.
* ``script:`` Any function in **s** is one that's in consideration to be redesigned or deleted entirely in the code, this section will stop being updated after the competition ends.

> **Note!**
> Once a function is deleted, all records of will also disappear from the github except for mentions of it in the [legacy](src/legacy) folder, as we do not think it is as important to go into detail about functions that do not exist anymore.
### 2.2 Reading Functions
These functions include everything that does not directly make the robot move but help determine how actions will play out.
| function name | function description |
| --- | --- |
| **leer_sensores** | This function allows for a constant reading of the sensors while filtering out any jaggies to minimize the rate of false positives as much as possible and avoid overcrowing the cpu by having it clear the censors constantly after every reading. |
### 2.3 Action Functions
These functions will make the robot do a certain action with the context provided from the **reading functions** (check above).
| function name | function description |
| --- | --- |
| **mover_por_mm** | This function turns the **degrees** from the robot's drive (which acts as some sort of rotatory motor) to **mm** (distancia_in_mm * 360) / (62 * 3.1416) with 62mm being the wheel's size, after this, the signal is sent to the motor so it can move, its not ideal for constant movement but works for more precise matters like adjusting or parking|
| ``girar`` | after being given the **turn angle** in the first turn (check 2.2 State functions), it will force the steering to that degree and start driving a "straight" line (or curved to our eyes) while constantly measuring gyro measures, it will stop once the gyro detects a full 90 degree has been done and will set the current position as the new heading by adding or reducing to the number depending on the direction in which the robot is turning (check 2.2 State functions). In the first instance of a turn, the ``girar()`` measure will be able to check which side the robot is turning to, using this to determine the "state" it has to be in, which will choose things like the degree of turn for every other big turn afterwards with a variable called "giro_direc" that can be either 0 or 1. |
| **giro_ajuste** | this will go smaller "turns" when the robot gets too close to a wall to avoid bumping on both sides, by calculating the amount of mm we need to get out with our sensor difference (limit - current_distance) and then turning that into degrees before forcing the robot to see in that direction until it the difference in the sensors does not surpass the limit of distance.|
| steering.run_target | It will force the steering of the angular motor (my setting it quickly to a specific position) to make the robot turn to a specific direction, run is used to avoid the "smooth acceleration" that would be used with other turning functions as to make the turns quicker as the robot is able to handle harsh turns.|
| drive.run | This function will cause the drive motor to run for an indefinite amount of time at a certain speed until the ``drive.stop`` function is set, you cannot set an angle or time for the run during the function instead having to set them all before or after with functions like ``wait`` and ``steering.run_target``|
| **mantener_linea_recta** | if it notices it's not the set "direction" that it should be, it will calculate the angle to return to the "ideal" state without interrupting any other function by relying on PID instead of an on-off mechanism.|

