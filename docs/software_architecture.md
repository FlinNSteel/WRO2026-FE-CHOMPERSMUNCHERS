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

### 2.1 brief guide
* *italics:* Any function in *i* has yet to be finished, its either being worked on currently or planned to be done in the future, this section will stop being updated after the competition ends.
* **bold:** Any function in **b** is custom, meaning that it wasn't picked out of any library and you'll most likely have to look at the given description for since it isn't shown on any external documentation.
* ``script:`` Any function in **s** is one that's in consideration to be redesigned or deleted entirely in the code, this section will stop being updated after the competition ends.

> **Note!**
> Once a function is deleted, all records of will also disappear from the github except for mentions of it in the [legacy](src/legacy) folder, as we do not think it is as important to go into detail about functions that do not exist anymore.
### 2.2 State Functions
txt
### 2.3 Precaution Functions
txt
### 2.5 Mobility Functions
| function name | function description |
| --- | --- |
| **mover_por_mm** ||
| **leer_sensores** ||
| **girar** ||
| steering.run_target ||
| drive.run ||


<small> (Hi there! for me later, remember to separate the functions in: Mobility (how does the robot move, like the rlly basic stuff), precautions (anything the robot has to do to avoid being stuck in a certain position) and state (anything done before actions to make everything work well like leer sensores and robot state stuff), functions can be in more than 1 section at once if necessary but don't overuse it.) </small>
