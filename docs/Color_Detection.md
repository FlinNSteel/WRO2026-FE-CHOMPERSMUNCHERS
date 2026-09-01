# Color Detection
This section explains how color detection is implemented on the robot using the bottom-mounted SPIKE Prime Color Sensor. 
It details how the sensor was configured, the exact functions used to evaluate terrain markers, and the logic implemented to minimize detection errors during navigation.
  </p>
</section>

<hr />

<section>
  <h2>Color Sensor Hardware</h2>
  <p>
    The Color Sensor (connected to <code>Port.E</code>) is mounted underneath the chassis facing downward. 
    It is primarily used to detect colored floor markers (such as the blue or orange lines in WRO Future Engineers tracks) to trigger automatic turning decisions.
  </p>

  <h3>How It Works</h3>
  <ul>
    <li><b>Light Emission:</b> The sensor projects white light from its internal LEDs onto the surface below.</li>
    <li><b>Photodiode Spectrum Detection:</b> Integrated Red, Green, and Blue (RGB) photodiodes measure the light reflected off the surface.</li>
    <li><b>Color Space Translation (HSV):</b> Raw RGB reflectance is mathematically converted by Pybricks into the <b>HSV (Hue, Saturation, Value)</b> color space:
      <ul>
        <li><b>Hue (<i>H</i>):</b> Represents the color type as an angle from 0° to 360° on the color wheel.</li>
        <li><b>Saturation (<i>S</i>):</b> Indicates color purity/intensity (0% to 100%). White, black, or neutral tile surfaces exhibit low saturation (<i>S</i> ≤ 35%), whereas vivid colors exhibit high saturation (<i>S</i> > 35%).</li>
        <li><b>Value (<i>V</i>):</b> Represents overall brightness/luminance (0% to 100%).</li>
      </ul>
    </li>
  </ul>
</section>

<hr />

<section>
  <h2>Functions & Code Architecture</h2>

  <h3>A. Sensor Initialization</h3>
<pre><code class="language-python">sensor_color = ColorSensor(Port.E)
</code></pre>
  <p>Instantiates the <code>ColorSensor</code>
  <h3>B. Live Readings: <code>sensor_color.hsv()</code></h3>
<pre><code class="language-python">hue, saturation, value = sensor_color.hsv()
</code></pre>
  <p>Returns a tuple containing <code>(hue, saturation, value)</code>:</p>
  <ul>
    <li><code>hue</code>: Integer [0, 359]</li>
    <li><code>saturation</code>: Integer [0, 100]</li>
    <li><code>value</code>: Integer [0, 100]</li>
  </ul>
  <p>In the main control loop, continuous non-blocking polling captures these values on every iteration.</p>

  <h3>C. Decision Logic: <code>AmIGayQuiz(s, h)</code></h3>
  <p>This function processes raw HSV data to decide whether to execute a turn, increment section counters, or ignore surface noise.</p>

<pre><code class="language-python">def AmIGayQuiz(s, h):
    print('color:', sensor_color.hsv())
    if s > 35:
        if h < 300:
            wait(100)
            girar(1, 100, -100)   # Blue line -> Turn Left
            print("blue")
            robot_state["seccion_actual"] += 1
            robot_state["cant_giros"] += 1
            reloj_rot.reset()
        else:
            wait(100)
            girar(-1, 100, -100)  # Orange/Magenta line -> Turn Right
            print("orang")
            robot_state["seccion_actual"] += 1
            robot_state["cant_giros"] += 1
            reloj_rot.reset()
    else:
        print("white, ignored")
</code></pre>

  <h4>Decision Flow Breakdown</h4>
  <ol>
    <li>
      <b>Saturation Filtering (<code>s > 35</code>):</b> 
      Discriminates active lines from neutral background surfaces. If saturation is 35% or lower, the surface is classified as white/gray background, printing <code>"white, ignored"</code> without altering robot behavior.
    </li>
    <li>
      <b>Hue Classification (<code>h < 300</code>):</b>
      <ul>
        <li><b><code>h < 300</code> (Blue Target):</b> Standard blue lines yield hue values around 200°–240°. Values under 300° trigger a left turn via <code>girar(1, ...)</code>.</li>
        <li><b><code>h >= 300</code> (Orange / Magenta Target):</b> Orange and red/magenta lines map to high hue angles (over 300° or wrapping near 360°). Values of 300° or higher trigger a right turn via <code>girar(-1, ...)</code>.</li>
      </ul>
    </li>
    <li>
      <b>State & Debounce Management:</b>
      <ul>
        <li>Increments <code>seccion_actual</code> and <code>cant_giros</code> in the global state dictionary.</li>
        <li>Calls <code>reloj_rot.reset()</code> to reset the rotation timer, preventing multi-triggering while the sensor passes over a single wide line.</li>
      </ul>
    </li>
  </ol>
</section>

<hr />

<section>
  <h2>Troubleshooting & Reliability Optimizations</h2>
  <p>To minimize color reading errors during high-speed runs, the following safeguards were integrated into the code:</p>
  <ul>
    <li><b>Time Debouncing (<code>reloj_rot.time() > 950</code>):</b> Evaluation of <code>AmIGayQuiz</code> only occurs if at least 950 ms have elapsed since the last detected turn. This prevents the robot from re-triggering while exiting a turn line.</li>
    <li><b>Direct HSV Thresholding over Pre-defined Classes:</b> Instead of relying on <code>sensor_color.color()</code>, raw HSV ranges were used directly. This bypasses ambient lighting misclassifications inherent to standard color matching functions.</li>
    <li><b>Hardware Shielding:</b> Mounting height was fixed to maintain a consistent focal distance, mitigating shadow distortions from room lighting.</li>
  </ul>
</section>

<hr />

**Click [here](https://github.com/FlinNSteel/WRO2026-FE-CHOMPERSMUNCHERS/blob/014eff31a032fad2efbe3ca8a4c5d52e492b31d6/README.md) to go back to the main page.**
