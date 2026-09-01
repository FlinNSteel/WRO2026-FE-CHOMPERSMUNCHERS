# Obstacle Vision
This section will be dedicated on explaining how we use the OPENMV camera to observe the enviorment around the robot and determine certain information, using this information to effectively dodge obstacles effectively, we are presenting the code in **micropython** for the **Open MV cam M7**.

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
### 2.2 Threshold calibration
To calibrate the detection of the blobs, a "threshold" is used instead of a fixed RGB or HSV value, where it has a range of each one of the LAB values, which was calibrated using the built in value checker in OPENMV, the calibration process goes as follows.

* Put the object in the enviorment it will be in
* Check the "min" value
* If the "min" value of the camera is lower than the threshold's, replace it.
* Check the "max" value
* If the "max" value of the camera is higher than the threshold's, replace it.
* Repeat for each value

### 2.3 Sifting through blobs

To ensure that no false positives set off the alarm for the robot, we've built a system that is able to filter out blobs depending on certain traits which can flag them for being fake.

The first system is a check for the area, we know that realistically there should be certain scenes that the robot should (when working) not be able to see, like pillars right on its fake after the limit to turn has been set, these characteristics look something like this (in pseudocode form to focus on the actual logic):

```
# assuming that lower limit is the smallest a pillar can be and higher limit the biggest a pillar could be
if lower_limit > Detected_X_or_Y > higher_limit:
    register the pillar
else:
    return False
```

After this, we can also check how "thin" or "tall" a pillar is, items like lines might be registered as "pillars" by accident because of having a decent size although very distorded proportions, so we made a "range" of sorts that the pillar should be around, like a ratio between width and lenght, if a part does not complete this ratio at all times, it is probably not a pillar.

```
# assuming that i_ratio is the ideal ration a pillar should have on screen
if minimum_i_ratio > (height/width) > maximum_i_ratio:
    register the pillar
else:
    return False
```

The third one is a little different compared to the other two, focusing on position instead of sizes, you see, sometimes "pillar-like" blobs would be detected on the floor because of the similar color to the camera between the red of the pillars and the color of the mat lines in the corners, as to avoid the robot getting confused, we set up a system so if the hightest point of a pillar went below a certain threshold, it'd be canceled no matter what as no pillar could realistically lay that low in the camera without the robot having crashed already into it, leaving the only posible conclusion to be that its a fake pillar.

```
if y_pillar > min_y:
    register the pillar
else:
    return False
```


### 2.4 Aproximation of blob dimensions

Then would come being able to turn the values from pixels the screen can see to centimeters we can use to define how much of a concern the pillar shoulds be to the robot currently, for this we use two functions ``interp_y`` and ``interp_x``, which work as "translators" of sorts, these work in relatively similar ways, as so they'll be explained as one.

First a "calibration" of sorts was doing by recording the pixel and "cm" heights of each blob, with importance rising the closer it was to the robot. All of these values were fed into an approximation machine, for example, if a pixel height of "115" was obtained and the closest value was "110", the equivalent in cm to that would be used in the table to calculate the value, usando el cx (posicion en x) para poder determinar cualquier tipo de offset cual se podria afectar el valor total del pixel height.

This is not because we actually need to know the size of the pillar, as it never changes but it is useful to define the mode we will run the code on, this "mode" displays the urgency of the turn and so things like the speed and angle that it turns at, heere is a table of the modes among with the "height" each one has:

| Mode | "height" |
| --- | --- |
| <19 | emergency |
| <29 | act |
| <39 | slow |
| >39 | watch |

You might be asking yourself, "Why are the ones with a smaller height the most important ones, don't objects look bigger when they're close?" which would be the case, however, we count the height from the start of the camera to the pillar itself to approximate distance, so the smaller that threshold is, the closer it is to the camera and by association, the robot. This information is then fed to the hub, which will know how to react to each pillar it "sees", with it increasing the angle by increments of ~10 using a similar system to the PID (Check that part), except for emergency where it lands on 45 instead of the expected 48 as that would go beyond the robot's physical limits.

### 2.5 Defining the urgency of the blob

To define the urgency of the blob, we use a mix between the "size" mentioned in section 2.4 and the position on x of the block with a "value" of sorts that can range from -2 to 2, this value can increment depending on different characteristics such as the block being far away or the size exceeding certain points along with the modes mentioned before, any blobs that hit -2 are not considered in the moment though still kept in check in case of any changes and the higher the value of a specific blob, the more likely it'll be to be avoided.

---
**Click [here](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/014eff31a032fad2efbe3ca8a4c5d52e492b31d6/README.md) to go back to the main page.**
