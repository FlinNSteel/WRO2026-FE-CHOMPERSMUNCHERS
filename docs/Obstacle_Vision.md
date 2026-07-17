# Obstacle Vision
This section will be dedicated on explaining how we use the OPENMV camera to observe the enviorment around the robot and determine certain information, mostly in the **obstacle challenge** but we are also planning to implement it into the **open challenge** loop.
For this challenge, we are presenting the code in **micropython** for the **Open MV cam M7**.

---
## 1. Strategy summary
Our strategy, starting in the camera finds the area of each "blob" on the camera, these blobs are the red or green traffic signs to be avoided. To do this, first we detect where in the "priority area" it is, areas on the side are set to a value of less priority than the one in the center, where the robot is at the highest risk of of crashing into the sign.
After this, we check the color of the blob before sending the area to the hub. The hub will recieve how high the priority of the "blob" was, the color, and the amount of said color of the "blob".

When a "blob" is detected, depending on the color read, the robot will be forced to start turning slightly, this turn will last until the "blob" is completely out of sight for the robot, where it will return to the original ``manter_linea_recta_`` state or keep driving forward normally.

### 1.2 Hypothetical code

Before implementing the code, a hypothetical "test" version was used to run the code on a simulated micropython, with the input from the camera being replaced with the ``temp`` variable, which would decrease in value gradually until hitting 0, where the robot would detect that the hypothetical blob was "no longer there" and so the obstacle had "been evaded"

```
import time
is_in_sight = 1
temp = 1
color = str('red')

while is_in_sight == 1:
    if color == str('green'): 
        print('evading green block, current temp time', temp,)
    elif color == str('red'): 
        print('evading red block')
    time.sleep(0.5) #replace time with wait later
    temp -= 0.3
    if 0 >= temp:
      is_in_sight = 0
else:
    print("pillar with da color", color,"evaded sucessfully")
```
> **Note!**
> "Temp" is a temporary variable to be replaced with camera input in a hypothetical "check_priority" or "find_blob" function in the code.

The ``is_in_sight`` function determines if a blob is present or not, with it activating the turning protocol (which would go where the "evading ___" block is) if it is. This is all slipped into a ``while`` that will run until the blob is no longer in function, with the "if" only running once to check the blob's color to avoid the robot having to constantly check which color it is, which would waste cpu usage.
## 2. Camera detection

Here, we will be displaying and glossing over how "blobs" are detected in the OPENMV software, showing the ways they can determine the distance and priority of each "blob" and then send those variables directly to the hub to be used, having all the calculations already done to avoid any delay with the code.
> **Note!**
> This is all yet to be fully implemented in the actual code, as so, major changes are very likely to happen between this version and the final one implemented in the code.
### 2.1 Initial configuration
All these functions are set in the ``sensor.(config)`` format and help know the usual adjustments of the camera to run on.

* ``.reset:`` Starts the camera.
* ``.setpixformat:`` Sets the pixel format to ``RGB`` so it can load colors and detect which color each "blob" is.
* ``.set_framesize:`` It checks the resolution of the camera, big enough for it to read a clear image but not too much as to not saturate the console.
* ``.skip_frame:`` Waits a certain amount of time before the camera fully adjusts.
* ``.set_auto_exposure:`` This is set to false, as enabling it could have the exposure shift between takes depending on where it starts, instead having it set on a fixed value to minimize variation.
* ``.set_saturation:`` Sets the saturation for the camera, set a high value to ensure the colors are easy to recognize for the camera.
* ``.set_contrast:`` Sets the contrast of the camera, with a high contrast being set to let the colors be easily differenciated from parts like the white of the floor.
* ``.set_auto_grain:`` It controls light sensitivity of the camera, this was disabled as to have the value be constant to avoid having the camera "auto recalibrate".
