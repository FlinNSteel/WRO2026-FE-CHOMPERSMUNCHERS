# Sensor Configuration
​1. Hardware Declaration and Initialization
​This is the setup phase where you define which physical port each sensor is attached to and initialize its default behavior.
​Port Mapping: Assigning physical inputs (e.g., Port.C, Port.D, Port.E).
​Sensor Modes: Initializing specific modes (e.g., configuring a motor's internal encoder direction using Direction.CLOCKWISE).
​2. Reading Parameters and Noise Filtering
​Real-world sensors produce noisy data or occasional random spikes. Proper software configuration uses filtering algorithms to clean up signals:
​Median Filtering (Buffers): Instead of reacting to a single raw value, the code stores a small history of readings (N = 5) and calculates the median. This removes extreme outliers—like an ultrasonic sensor briefly reporting 0 mm due to an echo anomaly.
​HSV Color Mapping: For color sensors, raw RGB values are often converted into HSV (Hue, Saturation, Value):
​Hue: Identifies the actual color spectrum (0\text{--}360^\circ).
​Saturation: Measures color intensity (0\text{--}100\%). Setting a saturation threshold (e.g., >35\%) helps filter out ambient white or gray surfaces.
​3. Non-Blocking Sampling
​Reading sensors continuously inside tight execution loops can overwhelm the Hub's processor, causing steering lag or missed events.
​Timer-Based Sampling (StopWatch): Configuring a dedicated sample rate (e.g., reading sensors every 30\text{ ms}) decouples sensor acquisition from the main control loop. This allows your PID drive controller to run smoothly at high frequency while sensor checks happen at fixed, reliable intervals.
​4. Calibration and State Resets
​Sensors need clean baseline states before executing autonomous routines:
SensorConfiguration / Calibration ActionPurpose
Gyroscope / IMUhub.imu.reset_heading(0)Establishes absolute "North" (0^\circ) at startup to prevent rotational drift accumulated from previous runs.
Motor Encodersmotor.reset_angle(0)Resets internal angle counts before starting distance-based maneuvers.
Ultrasonic SensorsSetting safety boundaries (LIMITE_DIST)Filters out readings beyond the robot's physical field of interest.
