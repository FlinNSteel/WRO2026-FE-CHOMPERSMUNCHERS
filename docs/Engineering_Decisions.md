# Engineering Decisions

This section explains some of the key architectural, hardware, and algorithmic choices made during the development of our vehicle. 

---

### 1. Why LEGO SPIKE Prime?

As an up and coming team, there was bound to be a lot of trial and error with basic concepts which would mean lots of prototyping on parts that seemed "simple" or "basic". Which is why the LEGO SPIKE Prime kit was ideal for us, with lego providing a solid toolset with all the basic materials needed for the robot along with the proper flexibility to commit any changes needed on the fly, we are planning in the future to pivot towards more professional hardware such as switching out the lego hub for a raspberry or audino, however lego ended up being the best option for the time being since most of the team members had little to no experience with electronics, making this is a perfect opportunity to ensure a decent amount of customizability without overwhelming any of the members with details like learning breadboards or soddering.

The **LEGO SPIKE Prime Hub** also has several key advantages:

* **Integrated High-Precision IMU:** The built-in 6-axis gyro/accelerometer allows us to maintain stable heading tracking without relying on external IMU boards.
* **Native Pybricks Support:** Running MicroPython via **Pybricks** provides raw execution speed, low-latency control loops, and direct access to non-blocking background tasks.
* **Reliable Motor Encoders:** SPIKE motors feature built-in high-resolution optical encoders essential for precise distance travel and steering angle tracking.

<img src="https://i.postimg.cc/L8gZ5cJD/LEGO-SPIKE.png" width="50%" height="50%">

---

### 2. Why OpenMV?
For visual recognition tasks, we chose an **OpenMV Cam** over a full single-board computer (like a Raspberry Pi):

* **Dedicated Traffic Sign Detection:** OpenMV processes color detection and object tracking for traffic signs directly on-board, offloading visual processing from the SPIKE Hub.
* **Low Power & Fast Boot:** Instant boot time ensures no startup delays during competition runs while drawing minimal current from the system.
* **Simple I/O Interfacing:** Communicates cleanly with the main hub to pass real-time traffic sign detections directly to the decision-making loop.

<img src="https://i.postimg.cc/0jxQ2HVG/Camara.png" width="50%" height="50%">

---

### 3. Why This Mechanical Structure?
Our vehicle's structural layout was designed around stability, balance, and sensor optimization:

* **Robust Base Frame:** Configured to support heavy electronic payloads while maintaining a clean distribution of mass across all axes.
* **Low Center of Gravity (CoG):** Heavy components like the SPIKE Hub and OpenMV module are mounted low and centrally to prevent tipping during sharp, sudden turns.
* **Strategic Sensor Placement:** Sensors are positioned at extreme outer boundaries (front, side, bottom) to maximize reaction time before approaching track walls or markers.

<img src="https://i.postimg.cc/4y7rvwbz/NOTECHOQUES.avif" alt="Back View" width="600"/>

---

### 4. Why These Sensors?
Our sensor suite was built to provide modular, redundant data streams:

* **Dual Ultrasonic Sensors (Left & Right):** Placed laterally for real-time wall detection and repulsive steering alignment (`giro_ajuste`), preventing physical collisions.
* **Ground Color Sensor:** Optimized using HSV (Hue, Saturation, Value) color spaces rather than RGB to reliably distinguish colored section markers under changing ambient light.
* **Internal Gyroscope (Yaw Tracking):** Provides continuous heading feedback to correct drift on straightaways and execute precise 90° turn transitions.

---

### 5. Why This Control Algorithm?
We implemented a **Proportional-Integral-Derivative (PID) Heading Controller** integrated with **Proportional Ultrasonic Repulsion**:

* **Closed-Loop Heading Control:** The PID loop dynamically counters motor imbalance and mechanical drift by adjusting steering angles relative to the targeted IMU yaw heading.
* **Non-Blocking Sensor Reading:** Sensor inputs use median filtering across buffered samples (`leer_sensores()`) to reject ultrasonic noise without halting execution flow.
* **State Machine Architecture:** Clear separation of linear driving, wall avoidance, and cornering routines prevents race conditions during task switching.

---

### 6. Why This Target Velocity?
Finding the optimal velocity was an iterative process driven by mechanical changes and software processing limits:

* **Iteration 1 (Ackermann Steering):** Early iterations used Ackermann steering aiming for high speeds without added weight. However, the high speed outpaced the control loop's sensor reading rate, causing stability issues.
* **Iteration 2 (Full Motor Speed):** We reverted to a standard chassis design and pushed motors to maximum speed, which performed well prior to full vision hardware integration.
* **Final Configuration (`VELOCIDAD_AVANCE = 20000`):** Adding the OpenMV camera and mounting hardware increased the overall vehicle weight. To ensure smooth motor torque, prevent loss of traction, and give the visual processing system sufficient time to recognize traffic signs, we settled on 20,000 units. This speed provides the perfect balance between stability, power output, and system accuracy.

---
**Click [here](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/014eff31a032fad2efbe3ca8a4c5d52e492b31d6/README.md) to go back to the main page.**
