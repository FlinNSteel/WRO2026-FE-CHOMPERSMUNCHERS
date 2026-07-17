## Obstacle Vision

This section will be dedicated on explaining how we use the OPENMV camera to observe the enviorment around the robot and determine certain information, mostly in the **obstacle challenge** but we are also planning to implement it into the **open challenge** loop.
For this challenge, we are presenting the code in **micropython** for the **Open MV cam M7**. 
---
## 1. Strategy summary
Our strategy, starting in the camera finds the area of each "blob" on the camera, these blobs are the red or green traffic signs to be avoided. To do this, first we detect where in the "priority area" it is, areas on the side are set to a value of less priority than the one in the center, where the robot is at the highest risk of of crashing into the sign.
After this, we check the color of the blob before sending the area to the hub. The hub will recieve how high the priority of the "blob" was, the color, and the amount of said color of the "blob".

When a "blob" is detected, depending on the color read, the robot will be forced to start turning slightly, this turn will last until the "blob" is completely out of sight for the robot, where it will return to the original ``manter_linea_recta_`` state or keep driving forward normally.

### 1.2 Hypothetical code

Before implementing the code, a hypothetical "test" version was used to run the code on a simulated micropython, with the input from the camera being replaced with the ``temp`` variable, which would decrease in value gradually until hitting 0, where the robot would detect that the hypothetical blob was "no longer there" and so the obstacle had "been evaded"

``
import time
is_in_sight = 1
temp = 1
color = str('red')

while is_in_sight == 1:
    if color == str('green'): ## greeennnn :]>
        print('evading green block, current temp time', temp,)
    elif color == str('red'): #rrredddd *u*
        print('evading red block')
    time.sleep(0.5) #replace time with wait later
    temp -= 0.3
    if 0 >= temp:
      is_in_sight = 0
else:
    print("pillar with da color", color,"evaded sucessfully")
``
