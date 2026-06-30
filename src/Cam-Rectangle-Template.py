# This work is licensed under the MIT license.
# Copyright (c) 2013-2025 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor
import time

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.VGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.

max_width = 635
max_height = 480
rectangle_width= int(max_width/2)
rectangle_height= int(max_height/7)
Green_Threshold= (30, 100, -64, -8, -32, 32)
Red_Threshold= (12, 100, -47, 14, -1, 58)
gap_top = 50
gap_bottom = 100

while True:
    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot()  # Take a picture and return the image.
    print(clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
    # to the IDE. The FPS should increase once disconnected.
    # Top triangles, used for wall
    img.draw_rectangle(1, 1, rectangle_width-gap_top, rectangle_height, color=(255, 102, 255), thickness=2)
    img.draw_rectangle(int((max_width/2)+gap_top), 1, rectangle_width-gap_top, rectangle_height, color=(255, 102, 255), thickness=2)
    #below Top triangles, used for uhyhhh uhhh idk
    img.draw_rectangle(1, rectangle_height, rectangle_width-gap_bottom, int(rectangle_height*0.6), color=(255, 143, 221), thickness=2)
    img.draw_rectangle(int((max_width/2)+gap_bottom), rectangle_height, rectangle_width-gap_bottom, int(rectangle_height*0.6), color=(255, 143, 221), thickness=2)
    # Floor lines, for like the lines on the floor haha get it
    img.draw_rectangle(1, int(max_height-int(rectangle_height*0.8)), max_width, int(rectangle_height*0.8), color=(255, 0, 178), thickness=2)
